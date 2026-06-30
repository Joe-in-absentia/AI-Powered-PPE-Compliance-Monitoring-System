import streamlit as st
import hashlib
import os
import tempfile
import cv2
import av
import numpy as np
import boto3
from PIL import Image
from dotenv import load_dotenv
from deepface import DeepFace
from ultralytics import YOLO
from streamlit_webrtc import (webrtc_streamer,VideoProcessorBase)
from database import save_detection
from email_report import send_report
from sql_agent import ask_sql_agent

st.set_page_config( page_title="IntelliGuard",page_icon="🔐",layout="wide")

load_dotenv()

REGISTERED_FACE = os.getenv("FACE_PATH")
PASSWORD_HASH = os.getenv("PASSWORD")

# Section state.
default_states = {
    "logged_in": False,
    "violations": [],
    "video_running": False,
    "video_violations": [],
    "video_completed": False,
    "saved_files": set(),
    "image_saved": False,
    "webcam_saved": False}

for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Load the YOLO model.
@st.cache_resource
def load_model():
    model_path = "best.pt"
    # Download model from S3 if not available locally
    if not os.path.exists(model_path):
        s3 = boto3.client("s3",region_name=os.getenv("AWS_REGION"))
        s3.download_file(os.getenv("S3_BUCKET"),os.getenv("S3_MODEL_PATH"),model_path)
    return YOLO(model_path)

model = load_model()

# Password verification.
def verify_password(password):

    hashed_password = hashlib.sha256( password.encode()).hexdigest()
    return hashed_password == PASSWORD_HASH

# Face verification.
def verify_face(image_file):
    try:
        img = Image.open(image_file).convert("RGB")
        img_array = np.array(img)
        result = DeepFace.verify(img1_path=img_array,
            img2_path=REGISTERED_FACE,
            model_name="ArcFace",
            detector_backend="opencv",
            distance_metric="cosine",
            enforce_detection=True)
        
        return result["verified"]

    except Exception as e:
        st.error(f"Face Error: {e}")

        return False

# Violation check.
def is_violation(label):

    label = label.lower()
    return ("no_" in label
            or "no-" in label
            or "no " in label)

