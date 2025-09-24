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

 
3. **Get Your Credentials**:

### 4.Configure Environment Variables

1.Create a '.env' file in the project root

2.Add your Supabase Credentials to '.env':
SUPABASE_URL = https://dzdipugofiocwcunypgm.supabase.co
SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6ZGlwdWdvZmlvY3djdW55cGdtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIyMTgsImV4cCI6MjA3MzY1ODIxOH0.e4XXJeLcb5N_JEFT09oXG5bM3hq8aW9ouM2i7FFObag


### 5. Run the Application

## Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at 'http://localhost:8501'

## FastAPI Backend

cd api
python main.py

The API will be available at 'http://localhost:8000'

## How to use

## Technical Details

### Technologies Used
  **Frontend**: Python (Streamlit) – Interactive web interface for users

  **Backend**: Python (FastAPI) – API endpoints and business logic

  **Database**: Supabase PostgreSQL – Store users, meals, and meal plans

  **Programming Language**: Python – Full-stack development

### Key Components

1. **'src/db.py'**: Database operations
   Handles all CRUD Operations with Supabase

2. **'src/logic.py'**:Business logic Task validation and processing

3. **'api/main.py'** – Backend API
FastAPI endpoints to handle requests from the frontend, fetch data, and return meal plans or search results.

4. **'frontend/app.py'** – Frontend Interface
Streamlit-based user interface for interacting with the application, displaying meal plans, and searching meals.

5. **'requirements.txt'** – Python Dependencies
Lists all required Python packages for running the project (FastAPI, Streamlit, SQLAlchemy, requests, etc.).

6. **'.env'** – Environment Variables
Stores sensitive information like database paths, API keys, or secret keys securely.

7. **'README.md'** – Project Documentation
Contains project overview, setup instructions, features, and usage details.

## Troubleshooting

## Common Issues

1. **"Module not found" errors**
   Make sure you've installed all dependencies 'pip install -r
   requirements.txt'
   Check that you're running commands from the correct directory

## Future Enhancements
  Ideas for extending this project:

  **User Personalization**: Dietary preferences, progress tracking, water intake
  **Smart Meal Recommendations**: Based on available ingredients or goals
  **Nutrition Visualization**: Charts for calories and macros, weekly summaries
  **Social Features**: Share meal plans, comment, rate meals
  **Admin & Analytics**: Manage meals, track popular meals, generate reports
  **Notifications**: Reminders for meals or hydration
  **Deployment Enhancements**: Live web app with authentication and responsive design

## Support

If you encounter any issues or have questions:
Mobile No : 8121275126
Email Id : kopurimahimapujitha@gmail.com