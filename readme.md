# 🌍 Country & Region Data Viewer API

A FastAPI-powered web application that allows users to view, filter, and compare GDP and Population data by countries and regions using data from the World Bank.

![App Screenshot](static/images/screenshot.png) <!-- Replace with your actual image path -->

---


# 🌍 ETL Process: World Bank Data

This script extracts, transforms, and loads GDP and population data from the [World Bank API](https://data.worldbank.org/).

## 📦 Files Created

- `raw_countries.csv`: List of all countries (excluding aggregates)
- `raw_indicators.csv`: GDP & population data for 2020–2024
- `indicator_metadata.csv`: Metadata about selected indicators

## 🔁 How It Works

1. **Extract**:
   - Fetch all country details
   - Fetch metadata for GDP (`NY.GDP.MKTP.CD`) and population (`SP.POP.TOTL`)
   - Download indicator data for each country from 2020 to 2024

2. **Transform**:
   - Filter out aggregate entries (e.g., "World", "Europe & Central Asia")
   - Structure indicator data by country-year

3. **Load**:
   - Save all data to CSV files for use in your FastAPI app or data analysis

## ▶️ Run the Script

```bash
python etl_script.py



----
## 🚀 Features

- Interactive dropdowns for countries (name, ISO code, capital city)
- Region-wise aggregate views
- Line charts (GDP & Population)
- Light/Dark mode toggle
- Globe/world map background visuals
- Animated charts (via Chart.js)
- Dockerized for easy deployment

---

## 🛠️ Tech Stack

- **FastAPI** - Web framework
- **Jinja2** - Templating
- **Pandas** - Data manipulation
- **Chart.js** - Data visualization
- **HTML/CSS/JavaScript** - Frontend
- **Docker** - Containerization

---

## 📦 Setup & Run (Locally)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/worldbank-data-viewer.git
cd worldbank-data-viewer

worldbank-data-viewer/
│
├── app/
│   ├── fast.py              # FastAPI app logic
│   ├── templates/           # Jinja2 HTML files
│   ├── static/              # CSS, JS, images
│   └── data/                # CSV data files
│   └── etl/                 # etl 
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .dockerignore

---
```bash
pip install -r requirements.txt
```bash
unicorn fast:app --reload

##  User-Friendly API Guide (Non-developer users)

You can also include this in your `docs/usage_guide.md` or embed it on the homepage:

### 🌐 How to Use the App

1. **Open the application** in your browser at [http://localhost:8000](http://localhost:8000)
2. **Select**:
   - Countries by **Name**, **ISO Code**, or **Capital City**
   - One or more **Regions**
3. **Click "Search"**
4. You’ll see:
   - Tables showing GDP and population per year
   - **Interactive charts** with animations
5. **Switch themes** between light and dark mode
6. Use browser print or export tools to save results

---

Future : etl store as bucket, db , embedding for serach
deploy as app in cloud
