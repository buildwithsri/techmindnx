# Testing & QA Test Suite (`tests/`)

This directory contains automated test suites for the entire platform.

### Structure:
```text
tests/
├── unit/
│   ├── test_support_intelligence.py
│   ├── test_academic_evaluation.py
│   ├── test_face_recognition.py
│   ├── test_disaster_management.py
│   ├── test_object_detection.py
│   └── test_ai_engineering.py
├── integration/
│   └── test_api_gateway.py
└── performance/
    └── locustfile.py
```

### Running Tests:
```bash
pytest tests/ -v
```
