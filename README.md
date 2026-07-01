# 🛡️ IntelliGuard: AI-Powered PPE Compliance Monitoring System

<p align="center">
AI-Based Workplace Safety Monitoring Using Computer Vision, Cloud Computing & Generative AI
</p>

---

## 📌 Overview

**IntelliGuard** is an AI-powered workplace safety monitoring system designed to detect Personal Protective Equipment (PPE) compliance in real time using computer vision and deep learning.

The system identifies safety violations from image, video, and live webcam feeds using a trained YOLO object detection model. Detected violations are automatically logged into an AWS cloud database and visualized through an interactive Streamlit dashboard with secure authentication and an AI-powered chatbot for safety analytics.

---

##  Problem Statement

Industrial and manufacturing environments require strict safety compliance. Manual PPE inspection is time-consuming, inconsistent, and difficult to scale.

IntelliGuard automates workplace safety monitoring by:

- Detecting PPE violations such as missing helmet, gloves, mask, goggles, and shoes
- Processing image, video, and live camera streams
- Logging violation records into AWS RDS
- Providing AI-based safety insights through a chatbot interface
- Generating automated reports and alerts

---

## ✨ Key Features

- Real-time PPE violation detection using YOLO
- Face recognition-based secure login system
- Password authentication support
- Streamlit interactive monitoring dashboard
- Image, video, and webcam detection modes
- AWS S3 integration for YOLO model storage
- AWS RDS database for violation tracking
- LangChain SQL chatbot for natural language analytics
- Google Gemini LLM integration
- Automated email violation reports
- CSV report generation
- TensorBoard training visualization

---

#  Tech Stack

## Artificial Intelligence
- YOLO Object Detection
- OpenCV
- DeepFace Face Recognition
- LangChain
- Google Gemini API

## Programming
- Python

## Frontend
- Streamlit

## Database
- PostgreSQL
- AWS RDS

## Cloud Services
- AWS S3
- AWS RDS

## Automation
- SMTP Email Service
- CSV Reporting

## Development Tools
- Git
- GitHub
- TensorBoard

---

# 🎯 Skills Gained

- Computer Vision with OpenCV & YOLO
- Object Detection and Model Fine-Tuning
- Face Recognition Authentication
- Streamlit Application Development
- AWS Cloud Integration (S3, RDS)
- NLP with LLMs and LangChain Agents
- SQL-Based AI Chatbot Development
- SMTP Email Automation
- TensorBoard Experiment Tracking
- End-to-End AI System Development

---

# 🏗️ Domain

- Industrial Safety & Compliance
- Manufacturing Automation
- AI-Based Workplace Monitoring
- Computer Vision Applications
- Cloud-Based Safety Analytics

---

### Dataset Details

- Industrial worker safety images
- YOLO bounding box annotation format
- Training, validation, and testing split
- Image resizing and normalization preprocessing

---

# ☁️ AWS Architecture

## Amazon S3

Used for:

- Storing trained YOLO model (`best.pt`)
- Cloud-based model loading for deployment

## Amazon RDS

Used for:

- Storing detection metadata
- Recording violation details
- Maintaining safety analytics history

---

##  Chatbot Features

IntelliGuard includes an AI-powered SQL chatbot using LangChain and Gemini.

The chatbot allows users to query safety analytics using natural language.

Example queries:

- "How many helmet violations happened today?"
- "Show weekly mask violations"
- "Which detection source has the highest violations?"
- "How many total violations occurred?"

---

##  Evaluation Metrics

The system performance is evaluated using:

- mAP (Mean Average Precision)
- Precision and Recall
- Face Recognition Accuracy
- Detection Latency
- Chatbot Response Time
- Database Logging Accuracy
- Streamlit Application Performance

---

##  Email Alerts

The system automatically generates email notifications when safety violations are detected.

Examples:

- Missing helmet detection
- Missing mask detection
- Missing gloves
- PPE compliance violations

---

#  Application Screenshots

## 🔐 Secure Login Page

Face recognition and password authentication provide secure access.

<p align="center">
<img src="[screenshots/login_page.png](https://github.com/Joe-in-absentia/AI-Powered-PPE-Compliance-Monitoring-System/blob/29c584c91412c399b229a2dca949f858c2292c69/login.png)" width="850">
</p>


---

## 🛡️ IntelliGuard Dashboard

Main dashboard for selecting detection modes and viewing safety analytics.

<p align="center">
<img src="[https://github.com/Joe-in-absentia/AI-Powered-PPE-Compliance-Monitoring-System/blob/2f1ff059dfd5bb644f8f2ef58049cacfe427b97a/main.png)" width="850">
</p>


---

## 📡 Live Webcam Monitoring

Real-time PPE monitoring using YOLO detection.

<p align="center">
<img src="screenshots/webcam_detection.png" width="850">
</p>



---

##  Results

- Accurate PPE violation detection using YOLO
- Real-time workplace safety monitoring
- Cloud-based violation logging using AWS RDS
- Secure face-authenticated access
- AI-powered safety analytics chatbot
- Automated email reporting system
- Scalable cloud-ready architecture

---

## 🏭 Business Use Cases

- Real-time factory safety monitoring
- Automated PPE compliance auditing
- Reduction of manual inspection workload
- Safety analytics dashboard for management
- AI-based workplace decision support
- Industrial automation solutions

---

##  Conclusion

IntelliGuard delivers an end-to-end AI solution for workplace safety by combining computer vision, cloud computing, and generative AI.

The system automates PPE violation detection, cloud-based logging, reporting, and analytics while providing an intelligent chatbot interface for safety insights.

By reducing manual monitoring efforts and enabling real-time safety analysis, IntelliGuard helps organizations improve compliance, enhance workplace safety, and make data-driven decisions.

---
