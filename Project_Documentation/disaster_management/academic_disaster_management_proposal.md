# Project Proposal: AI-Powered Student Support & Smart Campus Intelligence System
## Sub-Module: Academic Disaster Management & Early Warning Anomaly Detection Engine (ADM-EWS)

---

### Document Information
- **Project Domain:** Deep Learning, Time-Series Anomaly Detection, Intelligent Campus Automation
- **Parent Project:** AI-Powered Student Support and Smart Campus Intelligence System
- **Sub-System Title:** Academic Disaster Management & Predictive Early Warning Engine
- **Target Deployment:** Cloud / On-Premise Campus Server (Google Colab for Training, GitHub for VCS)
- **Document Version:** 1.0.0
- **Status:** Proposed

---

## 1. Executive Summary

In higher education institutions, academic attrition, sudden drops in engagement, and semester exam debarment due to attendance shortages (e.g., falling below the statutory 75% minimum) often occur as preventable crises. Traditional campus management portals operate reactively: students and faculty are only notified after attendance records or continuous assessment marks cross critical thresholds, leaving little to no time for corrective intervention.

The **Academic Disaster Management & Early Warning System (ADM-EWS)** module serves as the campus intelligence backbone. Utilizing deep learning time-series architectures (LSTM Autoencoders and Gated Recurrent Units), this module continuously monitors temporal behavioral trends, internal evaluation scores, and vision-based attendance logs. It identifies anomalous patterns weeks before they escalate into irreversible academic debarment, automatically dispatching structured payloads to the **Chatbot Team** (for parental/student alerts) and the **Academic Team** (for faculty intervention dashboards).

---

## 2. Problem Statement & Motivation

Existing academic management systems suffer from three primary bottlenecks:
1. **Threshold-Only Notifications:** Conventional systems use static logic (`if attendance < 75%`). By the time this rule triggers in week 11 or 12, a student cannot mathematically recover the deficit before final university exams.
2. **Behavioral Drift Ignorance:** Erratic behavior—such as a student with historical 90% attendance suddenly missing consecutive laboratory sessions or key morning lectures—is overlooked if their aggregate metric is temporarily above the threshold.
3. **Siloed Multimodal Signals:** Discrepancies between computer vision attendance data (captured by classroom cameras) and manual or RFID attendance logs are not cross-validated, allowing proxy attendance or camera blind-spot errors to propagate undetected.

The ADM-EWS module solves these challenges by transforming raw multimodal time-series records into actionable, predictive intelligence.

---

## 3. Scope & Objectives

### 3.1 Primary Objectives
- **Unsupervised Behavioral Anomaly Detection:** Train an LSTM Autoencoder on nominal student attendance and submission time-series data to detect abnormal deviations via reconstruction error spikes.
- **Predictive Trajectory Forecasting:** Implement a sequence-to-sequence GRU/TCN model that forecasts end-of-semester attendance and internal evaluation trajectories at weeks 4, 8, and 12 with over 85% predictive accuracy.
- **Vision Cross-Validation Engine:** Reconcile spatial face-recognition attendance logs from the Vision Team against physical logs to isolate anomalies such as unauthorized absence or proxy entries.
- **Real-Time Inter-Module Dispatcher:** Construct asynchronous webhook endpoints to dispatch risk alerts with confidence metrics to the Campus Chatbot and Academic Management Portals.

---

## 4. System Architecture & Methodology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Data Ingestion Layer                           │
│  [Vision Team Face Logs]   [Academic SIS Marks]   [LMS Portal Activity] │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 Temporal Feature Engineering Pipeline                   │
│   • Rolling 7-day/14-day attendance rate   • Z-score normalized internals│
│   • Slot-specific absence vector           • Submission latency delta   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Deep Learning Anomaly Core                          │
│                                                                         │
│   ┌──────────────────────────────┐    ┌─────────────────────────────┐   │
│   │   LSTM Autoencoder Engine    │    │  Bidirectional GRU Predictor│   │
│   │  (Reconstruction Anomaly)    │    │  (Debarment Trajectory)     │   │
│   └──────────────┬───────────────┘    └──────────────┬──────────────┘   │
└──────────────────┼───────────────────────────────────┼──────────────────┘
                   │                                   │
                   ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Risk Matrix & Decision Arbiter                      │
