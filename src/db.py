# db_manager.py
import os
from datetime import date
from supabase import create_client
from dotenv import load_dotenv

# loading environment variables 
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url,key)

# Create Task
def create_user(name, email, password, age, height, weight, gender, activity_level, goal, diet_preference):
    return supabase.table("Users").insert({
        "name": name,
        "email": email,
        "password": password,
        "age": age,
        "height": height,
        "weight": weight,
        "gender": gender,
        "activity_level": activity_level,
        "goal": goal,
        "diet_preference": diet_preference
    }).execute()

def get_user_by_email(email):
    return supabase.table("Users").select("*").eq("email", email).execute()

# ---------------- MEALS ----------------
def add_meal(name, calories, protein, carbs, fats, diet_type, meal_time, image_url):
    return supabase.table("Meals").insert({
        "name": name,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fats": fats,
        "diet_type": diet_type,
        "meal_time": meal_time,
        "image_url": image_url
    }).execute()

# ---------------- MEAL PLANS ----------------
def create_meal_plan(user_id, plan_type, date, total_calories, water_recommendation, step_recommendation):
    return supabase.table("MealPlans").insert({
        "user_id": user_id,
        "plan_type": plan_type,
        "date": date,
        "total_calories": total_calories,
        "water_recommendation": water_recommendation,
        "step_recommendation": step_recommendation
    }).execute()

def add_meal_to_plan(plan_id, meal_id):
    return supabase.table("MealPlanMeals").insert({
        "plan_id": plan_id,
        "meal_id": meal_id
    }).execute()

def get_user_meal_plans(user_id):
    return supabase.table("MealPlans").select("*").eq("user_id", user_id).execute()
