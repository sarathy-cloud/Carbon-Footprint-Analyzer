# EcoTrack: Carbon Footprint Dashboard

EcoTrack is a full-stack web application designed to help individuals and companies calculate, track, and reduce their carbon footprint. It provides a dynamic, responsive dashboard to visualize emission trends and offers data-driven recommendations for sustainability.

This project was built for the **Prompt-a-Thon Hackathon**, with its architecture, code, and iterative refinements developed in collaboration with generative AI.

## 🏆 Hackathon Context

This project is a direct result of the "Prompt-a-Thon" challenge. The primary goal was to architect and build a functional, full-stack application starting from a high-level concept, using natural language prompts as the primary development tool.

The entire application—from the initial idea, Python Flask backend, file-based database logic, and the responsive, multi-page HTML/Tailwind frontend—was generated and refined through a collaborative prompting process. This repository demonstrates a modern workflow where the developer acts as an architect and a guide, leveraging AI to build and debug complex software.

## ✨ Features

- **Secure User Authentication:** A simple, file-based login and registration system (`users.txt`).
    
- **Persistent File Storage:** Each user's emissions data is saved to a unique, persistent CSV file in the `/data` directory.
    
- **Dynamic Main Dashboard:** Displays key metrics, including total emissions and breakdowns for Scope 1, Scope 2, and Scope 3.
    
- **Historical Trend Analysis:** A table shows the last 3 weeks of emissions data, with color-coded indicators (red/green) to show increases or decreases.
    
- **Data-Driven Recommendations:** A core feature that compares the most recent week to the previous one, identifying the specific inputs (e.g., "Petrol Usage," "Electricity") that were the biggest drivers of change.
    
- **Sector-Specific Inputs:** Tailored "Add Data" forms for various industries (Manufacturing, Retail, IT, etc.), ensuring relevant data collection.
    
- **Multi-Page Interface:** A seamless single-page-app (SPA) feel, managed with JavaScript to show/hide Login, Dashboard, and Add Data pages.
    
- **Data Visualization:** Clean charts (powered by Chart.js) provide an instant visual breakdown of emissions.
    

## 📸 Screenshots

![[Pasted image 20251029051730.png]]
![[Pasted image 20251029051752.png]]
![[Pasted image 20251029051848.png]]

## 💻 Tech Stack

- **Backend:** **Python**
    
    - **Flask:** For the web server and API endpoints (`/login`, `/register`, `/get-data`, `/add-data`).
        
    - **`csv` & `json`:** For reading and writing to the file-based database.
        
- **Frontend:** **HTML5**
    
    - **Tailwind CSS:** For all styling and the responsive, dark-mode layout.
        
    - **JavaScript (Vanilla):** For all client-side logic, API calls (`fetch`), state management, and page navigation.
        
    - **Chart.js:** For rendering the doughnut and bar charts on the dashboard.
        

## 🚀 Setup and Installation

Follow these steps to run the project locally.

### 1. Project Structure

Ensure your project directory looks like this:

```
/
├── app.py             # The Python Flask backend
├── requirements.txt   # Python dependencies
├── users.txt          # File to store user logins (starts empty)
├── data/              # <-- You MUST create this empty folder
│   └── (empty)
├── templates/         # <-- You MUST create this folder
│   └── index.html     # The HTML/JS frontend
└── README.md
```

### 2. Create Folders

You must manually create the `data/` and `templates/` folders in the root of the project.

### 3. Set up a Virtual Environment

It's highly recommended to use a virtual environment.

```
# Create the virtual environment
python -m venv venv

# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

Install Flask and its dependencies from `requirements.txt`.

```
pip install -r requirements.txt
```

### 5. Run the Server

With your virtual environment active, run the Flask application.

```
flask run
```

You should see output similar to: `* Running on http://127.0.0.1:5000/`

### 6. Open the Application

Open your web browser and go to:

https://www.google.com/search?q=http://127.0.0.1:5000/

## 📖 How to Use

1. **Register:** On the login page, enter a new username (e.g., "admin") and password. The app will prompt you to register. Select your default business sector.
    
2. **Login:** You will be logged in and taken to the empty dashboard.
    
3. **Add Your First Week:** Click "Add Data" in the top-right corner. Fill out the form for your sector and click "Calculate & Save".
    
4. **View Dashboard:** You'll be taken back to the dashboard, which now shows your first week of data.
    
5. **Add a Second Week:** Click "Add Data" again to submit data for a second week.
    
6. **See the Magic:** The dashboard will now be fully populated. The "Previous Weeks" table will show both weeks, and the "Data-Driven Recommendations" section will activate, comparing your two entries and giving you specific feedback.
    

_This project was developed as part of the Prompt-a-Thon Hackathon._
