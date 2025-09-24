# NutriGuide
The NutriGuide is a web-based application that helps users plan and manage daily meals based on their personal health goals, dietary preferences, and activity levels. Users can generate personalized meal plans, track calories and macronutrients, browse and save favorite meals, and search meals by category or ingredients. This project demonstrates full-stack development skills, including user authentication, CRUD operations, database design, and responsive frontend design.

# Key Features
User Management: Registration, login, and profile with dietary goals
Personalized Meal Plans: Daily/weekly plans based on calories and macros
Meal Browsing: View meals with ingredients, nutrition, and steps
Favorites: Save preferred meals for easy access
Search & Filter: Find meals by name, ingredients, category, or calories
Optional Admin Panel: Add, edit, or delete meals

# Project Structure
 
NutriGuide/
|
|---src/             # core application logic
|   |---logic.py     # Business logic and task
operations           
|   |__db.py         # Database operations
|
|---api/             # Backend API
|   |__main.py       # FastAPI endpoints
|            
|---frontend/        # frontend application
|   |__app.py        # Streamlit web interface
|
|___requirements.txt  # Python dependencies
|
|___README.md       # Project Documentation
|
|___.env            # Python variables


## Quick Start

### Prerequisites

  Python 3.8 or higher
  A Supabase account
  Git(Push,cloning)

### 1. Clone or Download the Project 
# option 1: Clone with Git
git clone <repository-url>

# option 2: Download and extract the ZIP file

### 2. Install Dependencies

# Install all required Python packages
pip install -r requirements.txt

### 3. Set Up Supabase Database

1.create a Supabase Project:

2.Create the Tasks Table:

-- Go to the SQL Editor in your Supabase dashboard
  Run this SQL command:
--- sql
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    age INT,
    weight FLOAT,
    height FLOAT,
    activity_level VARCHAR(20),
    goal VARCHAR(20),
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP
);

