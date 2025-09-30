import os
from datetime import date
from supabase import create_client
from dotenv import load_dotenv

# ---------------- LOAD ENV VARIABLES ----------------
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- USERS ----------------
def register_user(name, email, password, age, height, weight, gender, activity_level, goal, diet_preference):
    """Register a new user in Supabase users table"""
    try:
        res = supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": password,  # ⚠️ Hash in production
            "age": age,
            "height": height,
            "weight": weight,
            "gender": gender,
            "activity_level": activity_level,
            "goal": goal,
            "diet_preference": diet_preference
        }).execute()
        return res
    except Exception as e:
        print("Supabase Error (register_user):", e)
        return None


def login_user(email, password):
    """Login user by verifying email + password"""
    try:
        user = supabase.table("users").select("*").eq("email", email).execute()
        if user.data and user.data[0]["password"] == password:
            return user.data[0]
        return None
    except Exception as e:
        print("Supabase Error (login_user):", e)
        return None


def get_user_by_email(email):
    try:
        return supabase.table("users").select("*").eq("email", email).execute()
    except Exception as e:
        print("Supabase Error (get_user_by_email):", e)
        return None


# ---------------- MEALS ----------------
def add_meal(name, calories, protein, carbs, fats, diet_type, meal_time, image_url=None, instructions=None):
    """Add a new meal (with optional image + instructions)"""
    try:
        return supabase.table("meals").insert({
            "name": name,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
            "diet_type": diet_type,
            "meal_time": meal_time,  # breakfast, lunch, snacks, dinner
            "image_url": image_url,
            "instructions": instructions
        }).execute()
    except Exception as e:
        print("Supabase Error (add_meal):", e)
        return None


def get_all_meals():
    try:
        return supabase.table("meals").select("*").order("meal_id").execute()
    except Exception as e:
        print("Supabase Error (get_all_meals):", e)
        return None


def get_meals_by_preference(diet_type):
    try:
        return supabase.table("meals").select("*").eq("diet_type", diet_type).execute()
    except Exception as e:
        print("Supabase Error (get_meals_by_preference):", e)
        return None


def get_unique_meals_for_day(diet_type):
    """
    Get 4 unique meals (breakfast, lunch, snacks, dinner)
    according to diet preference
    """
    try:
        res = supabase.table("meals").select("*").eq("diet_type", diet_type).execute()
        if not res.data:
            return []

        meals = res.data
        plan = {}
        used_ids = set()

        # Ensure uniqueness by filtering
        for meal_time in ["breakfast", "lunch", "snacks", "dinner"]:
            for m in meals:
                if m["meal_time"] == meal_time and m["meal_id"] not in used_ids:
                    plan[meal_time] = m
                    used_ids.add(m["meal_id"])
                    break

        return plan
    except Exception as e:
        print("Supabase Error (get_unique_meals_for_day):", e)
        return {}


# ---------------- MEAL PLANS ----------------
def create_meal_plan(user_id, plan_type, plan_date=None, total_calories=None, water_recommendation=None, step_recommendation=None):
    """Create a new daily/weekly plan for user"""
    try:
        if plan_date is None:
            plan_date = date.today()
        res = supabase.table("mealplans").insert({
            "user_id": user_id,
            "plan_type": plan_type,
            "date": plan_date,
            "total_calories": total_calories,
            "water_recommendation": water_recommendation,
            "step_recommendation": step_recommendation
        }).execute()
        return res
    except Exception as e:
        print("Supabase Error (create_meal_plan):", e)
        return None


def add_meal_to_plan(plan_id, meal_id):
    try:
        return supabase.table("mealplanmeals").insert({
            "plan_id": plan_id,
            "meal_id": meal_id
        }).execute()
    except Exception as e:
        print("Supabase Error (add_meal_to_plan):", e)
        return None


def get_user_meal_plans(user_id, plan_type=None):
    try:
        query = supabase.table("mealplans").select("*").eq("user_id", user_id)
        if plan_type:
            query = query.eq("plan_type", plan_type)
        return query.execute()
    except Exception as e:
        print("Supabase Error (get_user_meal_plans):", e)
        return None


# ---------------- HEALTH UTILS ----------------
def calculate_bmi(height_cm, weight_kg):
    """Calculate BMI and weight category"""
    try:
        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 1)

        if bmi < 18.5:
            status = f"Underweight (BMI {bmi}) - You may need to gain weight"
        elif 18.5 <= bmi < 24.9:
            status = f"Normal (BMI {bmi}) - Healthy weight"
        elif 25 <= bmi < 29.9:
            status = f"Overweight (BMI {bmi}) - Consider losing weight"
        else:
            status = f"Obese (BMI {bmi}) - Weight loss recommended"

        return bmi, status
    except Exception as e:
        print("Error (calculate_bmi):", e)
        return None, "Error calculating BMI"


def calculate_water_intake(weight_kg):
    """Water intake in liters (35 ml per kg)"""
    try:
        water_ml = weight_kg * 35
        water_l = round(water_ml / 1000, 2)
        return water_ml, water_l
    except Exception as e:
        print("Error (calculate_water_intake):", e)
        return None, None
