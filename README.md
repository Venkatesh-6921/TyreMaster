# 🚗 TyreMaster (Django)

A web-based **Tyre Management System** built using the **Django Framework** and **SQLite3 database**.  
The application helps manage and display tyre-related data in a structured and user-friendly web interface.

---

## 🚀 Features

- View and manage tyre information  
- Store tyre data using SQLite database  
- Modular Django app structure for clean organization  
- Dynamic pages rendered using Django templates  
- Static files for styling and frontend interaction  
- Easy to extend with search, filters, or analytics  
- Simple local setup and deployment-ready  

---

## 🏗️ Project Structure

```
TyreMaster/
├── manage.py
├── db.sqlite3
├── additional_vehicles.csv
├── tyremaster/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tyres/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── tyres/
│           └── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── requirements.txt
```

---

## ⚙️ Installation & Local Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Venkatesh-6921/TyreMaster.git
cd TyreMaster
```

### 2️⃣ Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Required Packages
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Development Server
```bash
python manage.py runserver
```

Now open your browser and visit:  
👉 http://127.0.0.1:8000/

---

### ⚠️ Important Note (Static Files Fix)

If static files do not load locally, update `STATICFILES_DIRS` in `settings.py`.

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

---

## 🗃️ Tech Stack

| Component | Technology |
|---------|------------|
| Framework | Django |
| Database | SQLite3 |
| Frontend | HTML, CSS (Django Templates) |
| Backend | Python |
| Deployment | PythonAnywhere |
| Version Control | Git + GitHub |

---

## 📦 Dependencies

```txt
Django>=5.0,<6.0
asgiref>=3.8,<4.0
sqlparse>=0.5,<1.0
tzdata>=2023.3,<2025.0
```

---

## 🧑‍💻 Author

**Maragada Venkateswara Reddy**  
🎓 Django Web Development Project  
📧 maragadavekatesh@gmail.com  

---

## 🪶 License

This project is licensed under the MIT License.
