from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import joblib
import numpy as np
import os

# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "survey_lung_cancer.joblib")

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"❌ Model file not found at {MODEL_PATH}. Please make sure 'survey_lung_cancer.joblib' is in the same folder.")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    raise RuntimeError(f"❌ Failed to load model: {e}")


app = FastAPI(
    title="Lung Cancer Prediction API",
    version="1.0",
    description="Predicts lung cancer risk based on user inputs"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 0 = NO, 1 = YES
# 0 = Female, 1 = Male
class LungCancerInput(BaseModel):
    GENDER: int = Field(..., ge=0, le=1, description="1 for Male, 0 for Female")
    AGE: int = Field(..., gt=0, lt=120, description="Patient's age")
    

    SMOKING: int = Field(..., ge=0, le=1)
    YELLOW_FINGERS: int = Field(..., ge=0, le=1)
    ANXIETY: int = Field(..., ge=0, le=1)
    PEER_PRESSURE: int = Field(..., ge=0, le=1)
    CHRONIC_DISEASE: int = Field(..., ge=0, le=1)
    FATIGUE: int = Field(..., ge=0, le=1)
    ALLERGY: int = Field(..., ge=0, le=1)
    WHEEZING: int = Field(..., ge=0, le=1)
    ALCOHOL_CONSUMING: int = Field(..., ge=0, le=1)
    COUGHING: int = Field(..., ge=0, le=1)
    SHORTNESS_OF_BREATH: int = Field(..., ge=0, le=1)
    SWALLOWING_DIFFICULTY: int = Field(..., ge=0, le=1)
    CHEST_PAIN: int = Field(..., ge=0, le=1)

    @field_validator("*", mode="before")
    @classmethod
    def check_empty(cls, v):
        if v is None or v == "":
            raise ValueError("Field cannot be empty")
        return v

# ==============================


@app.get("/")
def home():
    return {"message": "Lung Cancer Prediction API is Running!"}

@app.post("/predict")
def predict_cancer(data: LungCancerInput):
    try:

        input_data = list(data.model_dump().values())

        features = np.array([input_data])

        prediction = model.predict(features)[0]
        

        result_text = "LUNG CANCER DETECTED" if prediction == 1 else "NO LUNG CANCER DETECTED"

        return {
            "prediction_code": int(prediction),
            "result": result_text,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))