│   • LOW RISK: Advisory logged to Student Profile                        │
│   • MEDIUM RISK: Alert queued for Academic Advisor Mentorship           │
│   • CRITICAL RISK: Immediate escalation trigger                         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Inter-Module Payload Dispatcher                      │
│            ├──> Chatbot Team (Automated Parent/Student SMS)             │
│            └──> Academic Team (Faculty Remedial Dashboard)              │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Deep Learning Models
1. **LSTM Autoencoder (Unsupervised Anomaly Detection):**
   - Encodes a sliding window $W_t = [x_{t-k}, \dots, x_t]$ into a latent space representation and reconstructs it.
   - Reconstruction error is computed using Mean Squared Error (MSE):
     $$L_{recon} = \frac{1}{N} \sum_{i=1}^N (x_i - \hat{x}_i)^2$$
   - Sequences where $L_{recon} > \mu + 3\sigma$ are tagged as behavioral anomalies.
2. **Bidirectional GRU Trajectory Predictor (Supervised Forecasting):**
   - Inputs past weekly metrics to output the estimated end-of-semester attendance percentage $\hat{A}_{final}$ and failure probability $P(Debarment)$.
3. **Cross-Entropy Discrepancy Filter:**
   - Evaluates confidence scores from the Vision Team against physical logs to calculate proxy probability.

---

## 5. Inter-Team Integration & API Contracts

The module emits structured JSON alerts whenever an anomaly threshold is breached.

### Outbound Alert Schema (To Chatbot & Academic Teams)
```json
{
  "event_id": "EVT-2026-09-8831",
  "timestamp": "2026-09-07T10:30:00Z",
  "student_details": {
    "student_id": "STU2024CS089",
    "department": "Computer Science & Engineering",
    "semester": 5
  },
  "risk_assessment": {
    "risk_level": "CRITICAL",
    "anomaly_type": "PROJECTED_EXAM_DEBARMENT",
    "anomaly_confidence": 0.924,
    "root_causes": [
      "Consecutive absence in Subject CS301 (3 sessions)",
      "Current attendance 76.2% with projected trajectory 67.8%"
    ]
  },
  "metrics": {
    "current_attendance_pct": 76.2,
    "projected_end_sem_pct": 67.8,
    "minimum_statutory_pct": 75.0,
    "days_to_irreversible_limit": 4
  },
  "target_routing": {
    "notify_chatbot": true,
    "notify_academic_advisor": true,
    "chatbot_action": "TRIGGER_PARENT_EMERGENCY_ALERT",
    "portal_action": "HIGHLIGHT_ON_FACULTY_CONSOLE"
  }
}
```

---

## 6. Team Structure & Role Allocation (7 Members)

To ensure seamless execution, responsibilities are partitioned cleanly across data pipelines, core deep learning modeling, system integration, and evaluation:

| Member | Designated Role | Core Responsibilities | Primary Deliverables |
| :--- | :--- | :--- | :--- |
| **Member 1** | **Team Lead & System Architect** | System integration, cross-team API negotiation (Vision/Chatbot/Academic), GitHub repo setup & CI/CD workflow. | System design doc, API endpoints, orchestration pipeline. |
| **Member 2** | **Data Engineering & Synthesis Specialist** | Synthetic time-series generation (handling cold-start & class imbalance), temporal windowing, data validation. | Clean dataset generators, feature engineering notebooks (`data_pipeline.py`). |
| **Member 3** | **Deep Learning Engineer (Autoencoders)** | Designing, tuning, and validating the LSTM Autoencoder for unsupervised behavioral anomaly detection. | PyTorch/TensorFlow LSTM Autoencoder model (`model_autoencoder.py`). |
| **Member 4** | **Deep Learning Engineer (Trajectory Forecasting)** | Designing the Bidirectional GRU / Temporal CNN for predictive exam debarment forecasting. | Trajectory forecasting model and loss convergence benchmarks (`model_gru.py`). |
| **Member 5** | **Vision Cross-Validation & Anomaly Filter** | Reconciling classroom camera detection vectors against manual records; proxy anomaly identification. | Reconciliation heuristic engine and discrepancy filter module. |
| **Member 6** | **API & Webhook Engineer** | Developing FastAPI backend services, webhook dispatchers, and queue handling for the Chatbot team. | FastAPI microservice (`main.py`), Swagger docs, response caching. |
| **Member 7** | **Evaluation, Benchmarking & Documentation** | Model validation (ROC-AUC, Precision-Recall, inference latency), Colab notebook documentation, final project report. | Model performance reports, Colab verification suite, viva slide deck. |

