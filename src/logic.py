import requests
import random

EDAMAM_APP_ID = "your_app_id"
EDAMAM_APP_KEY = "your_app_key"

# ---------------- FALLBACK MEALS ---------------- #
FALLBACK_MEALS = {
    # VEGETARIAN - WEIGHT LOSS
    ("loss", "vegetarian"): [
        {
            "meal_time": "breakfast",
            "name": "Oats with Berries",
            "calories": 300,
            "protein": 12,
            "carbs": 50,
            "fats": 5,
            "ingredients": "Oats, Almond milk, Blueberries, Honey",
            "instructions": "Cook oats, add berries, drizzle with honey.",
            "image": "https://img.freepik.com/premium-photo/bowl-oatmeal-with-berries-oats_732812-1684.jpg"
        },
        {
            "meal_time": "lunch",
            "name": "Vegetable Stir Fry",
            "calories": 350,
            "protein": 14,
            "carbs": 45,
            "fats": 10,
            "ingredients": "Broccoli, Carrot, Tofu, Soy sauce",
            "instructions": "Stir fry veggies and tofu with soy sauce.",
            "image": "https://cdn.loveandlemons.com/wp-content/uploads/2025/02/stir-fry.jpg"
        },
        {
            "meal_time": "snack",
            "name": "Carrot Sticks with Hummus",
            "calories": 150,
            "protein": 6,
            "carbs": 18,
            "fats": 7,
            "ingredients": "Carrots, Hummus",
            "instructions": "Dip carrot sticks in hummus.",
            "image": "https://www.attainable-sustainable.net/wp-content/uploads/2018/04/red-pepper-hummus.jpg"
        },
        {
            "meal_time": "dinner",
            "name": "Lentil Soup",
            "calories": 400,
            "protein": 20,
            "carbs": 50,
            "fats": 8,
            "ingredients": "Lentils, Tomato, Onion, Spices",
            "instructions": "Cook lentils with tomato, onion, and spices.",
            "image": "https://tse4.mm.bing.net/th/id/OIP.AbJZfLD5sVec8xnWBfbNDAHaE8?rs=1&pid=ImgDetMain&o=7&rm=3"
        }
    ],

    # VEGETARIAN - WEIGHT GAIN
    ("gain", "vegetarian"): [
        {
            "meal_time": "breakfast",
            "name": "Paneer Paratha with Yogurt",
            "calories": 500,
            "protein": 22,
            "carbs": 60,
            "fats": 18,
            "ingredients": "Whole wheat flour, Paneer, Yogurt",
            "instructions": "Stuff paratha with paneer and serve with yogurt.",
            "image": "https://www.cookwithmanali.com/wp-content/uploads/2013/09/Paneer-Paratha-Homemade.jpg"
        },
        {
            "meal_time": "lunch",
            "name": "Chickpea Curry with Rice",
            "calories": 650,
            "protein": 28,
            "carbs": 80,
            "fats": 15,
            "ingredients": "Chickpeas, Rice, Onion, Tomato",
            "instructions": "Cook chickpeas in tomato gravy and serve with rice.",
            "image": "https://www.gimmesomeoven.com/wp-content/uploads/2022/09/Chickpea-Curry-9.jpg"
        },
        {
            "meal_time": "snack",
            "name": "Dry Fruits Mix",
            "calories": 350,
            "protein": 12,
            "carbs": 30,
            "fats": 22,
            "ingredients": "Almonds, Cashews, Walnuts, Raisins",
            "instructions": "Mix and eat dry fruits.",
            "image": "https://m.media-amazon.com/images/I/61jd1-BRNCL._SL1278_.jpg"
        },
        {
            "meal_time": "dinner",
            "name": "Paneer Butter Masala with Naan",
            "calories": 700,
            "protein": 30,
            "carbs": 75,
            "fats": 28,
            "ingredients": "Paneer, Tomato, Butter, Naan",
            "instructions": "Cook paneer in tomato butter gravy, serve with naan.",
            "image": "https://img.freepik.com/premium-photo/butter-naan-panner-butter-masala-indian-dish_651966-45.jpg?w=2000"
        }
    ],

    # NON-VEG - WEIGHT LOSS
    ("loss", "non-vegetarian"): [
        {
            "meal_time": "breakfast",
            "name": "Egg White Omelette",
            "calories": 250,
            "protein": 20,
            "carbs": 5,
            "fats": 10,
            "ingredients": "Egg whites, Spinach, Tomato",
            "instructions": "Whisk egg whites, cook with spinach and tomato.",
            "image": "https://healthyrecipesblogs.com/wp-content/uploads/2022/04/egg-white-omelet-1-2022-.jpg"
        },
        {
            "meal_time": "lunch",
            "name": "Grilled Chicken Salad",
            "calories": 400,
            "protein": 35,
            "carbs": 20,
            "fats": 12,
            "ingredients": "Chicken, Lettuce, Olive oil",
            "instructions": "Grill chicken and serve over salad.",
            "image": "https://tse4.mm.bing.net/th/id/OIP.r9p3zPhvzzRVDFAfpISbiwHaHa?rs=1&pid=ImgDetMain&o=7&rm=3"
        },
        {
            "meal_time": "snack",
            "name": "Boiled Eggs",
            "calories": 150,
            "protein": 12,
            "carbs": 2,
            "fats": 10,
            "ingredients": "Eggs, Salt, Pepper",
            "instructions": "Boil eggs and sprinkle salt and pepper.",
            "image": "https://tse4.mm.bing.net/th/id/OIP.0kZk-SwVTfYpGlxZ1kTW1AHaE7?rs=1&pid=ImgDetMain&o=7&rm=3"
        },
        {
            "meal_time": "dinner",
            "name": "Grilled Fish with Veggies",
            "calories": 500,
            "protein": 40,
            "carbs": 25,
            "fats": 15,
            "ingredients": "Fish, Olive oil, Zucchini, Carrots",
            "instructions": "Grill fish and veggies, drizzle with olive oil.",
            "image": "https://thumbs.dreamstime.com/b/grilled-fish-vegetables-served-plate-restaurant-food-delicious-food-generative-ai-grilled-fish-vegetables-served-278848709.jpg"
        }
    ],

    # NON-VEG - WEIGHT GAIN
    ("gain", "non-vegetarian"): [
        {
            "meal_time": "breakfast",
            "name": "Egg & Avocado Toast",
            "calories": 450,
            "protein": 20,
            "carbs": 35,
            "fats": 22,
            "ingredients": "Eggs, Avocado, Bread, Olive oil",
            "instructions": "Toast bread, add avocado and fried eggs.",
            "image": "https://www.skinnytaste.com/wp-content/uploads/2015/01/Avocado-Toast-with-Egg-3.jpg"
        },
        {
            "meal_time": "lunch",
            "name": "Grilled Chicken with Rice",
            "calories": 650,
            "protein": 45,
            "carbs": 70,
            "fats": 18,
            "ingredients": "Chicken breast, Rice, Spices",
            "instructions": "Grill chicken and serve with steamed rice.",
            "image": "https://easyhealthyrecipes.com/wp-content/uploads/2022/06/grilled-chicken-rice-14-768x1152.jpg"
        },
        {
            "meal_time": "snack",
            "name": "Protein Smoothie",
            "calories": 300,
            "protein": 25,
            "carbs": 40,
            "fats": 8,
            "ingredients": "Milk, Banana, Protein powder, Peanut butter",
            "instructions": "Blend all ingredients.",
            "image": "https://tse1.explicit.bing.net/th/id/OIP.woAt0TzJHA6hZ-ibB1veewHaHO?rs=1&pid=ImgDetMain&o=7&rm=3"
        },
        {
            "meal_time": "dinner",
            "name": "Steak with Sweet Potatoes",
            "calories": 700,
            "protein": 50,
            "carbs": 45,
            "fats": 25,
            "ingredients": "Steak, Sweet potatoes, Garlic",
            "instructions": "Grill steak and serve with roasted sweet potatoes.",
            "image": "https://th.bing.com/th/id/OIP.oGzfYbg7gIqAoNjpKuWwkAHaFj?w=234&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3"
        }
    ],

    # KETO - WEIGHT LOSS
    ("loss", "keto"): [
        {
            "meal_time": "breakfast",
            "name": "Keto Scrambled Eggs",
            "calories": 300,
            "protein": 18,
            "carbs": 4,
            "fats": 22,
            "ingredients": "Eggs, Butter, Cheese, Spinach",
            "instructions": "Scramble eggs in butter, add cheese and spinach.",
            "image": "https://th.bing.com/th/id/OIP.Ht8GTqJrKxn7FXNN2yG5KAHaLH?o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3"
        },
        {
            "meal_time": "lunch",
            "name": "Avocado Chicken Salad",
            "calories": 450,
            "protein": 30,
            "carbs": 8,
            "fats": 28,
            "ingredients": "Chicken, Avocado, Lettuce, Olive oil",
            "instructions": "Mix avocado and grilled chicken into a salad.",
            "image": "https://leisurerecipes.com/wp-content/uploads/2025/03/Keto-Avocado-Chicken-Salad-2-1024x683.webp"
        },
        {
            "meal_time": "snack",
            "name": "Cheese Cubes",
            "calories": 200,
            "protein": 12,
            "carbs": 2,
            "fats": 15,
            "ingredients": "Cheddar cheese, Mozzarella cheese",
            "instructions": "Cut cheese into cubes and eat.",
            "image": "https://images.freshop.com/7731219/5dd7e52ff63af3d57cfa778ea1343323_large.png"
        },
        {
            "meal_time": "dinner",
            "name": "Zucchini Noodles with Pesto",
            "calories": 350,
            "protein": 14,
            "carbs": 10,
            "fats": 25,
            "ingredients": "Zucchini, Pesto, Olive oil",
            "instructions": "Spiralize zucchini, toss with pesto and olive oil.",
            "image": "https://i.pinimg.com/736x/92/e5/ca/92e5caf48f1a55d92771932e72d26819.jpg"
        }
    ],

    # KETO - WEIGHT GAIN
    ("gain", "keto"): [
        {
            "meal_time": "breakfast",
            "name": "Keto Bulletproof Coffee",
            "calories": 400,
            "protein": 2,
            "carbs": 1,
            "fats": 40,
            "ingredients": "Coffee, Butter, MCT oil",
            "instructions": "Blend coffee with butter and MCT oil.",
            "image": "https://tse2.mm.bing.net/th/id/OIP.hlsX_HyQUxmlq7wjgPfSQwHaKX?rs=1&pid=ImgDetMain&o=7&rm=3"
        },
        {
            "meal_time": "lunch",
            "name": "Keto Beef Burger (no bun)",
            "calories": 650,
            "protein": 40,
            "carbs": 6,
            "fats": 48,
            "ingredients": "Beef patty, Cheese, Lettuce, Tomato",
            "instructions": "Grill beef patty, wrap in lettuce with toppings.",
            "image": "https://th.bing.com/th/id/OIP.0eWIjMtkNwciYcIZUwkzHgHaHa?o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3"
        },
        {
            "meal_time": "snack",
            "name": "Keto Fat Bombs",
            "calories": 300,
            "protein": 5,
            "carbs": 3,
            "fats": 30,
            "ingredients": "Coconut oil, Peanut butter, Cocoa powder",
            "instructions": "Mix ingredients and freeze into fat bombs.",
            "image": "https://irepo.primecp.com/2017/06/332185/Keto-Fat-Bombs-with-Cacao-and-Cashew_Large600_ID-2252854.jpg?v=2252854"
        },
        {
            "meal_time": "dinner",
            "name": "Grilled Salmon with Butter Sauce",
            "calories": 700,
            "protein": 45,
            "carbs": 4,
            "fats": 50,
            "ingredients": "Salmon, Butter, Garlic, Lemon",
            "instructions": "Grill salmon and serve with garlic butter sauce.",
            "image": "https://th.bing.com/th/id/OIP.1QT9viXh4nSmc86nz0zQ3AAAAA?o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3"
        }
    ],
}

