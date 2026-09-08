
 Project Proposal – CNN-Based Face Recognition and Automated Student Attendance

# PROJECT PROPOSAL

 ## Project Title

 **CNN-Based Face Recognition System for Student Identification and Automated Attendance**

 ## 1\. Project Overview

 The **Student Management Portal** is being developed collaboratively by seven groups, with each group responsible for a specific module. Our team consists of **8 members** and is responsible for developing the **CNN-based Face Recognition System** using **Deep Learning and TensorFlow/Keras**.

 Our module will receive student information from the **Academic Team**. Using this information and the facial dataset of registered students, our system will recognize students entering the classroom through a camera.

 After successful recognition, the system will display the following four student details:

 - **Student Name**
- **TL ID**
- **Student ID**
- **Email ID**

 The recognized student information will then be passed to the **Object Detection Team**, which will use it for further **anomaly detection**. The attendance information will also be recorded and integrated with the Student Management Portal.

---

 # 2\. Objectives

 - Develop a CNN-based face recognition model using **TensorFlow/Keras**.
- Receive and organize student information provided by the **Academic Team**.
- Create a facial dataset corresponding to registered students.
- Recognize students entering the classroom in real time.
- Display **Student Name, TL ID, Student ID, and Email ID** after recognition.
- Automatically record attendance.
- Prevent duplicate attendance during the same session.
- Identify unknown/unregistered faces.
- Pass recognized student information to the **Object Detection Team** for anomaly detection.
- Integrate our module with the overall Student Management Portal.

---

 # 3\. Input Data

 Our team will receive two major types of input.

 ### A. Student Information from Academic Team

 The Academic Team will provide the required student information, such as:

```
Student Name
TL ID
Student ID
Email ID
Department/Class
```

 The **Student ID** will act as the primary identifier connecting the student's facial data with their academic information.

 ### B. Facial Dataset

 Facial images will be collected for registered students with appropriate permission and consent.

 Approximately **30–50 images per student** can be collected, including:

 - Front-facing images
- Slight left/right face angles
- Different expressions
- Different lighting conditions
- Different distances
- Normal appearance variations such as spectacles

 For example:

 **100 students × 40 images = 4,000 images**

 Dataset structure:

```
dataset/
├── STU001/
│   ├── image_001.jpg
│   ├── image_002.jpg
│   └── ...
├── STU002/
│   ├── image_001.jpg
│   └── ...
└── STU003/
    └── ...
```

 The facial dataset should contain only the information necessary for recognition, while Name, TL ID, and Email ID can be retrieved from the student database using the Student ID.

---

 # 4\. Methodology

 The system will be developed through the following stages:

 ### Step 1 – Receive Student Data

 Receive student information from the **Academic Team** and create the required student records.

 ### Step 2 – Facial Dataset Collection

 Collect and label student facial images using the corresponding Student ID.

 ### Step 3 – Preprocessing

 Use **OpenCV** to detect, crop, resize, and normalize facial images.

 ### Step 4 – Data Augmentation

 Apply suitable augmentation such as small rotations, brightness variations, and zooming to improve model robustness.

 ### Step 5 – Dataset Splitting

 Divide the dataset approximately into:

 - 70% Training
- 15% Validation
- 15% Testing

 A separate real-world classroom dataset will be used for final testing.

 ### Step 6 – CNN Model Development

 Develop a CNN-based face recognition model using **TensorFlow/Keras**.

 ### Step 7 – Model Training

 Train the model using the prepared facial dataset and evaluate its performance using validation data.

 ### Step 8 – Real-Time Face Recognition

 Connect the trained model to a webcam/IP camera. When a student enters the classroom, the system detects and recognizes their face.

 ### Step 9 – Student Information Retrieval

 After recognizing the student, the system uses the **Student ID** to retrieve the student's information from the student database.

 ### Step 10 – Display Student Information

 The system displays:

```
Student Name
TL ID
Student ID
Email ID
```

 along with the recognition/attendance status.

 ### Step 11 – Attendance Recording

 The system checks whether attendance has already been recorded for the current class session. If not, the student's attendance is marked with the date and time.

 ### Step 12 – Pass Information to Object Detection Team

 After recognition, the identified student's information is passed to the **Object Detection Team**.

 The Object Detection Team uses the information as part of its **anomaly detection process**.

 ### Step 13 – Final Integration

 Our module will be integrated with the other modules of the Student Management Portal.

---

 # 5\. System Architecture

 The overall interaction between the teams will be:

```
                 ┌─────────────────────┐
                 │    Academic Team    │
                 │                     │
                 │ Student Name        │
                 │ TL ID               │
                 │ Student ID          │
                 │ Email ID            │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Face Recognition    │
                 │       Team          │
                 │                     │
                 │ CNN + TensorFlow    │
                 │ OpenCV              │
                 └──────────┬──────────┘
                            │
                       Camera Input
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Face Detection    │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │   CNN Recognition   │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │     Student ID      │
                 └──────────┬──────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
       ┌──────────────────┐    ┌─────────────────┐
       │ Student Details  │    │   Attendance    │
       │                  │    │                 │
       │ Name             │    │ Date            │
       │ TL ID            │    │ Time            │
       │ Student ID       │    │ Status          │
       │ Email ID         │    └─────────────────┘
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────────┐
       │ Object Detection     │
       │ Team                 │
       │                      │
       │ Anomaly Detection    │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │ Student Management   │
       │ Portal               │
       └──────────────────────┘
```

