import os
import time
from typing import Optional

import streamlit as st
from PIL import Image

from model.classifier import WeaponClassifier, PredictionResult
from model.weapon_info import (
    get_weapon_info,
    get_weapon_label_display_name,
)
from utils.image_processing import read_image_as_pil
from utils.audio import load_weapon_sound_bytes, generate_tts_audio_bytes

def compute_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    if inter_area == 0:
        return 0.0
    
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    return inter_area / float(area1 + area2 - inter_area)

def apply_nms(detections, iou_threshold=0.4):
    detections = sorted(detections, key=lambda x: x["prediction"].score, reverse=True)
    kept_detections = []
    
    for det in detections:
        keep = True
        for kept_det in kept_detections:
            if compute_iou(det["box"], kept_det["box"]) > iou_threshold:
                keep = False
                break
        if keep:
            kept_detections.append(det)
            
    return kept_detections


# ----------------------------
# Streamlit Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Rakshakai - AI Weapon Recognition",
    page_icon="RAKSHAKAI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------
# Custom Dark Military Theme
# ----------------------------
CUSTOM_CSS = """
<style>
/* import a sci-fi, monospaced font and fallbacks */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

/* Global dark defense theme with gradient background and subtle noise */
.stApp {
    background: linear-gradient(135deg, #111 0%, #222 100%);
    background-attachment: fixed;
    color: #f5f5f5;
    font-family: 'Orbitron', 'Segoe UI', sans-serif;
    overflow-x: hidden;
}

/* subtle animated noise overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    background: url('https://www.transparenttextures.com/patterns/black-linen.png');
    opacity: 0.15;
}

/* Header radar rotation */
.radar-icon {
    display: inline-block;
    animation: rotateRadar 6s linear infinite;
}

/* shift background gradient slowly */
@keyframes bgShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp {
    background: linear-gradient(135deg, #111 0%, #222 100%);
    background-size: 200% 200%;
    animation: bgShift 30s ease-in-out infinite;
}

@keyframes rotateRadar {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Section title slide in */
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

.rakshakai-section-title {
    animation: slideIn 0.6s ease-out;
}

/* Button pulse */
@keyframes pulse {
    0%,100% { box-shadow: 0 0 12px rgba(0,0,0,0.8); }
    50% { box-shadow: 0 0 18px rgba(107, 142, 35, 0.5); }
}
.stButton>button {
    animation: pulse 3s ease-in-out infinite;
}

/* Badge pop animation when discovered */
@keyframes pop {
    0% { transform: scale(0.5); opacity: 0; }
    60% { transform: scale(1.1); opacity: 1; }
    100% { transform: scale(1); }
}
.confidence-badge, .warning-badge {
    animation: pop 0.6s ease-out;
}

/* glowing pulse for confidence badge border */
@keyframes glow {
    from { box-shadow: 0 0 4px #6b8e23; }
    to { box-shadow: 0 0 12px #6b8e23; }
}
.confidence-badge {
    animation: pop 0.6s ease-out, glow 3s infinite alternate;
}

/* Result block fade (for detection section) */
.result-block {
    animation: fadeIn 0.5s ease-out;
}

/* Main container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Header */
.rakshakai-header {
    padding: 1.5rem 1.8rem;
    border-radius: 12px;
    background: radial-gradient(circle at top left, #243324, #050608 55%);
    border: 1px solid #3b4a3b;
    position: relative;
    overflow: hidden;
}

/* Animated subtle scan line */
.rakshakai-header::after {
    content: "";
    position: absolute;
    top: -50%;
    left: -100%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        120deg,
        rgba(107, 142, 35, 0.06),
        rgba(255, 255, 255, 0.0),
        rgba(107, 142, 35, 0.06)
    );
    animation: headerSweep 8s linear infinite;
}

@keyframes headerSweep {
    0% { transform: translateX(-40%); }
    100% { transform: translateX(40%); }
}

.rakshakai-title {
    font-size: 2.2rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #dbe6c3;
    font-weight: 700;
    animation: fadeIn 1s ease-out;
}

.rakshakai-subtitle {
    font-size: 1.0rem;
    color: #a3b19a;
    margin-top: 0.2rem;
}

.rakshakai-badge {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: #b0ffb2;
    background: rgba(12, 34, 12, 0.85);
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    border: 1px solid #6b8e23;
}

/* Cards */
.rakshakai-card {
    background: linear-gradient(145deg, #0c1010, #050608);
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    border: 1px solid #2a382a;
    box-shadow: 0 0 14px rgba(0, 0, 0, 0.7);
    transition: transform 0.2s ease-out, box-shadow 0.2s ease-out, border-color 0.2s ease-out;
    animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.rakshakai-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 22px rgba(0, 0, 0, 0.9);
    border-color: #6b8e23;
}

/* Section titles */
.rakshakai-section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #d6e0c2;
    border-left: 3px solid #6b8e23;
    padding-left: 0.6rem;
    margin-bottom: 0.8rem;
}

/* Result image styling */
.result-image {
    border: 2px solid #6b8e23;
    border-radius: 8px;
}

/* Top predictions list */
.top-predictions {
    list-style: disc inside;
    padding-left: 1rem;
}
.top-predictions li {
    margin: 0.2rem 0;
}

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 999px;
    border: 1px solid #6b8e23;
    background: radial-gradient(circle at 20% 20%, #1c2520, #050608);
    color: #f5f5f5;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-size: 0.75rem;
    padding: 0.55rem 0.3rem;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.8);
    transition: background 0.2s ease-out, transform 0.1s ease-out, box-shadow 0.2s ease-out;
}

.stButton>button:hover {
    transform: translateY(-1px);
    background: radial-gradient(circle at 80% 0%, #223622, #050608);
    box-shadow: 0 0 18px rgba(107, 142, 35, 0.4);
}

/* File uploader */
.css-1cpxqw2, .stFileUploader {
    background-color: #060909 !important;
    border-radius: 10px !important;
    border: 1px dashed #3a4d35 !important;
}

/* Metrics / labels */
.confidence-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    border: 1px solid #6b8e23;
    font-size: 0.8rem;
    color: #dbe6c3;
    background: rgba(22, 38, 18, 0.85);
}

.warning-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    border: 1px solid #c27b0a;
    font-size: 0.8rem;
    color: #ffdfb3;
    background: rgba(54, 32, 4, 0.9);
}

/* Expander styling */
.streamlit-expanderHeader {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #c4d4b1;
}

/* Sidebar tweaks */
section[data-testid="stSidebar"] {
    background: #0a0d0f;
    border-right: 1px solid #3b4a3b;
}

/* Slider track and thumb */
.stSlider > div > div > div > div {
    background: #6b8e23 !important;
}
.stSlider .stMarkdown {
    color: #dbe6c3;
}

/* Custom scrollbar for dark theme */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: rgba(107, 142, 35, 0.6);
    border-radius: 4px;
}
::-webkit-scrollbar-track {
    background: #050608;
}

/* Enhanced links */
a {
    color: #9cc472;
    text-decoration: none;
}
a:hover {
    color: #c2e29a;
    text-decoration: underline;
}
/* Images in Streamlit blocks (uploads/results) */
.stImage img {
    border-radius: 8px;
    border: 2px solid #6b8e23;
}

/* Animate images when they appear inside result block */
.result-block .stImage img {
    animation: pop 0.6s ease-out;
}
/* Footer styling - added by script in markup */
.rakshakai-footer {
    font-size: 0.75rem;
    color: #7f8c7f;
    text-align: center;
    margin-top: 2rem;
}

/* Audio player background */
audio {
    outline: none;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def get_classifier(confidence_threshold: float) -> WeaponClassifier:
    return WeaponClassifier(confidence_threshold=confidence_threshold)

@st.cache_resource(show_spinner=False)
def get_detector():
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")
    return model

def main():
    # Header
    with st.container():
        st.markdown(
            """
            <div class="rakshakai-header">
                <div style="display:flex; flex-direction:row; justify-content:space-between; align-items:flex-start; gap:1rem;">
                    <div style="display:flex; align-items:center; gap:0.8rem;">
                        <div class="radar-icon">
                            <img src="https://img.icons8.com/ios/50/ffffff/radar--v1.png" alt="radar" style="width:48px;height:48px;" />
                        </div>
                        <div>
                            <div class="rakshakai-title">RAKSHAKAI</div>
                            <div class="rakshakai-subtitle">AI Defense Recognition System</div>
                        </div>
                    </div>
                    <div style="display:flex; flex-direction:column; align-items:flex-end; gap:0.2rem;">
                        <div class="rakshakai-badge">Mode: Analysis Only</div>
                        <div style="font-size:0.7rem; color:#7f8c7f;">No targeting or engagement capabilities</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # Sidebar controls
    with st.sidebar:
        st.markdown("#### Detection Settings")
        confidence_threshold = st.slider(
            "Confidence threshold",
            min_value=0.05,
            max_value=0.95,
            value=0.45,
            step=0.05,
            help="Minimum confidence score required to report a weapon instead of 'Unknown / No Weapon'.",
        )

        st.markdown("---")
        st.markdown("#### System Info")
        st.markdown(
            """
            - **Model**: Vision Transformer (ViT)
            - **Backend**: PyTorch + Transformers
            - **Interface**: Streamlit (demo, not fine-tuned)
            - **Purpose**: Awareness, documentation, and research.
            """
        )

        st.markdown("---")
        st.markdown(
            """
            **Ethical Notice**

            Rakshakai is designed strictly for:
            - Educational demonstrations  
            - Historical/technical understanding  
            - Defensive and safety research  

            It must **not** be used for weapon procurement, modification, or operational planning.
            """
        )

    classifier = get_classifier(confidence_threshold=confidence_threshold)
    classifier.confidence_threshold = confidence_threshold

    try:
        detector = get_detector()
    except ImportError:
        st.error("ultralytics package is missing. Please run `pip install ultralytics`.")
        detector = None

    # Layout: left = upload, right = results
    left_col, right_col = st.columns([1.1, 1.3])

    uploaded_image: Optional[Image.Image] = None

    with left_col:
        st.markdown('<div class="rakshakai-card">', unsafe_allow_html=True)
        st.markdown('<div class="rakshakai-section-title">Input Image</div>', unsafe_allow_html=True)

        input_method = st.radio(
            "Select input method:",
            ("Upload Image", "Use Camera"),
            horizontal=True
        )

        uploaded_file = None
        camera_file = None

        if input_method == "Upload Image":
            uploaded_file = st.file_uploader(
                "Upload an image (JPG / PNG)",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
            )
        else:
            camera_file = st.camera_input("Take a picture", label_visibility="collapsed")
        
        input_file = uploaded_file or camera_file

        if input_file is not None:
            uploaded_image = read_image_as_pil(input_file)
            st.session_state['last_uploaded_image'] = input_file.getvalue()
            st.image(uploaded_image, caption="Input Image", width=500)
        elif 'last_uploaded_image' in st.session_state:
            # Show the last uploaded image if available
            from io import BytesIO
            uploaded_image = read_image_as_pil(BytesIO(st.session_state['last_uploaded_image']))
            st.image(uploaded_image, caption="Input Image", width=600)
        else:
            st.info("Awaiting image input...")

        detect_button = st.button("🔍 Analyze Weapon")

        # Reset all play_sound and tts session state keys when a new image is analyzed
        if detect_button:
            for k in list(st.session_state.keys()):
                if k.startswith("play_sound_") or k.startswith("tts_"):
                    st.session_state[k] = False

        st.markdown("</div>", unsafe_allow_html=True)


    with right_col:
        st.markdown('<div class="rakshakai-card result-block">', unsafe_allow_html=True)
        st.markdown('<div class="rakshakai-section-title">Detection Output</div>', unsafe_allow_html=True)

        # Use session state to persist detection results
        detections = None
        annotated_image = None
        
        if detect_button and uploaded_image is not None and detector is not None:
            detections = []
            with st.spinner("Detecting objects in scene with YOLOv8..."):
                results = detector.predict(uploaded_image, conf=0.05, iou=0.45) # Aggressively low confidence to capture all small objects, let ViT filter the garbage
                
            if len(results) > 0 and len(results[0].boxes) > 0:
                with st.spinner("Classifying found objects with Vision Transformer..."):
                    for box in results[0].boxes:
                        b = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = [int(v) for v in b]
                        
                        crop = uploaded_image.crop((x1, y1, x2, y2))
                        
                        # We classify each crop
                        pred = classifier.predict(crop)
                            
                        # Only keep detections that the ViT classifies as weapons
                        if pred.label != "no_weapon":
                            detections.append({"box": (x1, y1, x2, y2), "prediction": pred})

            # Apply NMS on the resulting final bounding boxes so the same physical weapon
            # is not detected multiple times due to YOLO's generous generic proposals
            if len(detections) > 1:
                detections = apply_nms(detections, iou_threshold=0.45)

            # FALLBACK: If YOLO found no relevant objects (e.g., close-up images or unsupported categories)
            if len(detections) == 0:
                with st.spinner("No localized objects identified. Scanning full image as fallback..."):
                    pred = classifier.predict(uploaded_image)
                    if pred.label != "no_weapon":
                        w, h = uploaded_image.size
                        detections.append({"box": (0, 0, w, h), "prediction": pred})
            
            st.session_state['last_detections'] = detections
        elif 'last_detections' in st.session_state:
            detections = st.session_state['last_detections']

        annotated_image = None

        if uploaded_image is not None and detections:
            from PIL import ImageDraw
            annotated_image = uploaded_image.copy()
            draw = ImageDraw.Draw(annotated_image)
            
            for det in detections:
                x1, y1, x2, y2 = det["box"]
                draw.rectangle([x1, y1, x2, y2], outline="#6b8e23", width=4)
                
            st.markdown("##### YOLO Annotated Scene")
            st.image(annotated_image, caption="Bounding boxes around potential weapons")

        if detections is not None:
            if len(detections) == 0:
                st.markdown(
                    '<span class="warning-badge">No weapons detected in the scene by the YOLO model.</span>',
                    unsafe_allow_html=True,
                )
            else:
                for idx, det in enumerate(detections):
                    st.markdown("---")
                    st.markdown(f"#### Detection {idx + 1}")
                    x1, y1, x2, y2 = det["box"]
                    # Crop dynamically so we don't depend on stale fast-state images
                    crop_img = uploaded_image.crop((x1, y1, x2, y2))
                    prediction = det["prediction"]
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(crop_img, caption="Cropped Object")
                    
                    with col2:
                        display_label = get_weapon_label_display_name(prediction.label)
                        info = get_weapon_info(prediction.label)

                        if prediction.label == "no_weapon":
                            st.markdown(
                                '<span class="warning-badge">Object classified as non-weapon / unknown.</span>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<span class="confidence-badge">Classified as: <strong>{display_label}</strong> '
                                f'({prediction.score * 100:.1f}% confidence)</span>',
                                unsafe_allow_html=True,
                            )

                            # Add play sound button if sound exists for this weapon
                            audio_bytes = load_weapon_sound_bytes(prediction.label)
                            play_key = f"play_sound_{idx}_{display_label}"
                            if audio_bytes:
                                if st.button(f"Play {display_label} sound", key=f"btn_audio_{idx}"):
                                    st.session_state[play_key] = True
                                if st.session_state.get(play_key, False):
                                    try:
                                        st.audio(audio_bytes, format='audio/mp3')
                                    except Exception as e:
                                        st.warning(f"Error playing sound: {e}")
                            else:
                                st.info("No sound available for this weapon.")

                        st.write("")
                        st.markdown("**Overview**")
                        if prediction.label == "no_weapon":
                            st.write(
                                "CLIP did **not** recognize this crop as a known weapon category with sufficient confidence."
                            )
                        else:
                            st.write(f"**Type**: {info.get('type', 'N/A')}")
                            st.write(f"**Country of Origin**: {info.get('origin', 'N/A')}")
                            
                            st.write("")
                            st.markdown("**Historical / Technical Description**")
                            st.write(info.get("description", ""))
                            
                            st.write("")
                            st.markdown("**Common Usage Context**")
                            st.write(info.get("usage", ""))

                            # --- Audio Transcription / Text-to-Speech ---
                            st.write("")
                            st.markdown("**Audio Transcription (Voice Narration)**")
                            tts_key = f"tts_{idx}_{display_label}"
                            if st.button("🔊 Narrate Details", key=f"btn_{tts_key}"):
                                st.session_state[tts_key] = True

                            if st.session_state.get(tts_key, False):
                                with st.spinner("Generating audio transcription..."):
                                    description_text = f"Weapon detected: {display_label}. " \
                                                       f"Type: {info.get('type', 'Unknown')}. " \
                                                       f"Description: {info.get('description', '')}"
                                    tts_bytes = generate_tts_audio_bytes(description_text)
                                    if tts_bytes:
                                        st.audio(tts_bytes, format='audio/mp3')
                                    else:
                                        st.warning("Failed to generate audio transcription.")

                        # Technical details expander
                        with st.expander("Technical details (model, logits, and top predictions)"):
                            st.write(f"**CLIP Inference time**: {prediction.inference_time_ms:.2f} ms")
                            st.markdown("**Top predictions:**")
                            st.markdown("<ul class=\"top-predictions\">", unsafe_allow_html=True)
                            for label, score in prediction.top_k:
                                st.markdown(
                                    f"<li>{get_weapon_label_display_name(label)}: {score * 100:.2f}%</li>",
                                    unsafe_allow_html=True,
                                )
                            st.markdown("</ul>", unsafe_allow_html=True)
        else:
            st.info(
                "Upload/Capture an image on the left and press **Run Weapon Detection** to find weapons using YOLO-World."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # page footer
    st.markdown(
        '<div class="rakshakai-footer">Rakshakai demo &bull; AI Weapon Recognition powered by Streamlit &amp; Transformers</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

