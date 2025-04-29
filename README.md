# 🧠 Social Media Post Prediction Dashboard

This is a Django-based web application that allows users to view, analyze, and track **predictions** made on their social media posts across platforms like  **Reddit** or others. The app displays historical post metrics alongside machine learning-based predictions of future performance (likes, comments, shares, mood).

## 🌟 Features

- User authentication and dashboard
- Profile summary and member since info
- List of recent predictions with:
  - Post content preview
  - Real and predicted metrics
  - Platform-specific icons
- Post detail page with:
  - Full post content
  - Platform source with external link
  - Real-time and predicted engagement metrics
  - Mood classification
- Bootstrap 5 & Bootstrap Icons support

## 🛠 Requirements

Before running the project, ensure you have the following installed:

- Python 3.8+
- Django 5.x
- `django-mongodb-engine` for MongoDB support
- MongoDB 4.0+ (running locally or via Atlas)


## 📦 Installation

#### 1. Clone the repo

```bash
git clone https://github.com/UkraintetsAndriyKPI/post-popularity-prediction.git
cd post-popularity-prediction
```

#### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate
# On Windows use: .venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```


## ⚙️ DB Configuration

Update `settings.py` to connect to your MongoDB instance:

```python
DATABASES = {
    "default": django_mongodb_backend.parse_uri(os.getenv("MONGODB_URI")),
    db_name="mongodb-main"),
}
```

## 🤝 Contributions

Feel free to fork the project and submit pull requests. Suggestions, issues, and improvements are always welcome!
