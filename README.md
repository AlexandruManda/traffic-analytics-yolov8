# traffic-analytics-yolov8
This project implements a real-time traffic analysis system using YOLOv8, leveraging advanced computer vision and machine learning techniques. The system enables vehicle detection, speed estimation, and pedestrian counting in real-time from various video sources such as webcams, YouTube links, UDP streams, and RTSP streams.

## Features
- Traffic Counting: Counts total vehicles and tracks specific traffic flow through dynamic line counting.
- Speed Estimation: Tracks vehicle speeds using frame-to-frame analysis.
- Pedestrian Counting: Detects and counts individuals in real-time.
- Source Input: Supports YouTube links, uploaded videos, UDP streams, and RTSP protocols.

## Dataset and Model
This project utilizes a custom dataset annotated in [Roboflow](https://universe.roboflow.com/car-detection-smznf/highway-cars-object-detection). 
- Roboflow simplifies dataset creation with features like sampling frames from videos and assisted annotation tools.

<a href="https://universe.roboflow.com/car-detection-smznf/highway-cars-object-detection">
    <img src="https://app.roboflow.com/images/download-dataset-badge.svg"></img>
</a>

<a href="https://universe.roboflow.com/car-detection-smznf/highway-cars-object-detection/model/">
    <img src="https://app.roboflow.com/images/try-model-badge.svg"></img>
</a>

## Architecture
The project follows a modular architecture that includes:
- **YOLOv8 Integration:** For real-time object detection and tracking.
- **Flask Backend:** Handles YOLO inferences and supports dynamic tracker parameter updates via MongoDB.
- **React Frontend:** User interface for media uploads, streaming, and displaying results.
- **Docker:** Ensures scalability and consistent deployment across environments.

### System Workflow
1. Upload a video or provide a stream link.
2. The backend processes the media using YOLOv8 and sends annotated frames.
3. Results are displayed in the frontend with live updates.

### Key Technologies
- YOLOv8: Fast, accurate object detection.
- MongoDB: Real-time updates for tracker parameters.
- Flask and React: Seamless backend and frontend communication.

### Architecture Diagram
Below is an architecture diagram showcasing the system's modular design:

![image](https://github.com/user-attachments/assets/aa342058-ec40-417d-9415-6e23b7f4e8b1)

## Performance and Results
The system is optimized for GPU processing using CUDA, significantly outperforming CPU-based solutions. Detailed comparisons and benchmarks demonstrate its real-time processing capability, even for large datasets.

### Sample Results
- **Vehicle Detection:**
  - Total Vehicle Count: Accurate classification and counting across multiple classes (cars, trucks, motorcycles, buses).
  - Speed Estimation: Real-time tracking and speed calculation.

- **Pedestrian Detection:**
  - Total Person Count: Provides a live count of individuals in the frame.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Start the application:
   ```bash
    docker-compose up

## Demo

https://github.com/user-attachments/assets/94ec153d-ec28-45c8-8b96-a93064a9f0ee



