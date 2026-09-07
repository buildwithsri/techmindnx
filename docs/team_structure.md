# Team Structure & Department Governance

## 1. Leadership & Organizational Hierarchy

```mermaid
graph TD
    PL[Project Lead / Chief Architect]
    
    subgraph Departments ["Specialized Engineering Tracks"]
        D1[01 Support Intelligence Team]
        D2[02 Academic Evaluation Team]
        D3[03 Face Recognition Team]
        D4[04 Disaster Management Team]
        D5[05 Object Detection Team]
        D6[06 AI Engineering & MLOps Team]
        D7[07 Testing & QA Benchmark Team]
    end
    
    PL --> D1
    PL --> D2
    PL --> D3
    PL --> D4
    PL --> D5
    PL --> D6
    PL --> D7
```

---

## 2. Department Mandates & Responsibilities

| Module / Track | Primary Focus | Key Responsibilities |
| :--- | :--- | :--- |
| **00 Project Management** | Cross-team coordination | Repository governance, roadmap tracking, code review coordination, release management. |
| **01 Support Intelligence** | NLP & Conversational AI | Query classification, student ticket routing, attendance risk escalation logic, chatbot API. |
| **02 Academic Evaluation** | Predictive ML Analytics | Student trajectory modeling, grade forecasting, weak area diagnostic algorithms. |
| **03 Face Recognition** | Biometric Computer Vision | Face detection, embedding generation, contactless attendance logging, CCTV stream processing. |
| **04 Disaster Management** | Anomaly & Crisis Detection | ADM-EWS engine, anomaly detection for retention drops, bulk academic failure early warning. |
| **05 Object Detection** | Vision Surveillance | Spatial resource utilization, classroom occupancy counting, facility and perimeter monitoring. |
| **06 AI Engineering** | MLOps & Distributed Serving | FastAPI prediction gateway, MLflow model tracking, drift detection, containerization. |
| **07 Testing & QA** | Verification & Benchmarking | Test suite implementation (unit/integration), dataset validation, latency profiling, QA sign-off. |

---

## 3. Communication & Code Review Protocols
- **Daily / Weekly Syncs**: Department leads sync on interface definitions and schema updates.
- **Code Ownership**: Module code must be reviewed by the assigned CODEOWNER before merging into `main`.
- **Cross-Team Dependencies**: Any API schema modifications must be communicated to the AI Engineering (`06`) and Testing (`07`) teams.