---

 # 6\. JSON Architecture

```
{
  "system": "Student Management Portal",

  "teams": {
    "academic_team": {
      "provides": [
        "student_name",
        "tl_id",
        "student_id",
        "email_id"
      ]
    },

    "face_recognition_team": {
      "team_size": 8,
      "technology": [
        "Python",
        "TensorFlow",
        "Keras",
        "CNN",
        "OpenCV"
      ],

      "input": {
        "camera": "Webcam/IP Camera",
        "student_database": "Academic Team Data",
        "face_dataset": "Registered Student Facial Images"
      },

      "processing": [
        "Face Detection",
        "Face Preprocessing",
        "CNN Feature Learning",
        "Face Recognition",
        "Student ID Matching"
      ],

      "recognition_output": {
        "student_name": "Retrieved using Student ID",
        "tl_id": "Retrieved using Student ID",
        "student_id": "Recognized Student ID",
        "email_id": "Retrieved using Student ID"
      },

      "attendance": {
        "status": "Present",
        "date": "YYYY-MM-DD",
        "time": "HH:MM:SS",
        "duplicate_check": true
      },

      "output_to_object_detection_team": {
        "student_name": true,
        "tl_id": true,
        "student_id": true,
        "email_id": true,
        "recognition_status": true,
        "attendance_status": true
      }
    },

    "object_detection_team": {
      "input": [
        "student_name",
        "tl_id",
        "student_id",
        "email_id",
        "recognition_status"
      ],
      "process": "Anomaly Detection",
      "output": "Anomaly Status"
    }
  },

  "overall_flow": [
    "Academic Team",
    "Student Information",
    "Face Recognition",
    "Student Identification",
    "Display Student Details",
    "Attendance Recording",
    "Object Detection",
    "Anomaly Detection",
    "Student Management Portal"
  ]
}
```

---

 # 7\. Output After Face Recognition

 After a student's face is recognized, our module will produce an output similar to:

```
====================================
        STUDENT RECOGNIZED
====================================
Student Name : Rahul Kumar
TL ID        : TL1025
Student ID   : STU001
Email ID     : rahul@example.com
Attendance   : Present
Date         : 07-09-2026
Time         : 09:02:15
====================================
       SENT TO OBJECT DETECTION
====================================
```

 The four student details will be obtained from the **Academic Team's student database**, rather than storing personal information directly in the CNN model.

---

 # 8\. Technologies Used

 | Component | Technology |
| --- | --- |
| Programming | Python |
| Deep Learning | TensorFlow / Keras |
| Model | CNN |
| Face Detection | OpenCV |
| Data Processing | NumPy / Pandas |
| Database | MySQL/PostgreSQL |
| Communication | REST API |
| Camera | Webcam/IP Camera |

---

 # 9\. Team Division – 8 Members

 | Member | Responsibility |
| --- | --- |
| **1** | Team coordination, requirements, documentation, and communication with other teams |
| **2** | Receive/organize Academic Team data and manage facial dataset |
| **3** | Face detection and preprocessing using OpenCV |
| **4** | CNN architecture and TensorFlow/Keras implementation |
| **5** | Model training, augmentation, and optimization |
| **6** | Real-time face recognition and student information retrieval |
| **7** | Attendance system, API, and communication with Object Detection Team |
| **8** | Testing, accuracy evaluation, debugging, and deployment |

---

 # 10\. Expected Outcome

 Our team will deliver a **CNN-based real-time face recognition module** that:

 1. Receives student information from the Academic Team.
2. Captures students using a classroom camera.
3. Detects and recognizes their faces.
4. Retrieves and displays **Name, TL ID, Student ID, and Email ID**.
5. Automatically records attendance.
6. Prevents duplicate attendance.
7. Identifies unknown students.
8. Passes recognized student information to the **Object Detection Team**.
9. Supports the Object Detection Team's anomaly detection process.
10. Integrates with the overall Student Management Portal.

 ## 11\. Privacy and Security

 Student facial images and personal information must be collected and processed only with appropriate institutional permission and consent. Facial datasets should be securely stored and access should be restricted to authorized members. The CNN system should use the **Student ID as the link** to the academic database rather than unnecessarily storing personal information in the model.

 ## 12\. Conclusion

 The **CNN-Based Face Recognition System** will act as an important bridge between the **Academic Team, Object Detection Team, and Student Management Portal**. It will use TensorFlow/Keras and computer vision to recognize students entering the classroom, retrieve their academic information, display the required four details, record attendance, and pass the recognition result to the Object Detection Team for anomaly detection.

 This module will provide practical experience in **CNN, TensorFlow, computer vision, dataset preparation, real-time face recognition, API integration, attendance automation, and inter-team system integration**.
