# Rakshakai – AI Defense Recognition System

Rakshakai is an **AI-powered weapon recognition system** built with a Vision Transformer (ViT), PyTorch, and Streamlit.  
It analyzes images to **identify weapon categories** and provides **neutral, educational information** such as type, origin, introduction year, and historical/technical context.

> **Important:**  
> Rakshakai is intended **only** for awareness, research, and educational demonstrations.  
> It **must not** be used for weapon procurement, modification, targeting, or any offensive planning.

---

## Project Overview

- **Image-based classification** using a pretrained Vision Transformer (ViT) from HuggingFace Transformers.
- **Weapon category recognition** (e.g., AK‑47, INSAS Rifle, M16, Glock Pistol, Grenade, etc.).
- **Neutral metadata**:
  - Weapon name
  - Type (Assault Rifle / Handgun / Explosive / etc.)
  - Country of origin
  - Year introduced
  - Short historical/technical description
  - Common usage context (military / law enforcement)
- **Audio features**:
  - Simulated firing sounds via pre‑stored `.mp3` files
  - Optional voice narration of descriptions using gTTS
- **Modern defense-style UI**:
  - Dark military theme with olive green highlights
  - Subtle animated header sweep
  - Streamlit-based layout

---

## Tech Stack

- **Language**: Python
- **Core Libraries**:
  - [PyTorch](https://pytorch.org/) – model backend
  - [Transformers (HuggingFace)](https://huggingface.co/docs/transformers/) – ViT model + image processor
  - [Streamlit](https://streamlit.io/) – UI
  - [OpenCV](https://opencv.org/) – image handling (optional utilities)
  - [Pillow](https://python-pillow.org/) – image loading
  - [gTTS](https://pypi.org/project/gTTS/) – text-to-speech
  - `playsound` – included for optional local playback use cases
  - [ultralytics](https://github.com/ultralytics/ultralytics) – YOLOv8/YOLO-World object detection

---

## Project Structure

```text
rakshakai/
    app.py
    requirements.txt
    README.md
    model/
        __init__.py
        classifier.py
        weapon_info.py
    utils/
        __init__.py
        audio.py
        image_processing.py
    sound/
        M16.mp3
        grenade.mp3
        sniper-rifle.mp3
```

- `app.py`: Streamlit UI and end-to-end workflow.
- `model/classifier.py`: ViT-based classifier wrapped in a clean API.
- `model/weapon_info.py`: Weapon metadata dictionary and label mapping.
- `utils/image_processing.py`: Image loading and preprocessing helpers.
- `utils/audio.py`: Audio asset lookup and text-to-speech utilities.
- `sound/`: Pre-stored `.mp3` audio files for firing sound simulation.

---

## Installation

1. **Navigate into the project**

   ```bash
   cd rakshakai
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux / macOS
   source .venv/bin/activate
   ```


3. **Install dependencies**

  ```bash
  pip install -r requirements.txt
  ```

  If you plan to use the YOLOv8/YOLO-World detection features, ensure the `ultralytics` package is installed:

  ```bash
  pip install ultralytics
  ```

4. **Add audio assets**

   Place your `.mp3` files at:

   - `sound/M16.mp3`
   - `sound/grenade.mp3`
   - `sound/sniper-rifle.mp3`

   You can extend `sound` and `utils/audio.py` to support more granular audio profiles.

---

## How to Run

From the `rakshakai` directory:

```bash
streamlit run app.py
```


If you want to use YOLO-based detection, make sure the YOLO model files (`yolov8n.pt`, `yolov8s-world.pt`) are present in the project root. You can download these from the [Ultralytics YOLOv8 releases](https://github.com/ultralytics/ultralytics/releases) or train your own.

Then open the URL displayed in your terminal (typically `http://localhost:8501`) in a browser.

---

## Usage

1. **Open the Streamlit app** in your browser.
2. **Upload an image** that may contain a weapon.
3. Click **“Run Weapon Detection”**.
4. The app will:
   - Run the ViT classifier on the image.
   - Display:
     - Predicted weapon name (or **Unknown / No Weapon**)
     - Confidence score
     - Type, origin, year, description, and usage context
   - Provide:
     - Simulated firing sound playback (if configured for that label)
     - Optional text-to-speech narration of the description
   - Show an expandable **Technical details** section with model info and top‑k predictions.

A configurable **confidence threshold** in the sidebar determines when the model reports a specific weapon vs. the conservative **Unknown / No Weapon** category.

---

## Notes on the Model

- The current implementation uses a **generic pretrained ViT backbone** with a custom classification head configured for the weapon labels.
- In this reference project, the head is **not fine-tuned** on a real weapon dataset.  
  Predictions are therefore **demonstrative**, not authoritative.
- For realistic performance, you should:
  - Curate a high-quality labeled dataset of weapon / non‑weapon images.
  - Fine-tune the ViT model on that dataset.
  - Save and load your fine-tuned checkpoint via `WeaponClassifier.save_finetuned` and `WeaponClassifier.load_finetuned`.

---

## Future Improvements

- **Real dataset fine-tuning**
  - Collect and curate a responsibly sourced dataset.
  - Train and evaluate the ViT classifier with rigorous validation and bias checks.

- **Live camera detection**
  - Integrate OpenCV video capture for near-real-time analysis.
  - Add frame-by-frame detection with rate limiting and overlays.

- **Integration with surveillance systems**
  - Secure APIs for streaming frames from surveillance sources.
  - Event logging, alerting workflows, and auditing.
  - Strict role-based access controls and monitoring.

- **Robust evaluation and governance**
  - False-positive and false-negative analysis.
  - Documentation of limitations and bias risks.
  - Human-in-the-loop review for any critical use.

---

## Ethical and Legal Disclaimer

Rakshakai is provided for **educational, research, and awareness** purposes only.

- It **must not** be used to facilitate:
  - Weapon procurement, distribution, or modification.
  - Targeting, tracking, or engagement of individuals or groups.
  - Any operation that violates local or international law.

Any deployment or extension of this system should include:

- Strong human oversight.
- Clear documentation of limitations.
- Compliance with all applicable regulations and ethical guidelines.

