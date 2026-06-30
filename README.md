# 🛡️ Intelliguard: AI-Powered PPE Compliance Monitoring System

## 📌 Overview
Intelliguard is an AI-based workplace safety monitoring system designed to detect Personal Protective Equipment (PPE) compliance in real time using computer vision and deep learning. It identifies safety violations from image/video feeds, logs anomalies into AWS cloud database, and provides an intelligent dashboard with secure login and a chatbot for querying safety insights.

##  Problem Statement
Industrial and manufacturing environments require strict safety compliance. Manual monitoring is inefficient, inconsistent, and not scalable.

This system automates safety monitoring by:
- Detecting PPE violations (helmet, gloves, mask, etc.)
- Processing image/video streams in real time
- Logging violations into cloud database (AWS RDS)
- Providing AI-based insights through chatbot interface

##  Key Features
- Real-time PPE violation detection using YOLO
- Face recognition-based secure login system
- Streamlit interactive dashboard
- AWS S3 integration for model storage
- AWS RDS for violation logging
- LangChain SQL chatbot for natural language queries
- Email alert automation using SMTP
- CSV export for violation reports
- TensorBoard logging for training metrics

##  Skills Gained
- Computer Vision with OpenCV & YOLO
- Object Detection & Model Fine-tuning
- Face Recognition Authentication
- Streamlit App Development
- AWS (S3, RDS) Integration
- NLP with LLMs & LangChain Agents
- SQL-based chatbot system
- SMTP Email Automation
- TensorBoard Experiment Tracking
- End-to-end AI system development

## 🏗️ Domain
- Industrial Safety & Compliance
- Manufacturing Automation
- AI in Workplace Monitoring
- Computer Vision + NLP Integration

## ⚙️ System Workflow
1. Input: Image / Video / Webcam feed
2. YOLO model detects PPE objects and violations
3. OpenCV processes frames
4. Violations stored in AWS RDS
5. Streamlit dashboard displays results
6. Email alerts sent automatically
7. LangChain chatbot allows SQL-based querying

## 🧪 Dataset
PPE Safety Dataset

Classes:
['glove', 'goggles', 'helmet', 'mask', 'no-suit', 'no_glove',
 'no_goggles', 'no_helmet', 'no_mask', 'no_shoes', 'shoes', 'suit']

Data Details:
- Industrial worker images with PPE/non-PPE scenarios
- YOLO format bounding box annotations
- Train/Validation/Test split applied
- Preprocessing includes resizing and normalization

## ☁️ AWS Architecture
- S3 Bucket → Stores trained YOLO model
- RDS Database → Stores violation logs and metadata

##  Chatbot Features
LangChain SQL agent allows natural language queries such as:
- "How many helmet violations today?"
- "Show weekly mask violations"
- "Which shift has highest violations?"

##  Evaluation Metrics
- mAP (Mean Average Precision)
- Precision & Recall
- Face recognition accuracy
- Detection latency
- Chatbot response time
- Database logging accuracy
- Streamlit UI performance

##  Email Alerts
System automatically sends email notifications when violations are detected:
- Helmet missing
- Mask missing
- Safety gear violations

##  Results
- High-accuracy PPE detection using YOLO
- Real-time monitoring system
- Structured violation logging in AWS RDS
- Secure face-authenticated access
- AI-powered chatbot for analytics
- Automated reporting system

##  Business Use Cases
- Real-time factory safety monitoring
- Automated compliance auditing
- Reduction in manual inspection effort
- Safety analytics dashboard for management
- AI-based decision support system

##  conclusion
Intelliguard delivers an end-to-end AI solution for workplace safety by combining computer vision, cloud computing, and generative AI. It automates PPE violation detection, logging, and reporting while providing an intelligent chatbot interface for insights. This system improves safety compliance, reduces manual monitoring, and enables real-time decision-making in industrial environments.

