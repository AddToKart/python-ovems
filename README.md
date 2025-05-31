# 🗳️ Python Online Voting System

A simple full-stack web application demonstrating an online voting and election management system built with Python Flask and MySQL.

## 📋 Features

- **Candidate Management**: Add candidates for different positions (President, Vice President, Senator, Governor)
- **Voter Registration**: Register voters with unique IDs and email addresses
- **Secure Voting**: One vote per voter with validation
- **Real-time Results**: View election results with vote counts and percentages
- **Audit Logging**: Track all system activities for security and monitoring
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technologies Used

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database Connector**: mysql-connector-python

## 📁 Project Structure

```
python-sql/
├── voting_app.py          # Main Flask application with all backend logic
├── voting.html            # Frontend HTML interface
├── voting.css             # Styling for the interface
├── voting.js              # Frontend JavaScript functionality
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🚀 Setup Instructions

### Prerequisites

1. **Python 3.7+** installed on your system
2. **MySQL Server** installed and running
3. **MySQL Workbench** (optional but recommended for database management)

### Step 1: Clone/Download the Project

```bash
# If using git
git clone <repository-url>
cd python-sql

# Or download and extract the ZIP file
```

### Step 2: Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Setup MySQL Database

1. **Start MySQL Server** (if not already running)

2. **Create Database** using MySQL Workbench or command line:

   ```sql
   CREATE DATABASE voting_db;
   ```

3. **Update Database Configuration** in `voting_app.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'database': 'voting_db',
       'user': 'root',
       'password': 'YOUR_MYSQL_PASSWORD'  # Change this!
   }
   ```

### Step 4: Run the Application

```bash
# Make sure you're in the project directory
cd python-sql

# Run the Flask application
python voting_app.py
```

The application will start on `http://localhost:5000`

### Step 5: Initialize the Database

1. Open your web browser and go to `http://localhost:5000`
2. Click the **"Setup Database Tables"** button to create all necessary tables
3. Check the system messages section for confirmation

## 📖 How to Use

### 1. Add Candidates

- Fill in candidate information (name, party, position, description)
- Click "Add Candidate"
- Candidates will be available for voting

### 2. Register Voters

- Enter unique voter ID, full name, and email address
- Click "Register Voter"
- Each voter can only be registered once

### 3. Cast Votes

- Enter your registered voter ID
- Select a candidate from the dropdown
- Click "Cast Vote"
- Each voter can only vote once

### 4. View Results

- Click "View Results" to see current election standings
- Results show vote counts and percentages by position

### 5. Monitor System

- View all candidates and their current vote counts
- Check audit logs to see all system activities
- Monitor system messages for real-time feedback

## 🗄️ Database Schema

### Tables Created:

- **candidates**: Stores candidate information and vote counts
- **voters**: Stores registered voter information
- **votes**: Records each vote cast (maintains voting records)
- **audit_logs**: Tracks all system activities

### Key Relationships:

- Votes reference candidates through `candidate_id`
- Voters are tracked by unique `voter_id`
- Audit logs maintain system activity history

## 🔧 Configuration Options

### Database Configuration

Edit the `DB_CONFIG` dictionary in `voting_app.py`:

```python
DB_CONFIG = {
    'host': 'localhost',        # MySQL server host
    'database': 'voting_db',    # Database name
    'user': 'root',            # MySQL username
    'password': 'your_pass'    # MySQL password
}
```

### Adding New Positions

To add new voting positions, edit the HTML dropdown in `voting.html`:

```html
<select id="candidatePosition">
  <option value="">Select Position</option>
  <option value="President">President</option>
  <option value="Mayor">Mayor</option>
  <!-- Add new positions here -->
</select>
```

## 🛡️ Security Features

- **Input Validation**: All user inputs are validated on both frontend and backend
- **SQL Injection Prevention**: Uses parameterized queries
- **Duplicate Vote Prevention**: Database constraints prevent multiple votes per voter
- **Audit Trail**: All actions are logged with timestamps
- **Error Handling**: Graceful error handling with user-friendly messages

## 🐛 Troubleshooting

### Common Issues:

1. **Database Connection Failed**

   - Check if MySQL server is running
   - Verify database credentials in `voting_app.py`
   - Ensure `voting_db` database exists

2. **Module Not Found Error**

   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Port Already in Use**

   - Change the port in `voting_app.py`: `app.run(debug=True, port=5001)`

4. **Template Not Found**
   - Ensure all files are in the same directory
   - Check file names match exactly (case-sensitive)

### Debug Mode

The application runs in debug mode by default. For production:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 📚 Learning Objectives

This project demonstrates:

- **Full-stack web development** with Python and web technologies
- **Database design** and relationships
- **RESTful API** development with Flask
- **Frontend-backend communication** using AJAX
- **Data validation** and error handling
- **Security considerations** in web applications
- **Audit logging** and system monitoring

## 🔄 Future Enhancements

Potential improvements for learning:

- User authentication and authorization
- Vote encryption for enhanced security
- Real-time updates using WebSockets
- Email notifications for voters
- Advanced reporting and analytics
- Mobile app development
- Blockchain integration for vote verification

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages in the browser console
3. Check the system messages section in the application
4. Verify all prerequisites are properly installed

## 📄 License

This project is for educational purposes. Feel free to modify and extend for learning.

---

**Happy Coding! 🚀**
