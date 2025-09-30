# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys, os

# Add project root to path so 'src' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic import MealPlanManager
from src.db import register_user, login_user, get_user_by_email, get_meals_by_preference

# ---------------- App Setup -----------------
app = FastAPI(title="NutriGuide API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mealplan_manager = MealPlanManager()

# ----------------- Models -----------------
class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    age: int
    height: float
    weight: float
    gender: str
    activity_level: str
    goal: str
    diet_preference: str

class LoginUser(BaseModel):
    email: str
    password: str

class PlanRequest(BaseModel):
    email: str

# ----------------- Endpoints -----------------

@app.get("/")
def home():
    return {"message": "NutriGuide API is running"}

# ----------- User Endpoints -----------------
@app.post("/register")
def register_api(user: RegisterUser):
    existing = get_user_by_email(user.email)
    if existing and existing.data:
        raise HTTPException(status_code=400, detail="User already exists")

    res = register_user(**user.dict())
    if not res or not res.data:
        raise HTTPException(status_code=400, detail="Registration failed")
    return {"success": True, "message": "User registered successfully"}

@app.post("/login")
def login_api(user: LoginUser):
    user_data = login_user(user.email, user.password)
    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"success": True, "user": user_data}

# ----------- Meal Plan Endpoints -----------------
@app.post("/plan/daily")
def daily_plan_api(request: PlanRequest):
    user_resp = get_user_by_email(request.email)
    if not user_resp or not user_resp.data:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_resp.data[0]

    plan = mealplan_manager.generate_daily_plan(user)
    if not plan["success"]:
        raise HTTPException(status_code=400, detail=plan.get("message"))
    return plan

@app.post("/plan/weekly")
def weekly_plan_api(request: PlanRequest):
    user_resp = get_user_by_email(request.email)
    if not user_resp or not user_resp.data:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_resp.data[0]

    plan = mealplan_manager.generate_weekly_plan(user)
    if not plan["success"]:
        raise HTTPException(status_code=400, detail=plan.get("message"))
    return plan

# ---------------- Run Server -----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
