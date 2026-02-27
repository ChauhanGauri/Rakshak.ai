import time
from dataclasses import dataclass
from typing import List, Tuple

import torch
import torch.nn.functional as F
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


# Internal labels (model-level)
WEAPON_LABELS: List[str] = [
    "ak_47",
    "insas_rifle",
    "rifle_22",
    "m16",
    "m4_carbine",
    "mp5_smg",
    "uzi_smg",
    "glock_pistol",
    "revolver",
    "shotgun",
    "sniper_rifle",
    "grenade",
    "rpg",
    "knife",
    "sword",
    "crossbow",
    "generic_round_object",  # Negative class decoy for false grenade matches
    "generic_tool",          # Negative class for drills, wrenches, hammers
    "cylindrical_object",    # Negative class for pipes, tubes, umbrellas
    "electronic_device",     # Negative class for cameras, phones, remotes
    "no_weapon",  # "Unknown / No Weapon"
]


PROMPTS = {
    "ak_47": "a clear photo of an AK-47 Kalashnikov assault rifle on a plain background",
    "insas_rifle": "a photo of an INSAS assault rifle used by Indian armed forces",
    "rifle_22": "a photo of a small .22 caliber sporting rifle",
    "m16": "a photo of an M16 5.56 NATO assault rifle with a carrying handle",
    "m4_carbine": "a photo of an M4 carbine rifle with a telescoping stock",
    "mp5_smg": "a photo of an MP5 submachine gun with a curved magazine",
    "uzi_smg": "a photo of an Uzi submachine gun",
    "glock_pistol": "a close-up photo of a Glock semi-automatic pistol on a table",
    "revolver": "a photo of a metal revolver handgun with a rotating cylinder",
    "shotgun": "a photo of a pump-action or double-barrel shotgun laid flat",
    "sniper_rifle": "a photo of a long sniper rifle with a scope and bipod",
    "grenade": "a photo of a military hand grenade with an olive drab or metal casing, textured surface, safety pin, and release lever",
    "rpg": "a photo of a rocket-propelled grenade launcher on a shoulder or on the ground",
    "knife": "a photo of a knife or combat blade with a visible sharp edge",
    "sword": "a photo of a long sword or katana blade",
    "crossbow": "a photo of a modern crossbow or hunting bow",
    "generic_round_object": "a photo of a generic round or spherical object like a ball, fruit, or toy",
    "generic_tool": "a photo of a generic hand tool or power tool like a drill, hammer, saw, or wrench",
    "cylindrical_object": "a photo of a harmless cylindrical or tube-like object like a metal pipe, bottle, or umbrella",
    "electronic_device": "a photo of a consumer electronic device like a camera, phone, tripod, or laptop",
    "no_weapon": "a photo with no weapons, only everyday objects, people, or landscapes",
}


@dataclass
class PredictionResult:
    label: str
    score: float
    top_k: List[Tuple[str, float]]
    raw_logits: List[float]
    device: str
    inference_time_ms: float


class WeaponClassifier:
    """
    Zero-shot weapon-category classifier using CLIP.

    Instead of requiring supervised fine-tuning, this classifier compares the
    image against natural-language prompts for each weapon category using CLIP.
    This tends to work reasonably well on web images without a custom dataset,
    but it is still not perfect and should be treated as approximate.
    """

    def __init__(
        self,
        model_name: str = "openai/clip-vit-base-patch32",
        confidence_threshold: float = 0.3,
        device: str | None = None,
    ) -> None:
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def predict(self, image: Image.Image, top_k: int = 3) -> PredictionResult:
        """
        Run zero-shot inference on a single PIL image using CLIP similarity to
        natural-language prompts for each category.
        """
        if image.mode != "RGB":
            image = image.convert("RGB")

        texts = [PROMPTS[label] for label in WEAPON_LABELS]

        start = time.perf_counter()
        inputs = self.processor(
            text=texts,
            images=image,
            return_tensors="pt",
            padding=True,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outputs = self.model(**inputs)
        end = time.perf_counter()

        # logits_per_image shape: (1, num_labels)
        logits = outputs.logits_per_image[0]
        probs = F.softmax(logits, dim=-1)

        k = min(top_k, len(WEAPON_LABELS))
        scores, indices = torch.topk(probs, k=k)

        scores_list = scores.detach().cpu().tolist()
        indices_list = indices.detach().cpu().tolist()

        top_label_idx = indices_list[0]
        top_label = WEAPON_LABELS[top_label_idx]
        top_score = scores_list[0]

        if top_score < self.confidence_threshold or top_label in [
            "generic_round_object",
            "generic_tool",
            "cylindrical_object",
            "electronic_device",
        ]:
            top_label = "no_weapon"

        top_predictions: List[Tuple[str, float]] = []
        for idx, score in zip(indices_list, scores_list):
            label = WEAPON_LABELS[idx]
            top_predictions.append((label, float(score)))

        return PredictionResult(
            label=top_label,
            score=float(top_score),
            top_k=top_predictions,
            raw_logits=logits.detach().cpu().tolist(),
            device=self.device,
            inference_time_ms=(end - start) * 1000.0,
        )

    def save_finetuned(self, output_dir: str) -> None:
        """
        Included for API compatibility; CLIP here is used zero-shot,
        so this is not used in the current setup.
        """
        self.model.save_pretrained(output_dir)
        self.processor.save_pretrained(output_dir)

    @classmethod
    def load_finetuned(
        cls,
        checkpoint_dir: str,
        confidence_threshold: float = 0.3,
        device: str | None = None,
    ) -> "WeaponClassifier":
        """
        Load a previously saved CLIP checkpoint (if you choose to fine-tune).
        """
        instance = cls.__new__(cls)
        instance.model_name = checkpoint_dir
        instance.confidence_threshold = confidence_threshold

        if device is None:
            instance.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            instance.device = device

        instance.processor = CLIPProcessor.from_pretrained(checkpoint_dir)
        instance.model = CLIPModel.from_pretrained(checkpoint_dir)
        instance.model.to(instance.device)
        instance.model.eval()

        return instance

