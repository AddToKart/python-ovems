from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
from mysql.connector import Error
import datetime

# Create Flask application instance
app = Flask(__name__)

# Database configuration - stores connection details for MySQL
DB_CONFIG = {
    'host': 'localhost',
    'database': 'voting_db',  # Database name for voting system
    'user': 'root',
    'password': 'root'  # Change this to your MySQL password
}

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database.
    This function handles database connection errors gracefully.
    
    Returns:
        connection object if successful, None if failed
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Route handlers - these functions respond to HTTP requests

@app.route('/')
def index():
    """
    Serves the main HTML page when user visits the root URL (/)
    """
    return send_from_directory('.', 'voting.html')

@app.route('/voting.css')
def styles():
    """
    Serves the CSS file for styling the voting interface
    """
    return send_from_directory('.', 'voting.css')

@app.route('/voting.js')
def script():
    """
    Serves the JavaScript file for frontend functionality
    """
    return send_from_directory('.', 'voting.js')

@app.route('/setup-database', methods=['POST'])
def setup_database():
    """
    Creates all necessary tables for the voting system.
    This includes: candidates, voters, votes, and audit_logs tables.
    
    Returns:
        JSON response indicating success or failure
    """
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})
    
    try:
        cursor = connection.cursor()
        
        # Create candidates table - stores information about people running for election
        create_candidates_table = """
        CREATE TABLE IF NOT EXISTS candidates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            party VARCHAR(100),
            position VARCHAR(100) NOT NULL,
            description TEXT,
            vote_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create voters table - stores registered voter information
        create_voters_table = """
        CREATE TABLE IF NOT EXISTS voters (
            id INT AUTO_INCREMENT PRIMARY KEY,
            voter_id VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create votes table - records each vote cast (keeps voting anonymous)
        create_votes_table = """
        CREATE TABLE IF NOT EXISTS votes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            candidate_id INT NOT NULL,
            voter_id VARCHAR(50) NOT NULL,
            position VARCHAR(100) NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        )
        """
        
        # Create audit logs table - tracks all system activities for security
        create_audit_table = """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            action VARCHAR(100) NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Execute all table creation queries
        cursor.execute(create_candidates_table)
        cursor.execute(create_voters_table)
        cursor.execute(create_votes_table)
        cursor.execute(create_audit_table)
        
        # Save changes to database
        connection.commit()
        
        # Log this action for audit purposes
        log_audit_action("Database Setup", "All voting tables created successfully")
        
        return jsonify({'status': 'success', 'message': 'Voting database setup completed!'})
        
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Error setting up database: {e}'})
    finally:
        # Always close database connections to free up resources
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/add-candidate', methods=['POST'])
def add_candidate():
    """
    Adds a new candidate to the election.
    Expects JSON data with: name, party, position, description
    
    Returns:
        JSON response indicating success or failure
    """
    # Get data sent from the frontend
    data = request.json
    name = data.get('name')
    party = data.get('party')
    position = data.get('position')
    description = data.get('description')
    
    # Validate required fields
    if not name or not position:
        return jsonify({'status': 'error', 'message': 'Name and position are required'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})
    
    try:
        cursor = connection.cursor()
        # Insert new candidate into database
        insert_query = """
        INSERT INTO candidates (name, party, position, description) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, party, position, description))
        connection.commit()
        
        # Log this action for audit trail
        log_audit_action("Add Candidate", f"Added candidate: {name} for position: {position}")
        
        return jsonify({'status': 'success', 'message': 'Candidate added successfully!'})
        
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Error adding candidate: {e}'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/register-voter', methods=['POST'])
def register_voter():
    """
    Registers a new voter in the system.
    Expects JSON data with: voter_id, name, email
    
    Returns:
        JSON response indicating success or failure
    """
    data = request.json
    voter_id = data.get('voter_id')
    name = data.get('name')
    email = data.get('email')
    
    # Validate required fields
    if not voter_id or not name or not email:
        return jsonify({'status': 'error', 'message': 'All fields are required'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})
    
    try:
        cursor = connection.cursor()
        # Insert new voter into database
        insert_query = "INSERT INTO voters (voter_id, name, email) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (voter_id, name, email))
        connection.commit()
        
        # Log this action
        log_audit_action("Register Voter", f"Registered voter: {name} with ID: {voter_id}")
        
        return jsonify({'status': 'success', 'message': 'Voter registered successfully!'})
        
    except Error as e:
        # Handle duplicate voter ID or email
        if "Duplicate entry" in str(e):
            return jsonify({'status': 'error', 'message': 'Voter ID or email already exists'})
        return jsonify({'status': 'error', 'message': f'Error registering voter: {e}'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/cast-vote', methods=['POST'])
def cast_vote():
    """
    Records a vote for a candidate.
    Ensures each voter can only vote once per position.
    
    Returns:
        JSON response indicating success or failure
    """
    data = request.json
    voter_id = data.get('voter_id')
    candidate_id = data.get('candidate_id')
    
    if not voter_id or not candidate_id:
        return jsonify({'status': 'error', 'message': 'Voter ID and candidate ID are required'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})
    
    try:
        cursor = connection.cursor()
        
        # Check if voter exists and hasn't voted yet
        cursor.execute("SELECT has_voted FROM voters WHERE voter_id = %s", (voter_id,))
        voter = cursor.fetchone()
        
        if not voter:
            return jsonify({'status': 'error', 'message': 'Voter not found'})
        
        if voter[0]:  # has_voted is True
            return jsonify({'status': 'error', 'message': 'Voter has already cast their vote'})
        
        # Get candidate information
        cursor.execute("SELECT position, name FROM candidates WHERE id = %s", (candidate_id,))
        candidate = cursor.fetchone()
        
        if not candidate:
            return jsonify({'status': 'error', 'message': 'Candidate not found'})
        
        position, candidate_name = candidate
        
        # Record the vote
        cursor.execute(
            "INSERT INTO votes (candidate_id, voter_id, position) VALUES (%s, %s, %s)",
            (candidate_id, voter_id, position)
        )
        
        # Update candidate vote count
        cursor.execute(
            "UPDATE candidates SET vote_count = vote_count + 1 WHERE id = %s",
            (candidate_id,)
        )
        
        # Mark voter as having voted
        cursor.execute(
            "UPDATE voters SET has_voted = TRUE WHERE voter_id = %s",
            (voter_id,)
        )
        
        connection.commit()
        
        # Log this action
        log_audit_action("Cast Vote", f"Voter {voter_id} voted for {candidate_name} ({position})")
        
        return jsonify({'status': 'success', 'message': 'Vote cast successfully!'})
        
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Error casting vote: {e}'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/get-candidates', methods=['GET'])
def get_candidates():
    """
    Retrieves all candidates and their current vote counts.
    Used to display candidates and election results.
    
    Returns:
        JSON response with list of candidates
    """
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})
    
    try:
        cursor = connection.cursor(dictionary=True)  # Returns results as dictionaries
        cursor.execute("SELECT * FROM candidates ORDER BY position, vote_count DESC")
        candidates = cursor.fetchall()
        
        return jsonify({'status': 'success', 'data': candidates})
        
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Error fetching candidates: {e}'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/get-results', methods=['GET'])
def get_results():
    """
    Gets voting results grouped by position.
    Shows vote counts and percentages for each candidate.
    
    Returns:
        JSON response with election results
    """
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get total votes per position for percentage calculation
        cursor.execute("""
            SELECT position, 
                   SUM(vote_count) as total_votes,
                   COUNT(*) as candidate_count
            FROM candidates 
            GROUP BY position
        """)
        position_totals = cursor.fetchall()
        
        # Get detailed results
        cursor.execute("""
            SELECT position, name, party, vote_count,
                   ROUND((vote_count * 100.0 / SUM(vote_count) OVER (PARTITION BY position)), 2) as percentage
            FROM candidates 
            WHERE vote_count > 0
            ORDER BY position, vote_count DESC
        """)
        results = cursor.fetchall()
        
        return jsonify({
            'status': 'success', 
            'results': results,
            'position_totals': position_totals
        })
        
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Error fetching results: {e}'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/get-audit-logs', methods=['GET'])
def get_audit_logs():
    """
    Retrieves recent audit logs for system monitoring.
    Shows the last 50 actions performed in the system.
    
    Returns:
        JSON response with audit log entries
    """
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Database connection failed'})
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM audit_logs 
            ORDER BY timestamp DESC 
            LIMIT 50
        """)
        logs = cursor.fetchall()
        
        return jsonify({'status': 'success', 'data': logs})
        
    except Error as e:
        return jsonify({'status': 'error', 'message': f'Error fetching audit logs: {e}'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def log_audit_action(action, details):
    """
    Helper function to record actions in the audit log.
    This helps track all activities for security and monitoring.
    
    Args:
        action (str): Type of action performed
        details (str): Detailed description of the action
    """
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO audit_logs (action, details) VALUES (%s, %s)",
            (action, details)
        )
        connection.commit()
    except Error as e:
        print(f"Error logging audit action: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
