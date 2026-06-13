# CI/CD Pipeline Demo with GitHub Actions

![CI Pipeline](https://github.com/OmPatkar04/cicd-pipeline-demo/actions/workflows/ci.yml/badge.svg)
![CD Pipeline](https://github.com/OmPatkar04/cicd-pipeline-demo/actions/workflows/cd.yml/badge.svg)

A FastAPI application with fully automated CI/CD pipeline using GitHub Actions.

## 🚀 Pipeline Overview

Every push to main branch triggers:
1. ✅ **18 automated tests** with pytest
2. ✅ **Code quality check** with Flake8
3. ✅ **Security scan** with Safety
4. ✅ **Auto-deployment** to Render.com

## 📁 Project Structure
cicd-pipeline-demo/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Test, Lint, Security
│       └── cd.yml          # Auto-deploy
├── app/
│   ├── main.py             # FastAPI application
│   ├── test_main.py        # 18 automated tests
│   └── requirements.txt
├── Dockerfile
└── README.md

## 🛠 Tech Stack
- **Backend:** Python + FastAPI
- **Testing:** Pytest (18 tests)
- **Linting:** Flake8
- **Security:** Safety
- **CI/CD:** GitHub Actions
- **Container:** Docker
- **Deploy:** Render.com

## 📊 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API info |
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| POST | /tasks | Create task |
| GET | /tasks/{id} | Get task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |
| GET | /stats | Task statistics |

## 🏃 Run Locally
git clone https://github.com/OmPatkar04/cicd-pipeline-demo.git
cd cicd-pipeline-demo
python -m venv venv
venv\Scripts\activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload

## 🧪 Run Tests
cd app
pytest test_main.py -v

## 🐳 Run with Docker
docker build -t cicd-demo .
docker run -p 8000:8000 cicd-demo