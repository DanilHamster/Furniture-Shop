# 🪑 Furniture-Shop

**Premium Django-based eCommerce platform** for elegant furniture cataloging, seamless user interaction, and refined admin management.



## 🚀 Key Features

- 🔐 Email-based custom user authentication  
- 🛋️ Dynamic product catalog with smart filtering  
- 🧠 HTMX-powered interactions for snappy UX  
- 🗂️ Dropbox-integrated media storage (optional)  
- 🧾 Admin panel with enhanced readability and visual separation  
- 🎨 Bootstrap 5 + crispy-forms for clean, responsive UI  

```
Furniture-Shop/
├── account/           # Users, Cart, Comments
├── service/           # Items, ItemClass, Color, Material
├── templates/         # HTML templates (Jinja2)
├── static/            # CSS, JS, images
├── Market/            # Core settings, URLs, WSGI
└── .env
```




## ⚙️ Setup Guide

### 1. 📥 Clone the repository

bash
git clone https://github.com/CashMasterrrr/Furniture-Shop.git
cd Furniture-Shop
. 🧪 Create and activate virtual environment
```
python -m venv .venv
source .venv/Scripts/activate
```


3. 📦 Install dependencies
```
pip install -r requirements.txt
```


5. 🛠️ Configure .env
```
SECRET_KEY=your-secret-key
DEBUG=True

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_PORT=587

DROPBOX_OAUTH2_ACCESS_TOKEN=your-token
DROPBOX_APP_KEY=your-app-key
DROPBOX_APP_SECRET=your-app-secret
```


5. 🧱 Apply migrations and load fixtures
```
python manage.py migrate
python manage.py loaddata furniture_fixture.json
```


7. 👤 Create superuser (optional)
python manage.py createsuperuser


✅ Default admin credentials:
```
Username: admin
Password: admin
```


🖥️ Launch the Server
python manage.py runserver


Open http://127.0.0.1:8000 in your browser to explore the platform.
