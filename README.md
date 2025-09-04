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

python manage.py collectstatic


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
# 🔐 Django Core Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_SETTINGS_MODULE=Market.settings.dev
ALLOWED_HOSTS=127.0.0.1,localhost

# 📧 Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# 📦 Dropbox Storage (optional)
DROPBOX_OAUTH2_ACCESS_TOKEN=your-dropbox-access-token
DROPBOX_OAUTH2_REFRESH_TOKEN=your-dropbox-refresh-token
DROPBOX_APP_KEY=your-dropbox-app-key
DROPBOX_APP_SECRET=your-dropbox-app-secret
DROPBOX_ROOT_PATH=media/

# 🗄️ PostgreSQL via Neon
POSTGRES_DB=your-database-name
POSTGRES_DB_PORT=5432
POSTGRES_USER=your-db-username
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=your-db-host-url
```

6. 🧱 Apply migrations and load fixtures
```
python manage.py migrate
python manage.py loaddata furniture_fixture.json
```


7. 👤 Create superuser (optional)
python manage.py createsuperuser

8. 📁 Collect static files (for production)

```bash
python manage.py collectstatic
```


✅ Default admin credentials:
```
Username: admin
Password: superadmin
```

✅ Default user credentials:
```
Username: user1
Password: bestpassword1
```


🖥️ Launch the Server
python manage.py runserver


Open http://127.0.0.1:8000 in your browser to explore the platform.

🌐 Live Deployment

 Or link on render site # 🪑 Furniture-Shop https://hamster-shop.onrender.com 