---

## 7. Tech Stack & Collaboration Framework

- **Core Deep Learning Framework:** PyTorch / TensorFlow 2.x, Scikit-learn
- **Data Manipulation & Time-Series:** Pandas, NumPy, Scipy
- **API & Serving Microservice:** FastAPI, Pydantic, Uvicorn
- **Development & Hardware Acceleration:** Google Colab (Nvidia T4/V100 GPU runtimes)
- **Version Control & Collaboration:** GitHub (Feature-branch workflow, Pull Requests, Git LFS for `.pt` / `.h5` model checkpoints)
- **Environment Management:** Python 3.10+, `requirements.txt`, Docker (optional deployment container)

---

## 8. Implementation Roadmap & Milestones

```
Week 01 - 02: Requirements Finalization & Synthetic Academic Dataset Generation
Week 03 - 04: Exploratory Data Analysis (EDA) & Feature Extraction Pipelines
Week 05 - 07: LSTM Autoencoder & GRU Trajectory Model Architecture Development (Colab)
Week 08 - 09: Cross-Validation with Vision Logs & Threshold Calibration (F1-score optimization)
Week 10 - 11: FastAPI Microservice Integration with Chatbot & Academic Modules
Week 12 - 13: End-to-End System Stress Testing, Latency Benchmarking & Final Documentation
```

---

## 9. Evaluation Metrics & Success Criteria

The module will be evaluated across two paradigms:

1. **Anomaly Detection Precision & Sensitivity:**
   - **Precision & Recall ($F_{\beta}$ score with $\beta=2$):** Optimized to minimize false negatives (failing to flag a debarred student is penalized heavily).
   - **Area Under the ROC Curve (AUC-ROC):** Target $\ge 0.88$ on historical debarment validation sets.
2. **Trajectory Prediction Accuracy:**
   - **Mean Absolute Percentage Error (MAPE):** Target $< 6.5\%$ on 4-week lookahead end-sem attendance forecasting.
3. **Inference & Dispatch Latency:**
   - Inference turnaround time $< 150\text{ ms}$ per batch request from the academic ingestion queue.

---

## 10. Repository Structure (GitHub Guidelines)

```
ai-campus-disaster-management/
├── .github/workflows/          # CI/CD test automation
├── data/
│   ├── raw/                    # Anonymized / synthetic raw logs
│   └── processed/              # Normalized temporal sliding windows
├── notebooks/                  # Google Colab experimentation notebooks
│   ├── 01_eda_and_synthesis.ipynb
│   ├── 02_lstm_autoencoder_training.ipynb
│   └── 03_gru_trajectory_forecasting.ipynb
├── src/
│   ├── __init__.py
│   ├── data_pipeline.py        # Feature extraction & rolling aggregates
│   ├── models/
│   │   ├── autoencoder.py      # PyTorch Autoencoder definition
│   │   └── trajectory_gru.py   # PyTorch GRU forecasting definition
│   ├── discrepancy_filter.py   # Vision reconciliation logic
│   └── api/
│       ├── main.py             # FastAPI service
│       └── schemas.py          # Pydantic data schemas
├── tests/                      # Unit and integration test suites
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation & execution guide
```

---
*Submitted by: Sub-Module Team 4 (Disaster Management & Anomaly Detection)*  
*Department of Computer Science & Engineering*
