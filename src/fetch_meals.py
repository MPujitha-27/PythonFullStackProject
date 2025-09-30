# src/fetch_meals.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# ---------- LOAD ENV VARIABLES ----------
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- ASSIGN MEALS TO EXISTING MEAL PLANS ----------
def assign_meals_to_plans():
    try:
        # Fetch all users
        users = supabase.table("users").select("user_id,diet_preference,email").execute().data
        
        for user in users:
            # Fetch user's meal plans
            plans = supabase.table("mealplans").select("plan_id,plan_type").eq("user_id", user["user_id"]).execute().data
            if not plans:
                continue

            # Fetch meals matching user's diet
            meals = supabase.table("meals").select("meal_id").eq("diet_type", user["diet_preference"]).execute().data
            
            for plan in plans:
                for meal in meals:
                    # Check if meal already linked to avoid duplicates
                    existing = supabase.table("mealplanmeals").select("*").eq("plan_id", plan["plan_id"]).eq("meal_id", meal["meal_id"]).execute().data
                    if not existing:
                        supabase.table("mealplanmeals").insert({
                            "plan_id": plan["plan_id"],
                            "meal_id": meal["meal_id"]
                        }).execute()

        print("Assigned meals to all user plans successfully!")

    except Exception as e:
        print("Error assigning meals to plans:", e)

# ---------- MAIN ----------
if __name__ == "__main__":
    assign_meals_to_plans()