# YOLO detection.
def detect_objects(frame):

    results = model.predict(frame,conf=0.5,imgsz=640,verbose=False)[0]
    annotated = frame.copy()
    violations = []

    for box in results.boxes:
        x1,y1,x2,y2 = (box.xyxy[0].cpu().numpy().astype(int))
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        label = results.names[class_id]
        cv2.rectangle(annotated,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(annotated,f"{label} {confidence:.2f}",
            (x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

        if is_violation(label):
            violations.append({"label": label,"confidence": confidence})

    return annotated, violations

# Live camera processor.
class VideoProcessor(VideoProcessorBase):

    def __init__(self):
        self.violations = []
        self.frame_count = 0
        self.skip_frames = 2

    def recv(self, frame):
        self.frame_count += 1
        img = frame.to_ndarray(format="bgr24")
        if self.frame_count % self.skip_frames != 0:
            return av.VideoFrame.from_ndarray(img,format="bgr24")

        annotated, violations = detect_objects(img)

        for item in violations:
           if item["label"] not in [
              v["label"] for v in self.violations]:
              self.violations.append(item)

        return av.VideoFrame.from_ndarray(annotated,format="bgr24")


# Login page.
if not st.session_state.logged_in:
    st.title("🔐 IntelliGuard Security Login")
    st.write("### Choose Your Preferred Login Method")
    login_method = st.radio("**Authentication**",["Face Unlock","Password"])
    if login_method == "Face Unlock":
        st.subheader("🙂 Face Recognition")

        # Only camera size changed here.
        st.markdown("""
            <style>
            div[data-testid="stCameraInput"] {
                width: 300px;
                margin-left: auto;
                margin-right: auto;}
            </style>""",
            unsafe_allow_html=True)
        
        # Center camera
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = st.camera_input( "**Look at the camera and capture your face**")
        

        if image:
            if verify_face(image):
                st.success("✅ Face Verified Successfully")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Face Verification Failed")
    else:
        st.subheader("🔑 Password Login")
        password = st.text_input("Password",type="password")

        if st.button("Login"):
            if verify_password(password):
                st.success("✅ Password Correct")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong Password")
else:
    st.title("🛡️ Intelliguard AI-Powered Dashboard")
    st.success("System Active")
    option = st.selectbox("Detection Mode",
                 ["Image Detection","Video Detection","Live Webcam"])


# Image detection.
    if option == "Image Detection":
        st.subheader("Image Detection")
        uploaded_image = st.file_uploader(
              "Upload Image",type=["jpg","jpeg","png"])

        if uploaded_image:
           image_data = uploaded_image.getvalue()
           image_array = np.frombuffer(image_data,np.uint8)
           img = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
           annotated, violations = detect_objects(img)
           st.image(annotated,channels="BGR")

           if violations:
            try:
                if not st.session_state.image_saved:
                 save_detection("image","Image",violations)
                 st.session_state.image_saved = True
                 st.success("✅ Image violation saved to RDS")
                else:
                 st.info("Image already saved")
                st.error(f"🚨 Violations: {[v['label'] for v in violations]}")
            except Exception as e:
                st.error(f"Database Error: {e}")
           else:
            st.success("✅ No Violations")


# Video detection.
    elif option == "Video Detection":
        st.subheader("🎥 Video Detection")
        video_file = st.file_uploader("Upload Video",type=["mp4","avi","mov"])
        if video_file:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,suffix=".mp4")
            temp_file.write(video_file.read())
            video_path = temp_file.name
            col1,col2 = st.columns(2)
            with col1:
                if st.button( "▶ Start Video"):
                    st.session_state.video_running = True
                    st.session_state.video_violations = []
                    st.session_state.video_completed = False

            with col2:
                if st.button( "⏹ Stop Video"):
                    st.session_state.video_running = False
                    st.session_state.video_completed = True
            frame_placeholder = st.empty()

            if st.session_state.video_running:
                cap = cv2.VideoCapture(video_path)

                while cap.isOpened() and st.session_state.video_running:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    annotated, violations = detect_objects(frame)
                    for item in violations:
                        if item["label"] not in [v["label"] 
                           for v in st.session_state.video_violations]:
                             st.session_state.video_violations.append(item)

                    frame_placeholder.image( annotated,channels="BGR")
                cap.release()
                st.session_state.video_running = False
                st.session_state.video_completed = True

            # Save after video stop.
            if st.session_state.video_completed:
                if st.session_state.video_violations:
                    save_detection("video","video",st.session_state.video_violations)
                    st.success("✅ Video violation saved to RDS")
                st.session_state.video_completed = False
            st.divider()
            st.subheader("🚨 Violation Report")

            if st.session_state.video_violations:
                st.error(f"Detected: {[v['label'] for v in st.session_state.video_violations]}")
            else:
                st.success("✅ No Violations Found")

# Live web cam.
    elif option == "Live Webcam":
        st.subheader("📡 Live CCTV Monitoring")
        ctx = webrtc_streamer(key="intelliguard",
            video_processor_factory=VideoProcessor,
            media_stream_constraints={"video": True,"audio": False})

        if ctx.video_processor:
            st.session_state.violations = (ctx.video_processor.violations)

        # Save when camera stops.
        if not ctx.state.playing:
            if st.session_state.violations and not st.session_state.webcam_saved:
                save_detection("webcam","live_camera",st.session_state.violations)
                st.session_state.webcam_saved = True
                st.success("✅ Webcam violation saved to RDS")
        st.divider()

        if st.session_state.violations:
            st.error(f"🚨 Violations Detected: {[v['label'] for v in st.session_state.violations]}")
        else:
            st.success("✅ No Violations Detected")


# Sidebar for chatbot.
    with st.sidebar:
        st.title(" Chatbot Assistant")
        question = st.chat_input( " 🤖 Ask questions ...")
        if question:
            answer = ask_sql_agent(question)
            st.write("### Answer")
            st.write(answer)


# Email report button.
    st.divider()

    if st.button("📧 Send Violation Report"):
        try:
            send_report()
            st.success("Report sent successfully")

        except Exception as e:
            st.error(f"Email Error: {e}")

    st.divider()
    if st.button(":red[Logout]"):
        st.session_state.logged_in = False
        st.session_state.violations = []
        st.session_state.video_violations = []
        st.session_state.image_saved = False
        st.session_state.webcam_saved = False
        st.rerun()

