# 🚀 Quick Setup Guide for Beginners

## Step-by-Step Setup (Windows)

### 1. Install Python

- Download Python from [python.org](https://www.python.org/downloads/)
- ✅ Check "Add Python to PATH" during installation
- Verify: Open Command Prompt and type `python --version`

### 2. Install MySQL

- Download MySQL Community Server from [mysql.com](https://dev.mysql.com/downloads/mysql/)
- During installation, remember your **root password**
- Install MySQL Workbench for easier database management

### 3. Setup Project

```bash
# Open Command Prompt in your project folder
cd c:\Users\Kurt\Documents\dev-practice\python-sql

# Install requirements
pip install Flask mysql-connector-python

# Edit voting_app.py - Change line 15:
# 'password': 'your_password'  # Put your MySQL root password here
```

### 4. Create Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE voting_db;
```

### 5. Run Application

```bash
python voting_app.py
```

### 6. Open Browser

Go to: `http://localhost:5000`

### 7. Initialize System

1. Click "Setup Database Tables" first
2. Add some candidates
3. Register voters
4. Start voting!

## ❗ Common Beginner Mistakes

1. **Forgot to change password** in `voting_app.py`
2. **MySQL not running** - Start it from Services
3. **Wrong directory** - Make sure you're in the right folder
4. **Port 5000 busy** - Close other applications using port 5000

## 🎯 What Each File Does

- `voting_app.py` - The "brain" (backend server)
- `voting.html` - What you see (webpage)
- `voting.css` - How it looks (styling)
- `voting.js` - Interactive features (frontend logic)

Need help? Check the full README.md for detailed explanations!
