# Microservices Directory (`services/`)

This directory houses the independent FastAPI / Flask microservices for each module.

```text
services/
├── 01_support_intelligence/
├── 02_academic_evaluation/
├── 03_face_recognition/
├── 04_disaster_management/
├── 05_object_detection/
├── 06_ai_gateway/
└── common/
```

Each service should maintain its own `main.py`, `schemas.py`, `requirements.txt`, and `Dockerfile`.
