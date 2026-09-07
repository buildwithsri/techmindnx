# Coding Standards & Style Guide

To ensure consistency, readability, and maintainability across all sub-modules, all contributors must adhere to these standards.

---

## 1. Python Style Guide

- **Standard**: Follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- **Formatter**: Use `black` (line length: 88 characters) and `isort` for import sorting.
- **Linter**: Use `flake8` or `ruff`.

### Type Annotations
All function signatures and class methods must include Python 3.10+ type hints:
```python
from typing import List, Dict, Optional

def compute_risk_score(
    attendance_rate: float,
    gpa: float,
    assessment_history: List[float]
) -> Dict[str, float]:
    """Calculates student academic disaster risk score.
    
    Args:
        attendance_rate: Percentage attendance (0.0 to 1.0).
        gpa: Current cumulative GPA (0.0 to 4.0).
        assessment_history: List of recent test scores.
        
    Returns:
        Dictionary containing overall risk probability and factor weights.
    """
    ...
```

---

## 2. API Design & FastAPI Conventions

- **RESTful Endpoints**: Use nouns for resources, HTTP verbs for operations (`POST /api/v1/predictions/academic`).
- **Pydantic Schemas**: All request and response bodies must be validated with Pydantic v2 models in `schemas.py`.
- **Error Handling**: Use standard `HTTPException` with meaningful status codes (`400`, `404`, `422`, `500`) and structured JSON error responses.

---

## 3. Machine Learning & Deep Learning Standards

- **Reproducibility**: Always set random seeds at the top of training scripts:
  ```python
  import random, numpy as np, torch
  torch.manual_seed(42)
  np.random.seed(42)
  random.seed(42)
  ```
- **Model Checkpoints**:
  - Never commit binary model weights (`.pt`, `.h5`, `.onnx`) directly to Git.
  - Save weights to an S3/GCS bucket or local `models/checkpoints/` (which is excluded in `.gitignore`).
  - Log model artifacts via MLflow.
- **Tensors & GPU Acceleration**:
  - Code must dynamically handle CPU/CUDA device allocation:
  ```python
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  ```

---

## 4. Testing Standards

- All services must have unit tests in `tests/` using `pytest`.
- Target minimum test coverage: **75%** for business logic and data transformation utilities.
- Test files must be named `test_<module_name>.py`.
