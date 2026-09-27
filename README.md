# PocketSmart AI

PocketSmart AI is a Generative AI powered budget and recommendation assistant.

It provides three major planners:

1. Home Interior Planner
2. Party Budget Planner
3. Jewelry Budget Planner

The application uses FastAPI, SQLite, Jinja2, JavaScript and Gemini.

---

# Features

## Authentication

- Register
- Login
- Logout
- JWT authentication
- HTTP-only authentication cookie

## Home Interior Planner

Users can provide:

- Budget
- Style
- Rooms
- Required items

The system creates a budget-aware recommendation.

## Party Planner

Users can provide:

- Budget
- Number of guests
- Event type
- Venue
- City

The AI creates a party budget plan.

## Jewelry Planner

Users can provide:

- Budget
- Occasion
- Style
- Outfit color
- Metal preference
- Optional outfit image

The outfit image can be sent to Gemini as multimodal input.

## Recommendation History

Every generated recommendation is stored in SQLite.

## API Documentation

FastAPI automatically generates:

http://127.0.0.1:8000/docs

---

# Project Structure

```text
PocketSmartAI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── pages.py
│   │   ├── planners.py
│   │   └── api.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── catalog_service.py
│       ├── gemini_service.py
│       └── recommender.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── history.html
│   ├── planner.html
│   └── recommendations.html
│
├── tests/
│   └── test_app.py
│
├── data/
│   └── .gitkeep
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md