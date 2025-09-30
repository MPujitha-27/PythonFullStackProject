import sys
import os
import streamlit as st
import matplotlib.pyplot as plt

# ------------------- fix imports -------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(PROJECT_ROOT, "src"))

from logic import MealPlanManager
from db import login_user, register_user

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="NutriGuide", page_icon="🥗", layout="wide")

# ---------- STYLES ----------
st.markdown("""
<style>
body {
    background-image: url('https://images.unsplash.com/photo-1604908177522-0b16c9da0e7b?auto=format&fit=crop&w=1650&q=80');
    background-size: cover;
    background-attachment: fixed;
}
.block-container { padding-top: 0.5rem !important; }
h1.app-title { text-align: center; color: #ffffff; text-shadow: 2px 2px 4px #000000; margin: 6px 0 8px 0; font-family: 'Montserrat', sans-serif; }
.central-card { background: rgba(255,255,255,0.92); padding: 18px; border-radius: 12px; box-shadow: 0 6px 18px rgba(0,0,0,0.22); margin-bottom:15px; }
.stButton button { background-color: #218c74 !important; color: white !important; border-radius: 6px !important; padding: 0.45em 1.2em !important; border: none !important; font-weight: 600 !important; }
.profile-card { background: #f7f7f7; padding: 12px; border-radius: 10px; margin-bottom: 10px; color: black; }
.meal-card { background: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); margin-bottom:10px;}
.metric-card { background: #f1f1f1; padding: 8px; border-radius: 10px; text-align:center; }

/* Sidebar styling */
.sidebar-container {
    padding: 15px;
}
.sidebar-hello {
    font-size: 18px;
    margin-top: 10px;
    margin-bottom: 20px;
    color: #ffffff;   /* white color */
    font-weight: 600;
    text-shadow: 1px 1px 2px #000000; /* subtle shadow for visibility */
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='app-title'>🍏 NutriGuide — Your Personalized Meal Planner</h1>", unsafe_allow_html=True)

# ---------------- AUTHENTICATION ----------------
if "user" not in st.session_state:
    auth_choice = st.radio("Authentication", ["Login", "Register"], horizontal=True, key="auth_radio")
    with st.form("auth_form"):
        if auth_choice == "Login":
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login", key="login_btn")
            if submitted:
                user = login_user(email, password)
                if user:
                    st.session_state["user"] = user
                    st.success(f"Welcome {user.get('name','User')}! Logged in successfully.")
                    st.stop()
                else:
                    st.error("Invalid email or password.")
        else:
            st.subheader("Register")
            name = st.text_input("Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            age = st.number_input("Age", 0, 120, step=1, key="reg_age")
            height = st.number_input("Height (cm)", 50, 250, step=1, key="reg_height")
            weight = st.number_input("Weight (kg)", 20, 300, step=1, key="reg_weight")
            gender = st.selectbox("Gender", ["male","female"], key="reg_gender")
            activity_level = st.selectbox("Activity Level", ["sedentary","light","moderate","active","very_active"], key="reg_activity")
            goal = st.selectbox("Goal", ["loss","gain"], key="reg_goal")
            diet_preference = st.selectbox("Diet Preference", ["vegetarian","non-vegetarian","keto"], key="reg_diet")
            submitted = st.form_submit_button("Register", key="register_btn")
            if submitted:
                res = register_user(name, email, password, age, height, weight, gender, activity_level, goal, diet_preference)
                if res and getattr(res, "data", None):
                    st.success("Registration successful! Please login now.")
                    st.stop()
                else:
                    st.error("Failed to register. Try again.")

# ---------------- LOGGED-IN USER ----------------
user = st.session_state.get("user")
if not user:
    st.stop()

manager = MealPlanManager()

# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    st.markdown("<div class='sidebar-container'>", unsafe_allow_html=True)
    st.markdown("### ☰ Dashboard")
    st.image("https://cdn-icons-png.flaticon.com/512/847/847969.png", width=80)  # user icon
    st.markdown(f"<div class='sidebar-hello'>Hello, {user.get('name','User')}</div>", unsafe_allow_html=True)
    
    if st.button("🚪 Logout", key="sidebar_logout"):
        st.session_state["show_logout_confirm"] = True
    
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Logout confirmation modal ----
if st.session_state.get("show_logout_confirm", False):
    st.warning("Do you really want to logout?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes", key="logout_yes"):
            st.session_state.clear()
            st.success("Logged out successfully.")
            st.rerun()
    with col2:
        if st.button("❌ No", key="logout_no"):
            st.session_state["show_logout_confirm"] = False
            st.rerun()

# ---------------- PROFILE ----------------
st.subheader("Your Profile")
st.markdown(f"""
<div class="profile-card">
<strong>Name:</strong> {user.get("name","-")} <br>
<strong>Email:</strong> {user.get("email","-")} <br>
<strong>Age:</strong> {user.get("age","-")} <br>
<strong>Height:</strong> {user.get("height","-")} cm<br>
<strong>Weight:</strong> {user.get("weight","-")} kg<br>
<strong>Gender:</strong> {user.get("gender","-")}<br>
<strong>Activity Level:</strong> {user.get("activity_level","-")}<br>
<strong>Goal:</strong> {user.get("goal","-")}<br>
<strong>Diet Preference:</strong> {user.get("diet_preference","-")}<br>
</div>
""", unsafe_allow_html=True)

# ---------------- BMR, TARGETS & BMI ----------------
bmr = manager.calculate_bmr(user["weight"], user["height"], user["age"], user["gender"])
target_cal = manager.calculate_daily_calories(bmr, user["goal"], user["activity_level"])
water_liters = manager.calculate_water(user["weight"])
steps = manager.calculate_steps(user["activity_level"])
bmi_value, weight_status = manager.calculate_bmi(user["weight"], user["height"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("BMR (kcal/day)", f"{bmr:.2f}")
col2.metric("Target calories", f"{target_cal:.2f}")
col3.metric("Water (L/day)", f"{water_liters:.2f}")
col4.metric("BMI", f"{bmi_value:.2f} ({weight_status})")

# ---------------- WEIGHT GOAL MESSAGE ----------------
height_m = user["height"] / 100
ideal_weight_min = 18.5 * (height_m ** 2)
ideal_weight_max = 24.9 * (height_m ** 2)
current_weight = user["weight"]
goal = user.get("goal", "maintain")  # "gain" or "loss"

if goal == "gain":
    if current_weight < ideal_weight_max:
        weight_to_gain = ideal_weight_max - current_weight
        st.info(f"⚠️ Your goal is to gain weight. You should aim to gain approximately {weight_to_gain:.1f} kg to reach a healthy BMI range.")
    else:
        st.success("✅ You are already at or above the healthy BMI range. Maintain your weight.")
elif goal == "loss":
    if current_weight > ideal_weight_min:
        weight_to_lose = current_weight - ideal_weight_min
        st.info(f"⚠️ Your goal is to lose weight. You should aim to lose approximately {weight_to_lose:.1f} kg to reach a healthy BMI range.")
    else:
        st.success("✅ You are already at or below the healthy BMI range. Maintain your weight.")
else:
    if bmi_value < 18.5:
        weight_to_gain = ideal_weight_min - current_weight
        st.info(f"⚠️ You are underweight. You should aim to gain approximately {weight_to_gain:.1f} kg to reach a healthy BMI.")
    elif bmi_value > 24.9:
        weight_to_lose = current_weight - ideal_weight_max
        st.info(f"⚠️ You are overweight. You should aim to lose approximately {weight_to_lose:.1f} kg to reach a healthy BMI.")
    else:
        st.success("✅ Your weight is within the healthy range. Keep it up!")

# ---------------- FALLBACK MEALS ----------------
FALLBACK_MEALS = manager.get_fallback_meals()

# ---------------- GENERATE DAILY PLAN ----------------
st.subheader("Get your daily meal plan")
if st.button("Generate Plan", key="generate_plan"):
    try:
        plan = manager.generate_daily_plan(user)
        if not plan.get("success", True):
            plan = {
                "success": True,
                "meals": FALLBACK_MEALS,
                "total_calories": target_cal,
                "water_recommendation": water_liters,
                "step_recommendation": steps,
                "bmi": bmi_value,
                "weight_status": weight_status
            }
        daily_plan = plan

        st.markdown(f"### Today")

        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f"💪 **Calories:** {daily_plan.get('total_calories', target_cal):.2f} kcal")
        col2.markdown(f"💧 **Water:** {daily_plan.get('water_recommendation', water_liters):.2f} L")
        col3.markdown(f"🚶 **Steps:** {daily_plan.get('step_recommendation', steps)}")
        col4.markdown(f"⚖️ **Weight Status:** {daily_plan.get('weight_status', weight_status)} "
                       f"(BMI: {daily_plan.get('bmi', bmi_value):.2f})")
        st.markdown("---")

        meals = daily_plan.get("meals", FALLBACK_MEALS)
        meal_times_order = ["breakfast", "lunch", "snack", "dinner"]
        used_names = set()
        for mt in meal_times_order:
            meal = next((m for m in meals if m.get("meal_time") == mt and m.get("name") not in used_names), None)
            if meal:
                used_names.add(meal.get("name"))
                st.markdown("<div class='meal-card'>", unsafe_allow_html=True)
                cols = st.columns([1,2])
                with cols[0]:
                    if meal.get("image"):
                        st.image(meal.get("image"), width="stretch", caption=meal.get("name"))
                with cols[1]:
                    st.markdown(f"### {meal.get('meal_time').capitalize()} - {meal.get('name')}")
                    st.markdown(f"- Calories: {meal.get('calories',0)} kcal")
                    st.markdown(f"- Protein: {meal.get('protein',0)} g")
                    st.markdown(f"- Carbs: {meal.get('carbs',0)} g")
                    st.markdown(f"- Fats: {meal.get('fats',0)} g")
                    if meal.get("ingredients"):
                        st.markdown(f"**Ingredients:** {meal.get('ingredients')}")
                    if meal.get("instructions"):
                        st.markdown(f"[Recipe/Instructions]({meal.get('instructions')})")
                st.markdown("</div>", unsafe_allow_html=True)

        total_protein = sum(m.get("protein",0) for m in meals)
        total_carbs = sum(m.get("carbs",0) for m in meals)
        total_fats = sum(m.get("fats",0) for m in meals)
        if total_protein + total_carbs + total_fats > 0:
            fig, ax = plt.subplots(figsize=(2,2))
            ax.pie([total_protein*4, total_carbs*4, total_fats*9],
                   labels=[f"Protein ({int(total_protein)} g)",
                           f"Carbs ({int(total_carbs)} g)",
                           f"Fats ({int(total_fats)} g)"],
                   autopct=lambda p: f"{p:.1f}%" if p > 0 else "", startangle=140)
            ax.set_title("Macros (kcal %)")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error generating plan: {e}")