# ---------------- MEAL PLAN MANAGER ---------------- #
class MealPlanManager:
    def __init__(self):
        self.fallback_meals = FALLBACK_MEALS

    # ------------------ API FETCH ------------------
    def fetch_recipes(self, query, diet=None, meal_type=None):
        url = "https://api.edamam.com/search"
        params = {"q": query, "app_id": EDAMAM_APP_ID, "app_key": EDAMAM_APP_KEY, "from":0,"to":10}
        if diet: params["health"]=diet
        if meal_type: params["mealType"]=meal_type
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                hits = response.json().get("hits", [])
                meals=[]
                for hit in hits:
                    recipe = hit["recipe"]
                    meals.append({
                        "meal_time": meal_type or "meal",
                        "name": recipe["label"],
                        "calories": int(recipe["calories"]/recipe["yield"]),
                        "protein": int(recipe.get("totalNutrients", {}).get("PROCNT", {}).get("quantity",0)/recipe["yield"]),
                        "carbs": int(recipe.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity",0)/recipe["yield"]),
                        "fats": int(recipe.get("totalNutrients", {}).get("FAT", {}).get("quantity",0)/recipe["yield"]),
                        "ingredients": ", ".join(recipe.get("ingredientLines",[])),
                        "instructions": "Follow recipe steps on Edamam.",
                        "image": recipe.get("image","")
                    })
                return meals
        except:
            pass
        return []

    # ------------------ DAILY PLAN ------------------
    def generate_daily_plan(self, user):
        goal = user.get("goal")
        diet = user.get("diet_preference")
        queries = {"loss":"low calorie","gain":"high protein high calorie","maintain":"balanced diet"}
        selected_meals=[]
        for meal_time in ["breakfast","lunch","snack","dinner"]:
            meals = self.fetch_recipes(f"{queries.get(goal,'balanced')} {diet}",
                                       diet="vegetarian" if diet=="vegetarian" else None,
                                       meal_type=meal_time)
            if meals: 
                selected_meals.append(random.choice(meals))
        if len(selected_meals)<4:
            selected_meals = self.fallback_meals.get((goal,diet),[])
        return {"day":"Today","meals":selected_meals}

    # ------------------ UTILITY FUNCTIONS ------------------
    def get_fallback_meals(self):
        meals=[]
        for key in self.fallback_meals: 
            meals.extend(self.fallback_meals[key])
        return meals

    def calculate_bmr(self, weight,height,age,gender):
        return 10*weight+6.25*height-5*age+(5 if gender=="male" else -161)

    def calculate_daily_calories(self,bmr,goal,activity_level):
        multiplier={"sedentary":1.2,"light":1.375,"moderate":1.55,"active":1.725,"very_active":1.9}.get(activity_level,1.2)
        cal = bmr*multiplier
        if goal=="loss": cal-=500
        elif goal=="gain": cal+=500
        return int(cal)

    def calculate_water(self,weight): 
        return weight*0.035

    def calculate_steps(self,activity_level):
        return {"sedentary":4000,"light":6000,"moderate":8000,"active":10000,"very_active":12000}.get(activity_level,6000)

    def calculate_bmi(self,weight,height):
        h = height/100
        bmi = round(weight/(h*h),1)
        if bmi<18.5: status="Underweight"
        elif bmi<25: status="Normal"
        elif bmi<30: status="Overweight"
        else: status="Obese"
        return bmi,status