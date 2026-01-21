# TyreMaster

TyreMaster is a Django-based web application that helps you manage and explore tyre information. It includes a simple interface, a backend database, and static assets to support viewing, filtering, and interacting with tyre data.

## Features

- Django web app for tyre data management
- Preloaded tyre entries in a SQLite database
- Static assets (CSS, images, JS) for UI
- HTML templates to render pages and lists
- Easy to extend with additional tyre models or features

## Tech Stack

- Python 3
- Django Web Framework
- HTML, CSS, JavaScript
- SQLite (default Django database)

## Repo Structure

TyreMaster/
├── static/ # Static files (CSS, JavaScript, images)
├── templates/ # HTML templates
├── tyremaster/ # Django project settings
├── tyres/ # Tyres application
├── additional_vehicles.csv # Sample dataset
├── db.sqlite3 # SQLite database file
├── manage.py # Django CLI entry point
├── requirements.txt # Python dependencies
└── README.md


## Installation

1. Clone the repo

bash
git clone https://github.com/Venkatesh-6921/TyreMaster.git
cd TyreMaster
Create a Python virtual environment and activate it

python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
Install dependencies

pip install -r requirements.txt
Apply migrations

python manage.py migrate
Load initial data (if available) or skip

# Optional: if fixtures or CSV import logic exists
Run the development server

python manage.py runserver
Open your browser and navigate to:

http://127.0.0.1:8000/
Usage
Once the server is running:

Visit the home page to browse tyre listings

Use the app features to view detailed tyre data

Extend models and views to suit your use case

Contributing
Contributions are welcome. To propose changes:

Fork the repo

Create a feature branch

git checkout -b feature/new-feature
Commit and push your changes

Open a pull request

Keep code clean and consistent with existing Django patterns.
