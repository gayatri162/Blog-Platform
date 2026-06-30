# 📝 Blog Platform

A modern full-stack blogging platform built using Flask and MongoDB where users can register, publish blogs, upload images, like posts, save blogs, and interact through comments.

## 🚀 Live Demo

[https://blog-platform-8tr2.onrender.com](https://blog-platform-8tr2.onrender.com)

---

## ✨ Features

- User Registration & Login
- Secure Password Hashing (bcrypt)
- Create, Read, Edit & Delete Blogs
- Upload Images using Cloudinary
- Like / Unlike Blogs
- Save Blogs
- Comment Section
- Search Blogs
- User Profile
- Pagination
- Responsive Design
- MongoDB Atlas Database
- Deployed on Render

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Jinja2

### Backend
- Python
- Flask

### Database
- MongoDB Atlas

### Cloud Storage
- Cloudinary

### Deployment
- Render

---

## 📁 Project Structure

```

Blog-Platform/

│

├── database/

│   └── db.py

│

├── static/

│   ├── css/

│   │   └── style.css

│   └── js/

│       └── script.js

│

├── templates/

│   ├── index.html

│   ├── login.html

│   ├── register.html

│   ├── dashboard.html

│   ├── create_post.html

│   ├── edit_post.html

│   ├── post.html

│   ├── profile.html

│   └── saved.html

│

├── app.py

├── wsgi.py

├── requirements.txt

├── README.md

├── .gitignore

└── .env (not included in GitHub)

```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/gayatri162/Blog-Platform.git
```

Move into project folder

```bash
cd Blog-Platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
MONGO_URI=your_mongodb_uri

SECRET_KEY=your_secret_key

CLOUD_NAME=your_cloud_name

API_KEY=your_api_key

API_SECRET=your_api_secret
```

Run the project

```bash
python3 app.py
```

---

## 📷 Screenshots



---

## 👩‍💻 Author

**Gayatri**

Engineering Student

🐙GitHub:
[https://github.com/gayatri162](https://github.com/gayatri162)

📁Linkedin:
[https://www.linkedin.com/in/gayatri-singh/](https://www.linkedin.com/in/gayatri-singh/)
