import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "edututor.db"

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        preferred_language TEXT DEFAULT 'en',
        role TEXT DEFAULT 'student'
    )''')
    
    # Learning progress table
    c.execute('''CREATE TABLE IF NOT EXISTS learning_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT NOT NULL,
        score REAL,
        time_spent INTEGER,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Quiz results table
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quiz_topic TEXT NOT NULL,
        score REAL,
        total_questions INTEGER,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Study sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP,
        topic TEXT,
        session_type TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Achievements table
    c.execute('''CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        achievement_type TEXT NOT NULL,
        earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(email, full_name, password_hash, role="student"):
    """Create a new user"""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO users (email, full_name, password_hash, role)
                    VALUES (?, ?, ?, ?)''',
                 (email, full_name, password_hash, role))
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    finally:
        conn.close()

def get_user(email):
    """Get user by email"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def update_user_progress(user_id, topic, score, time_spent):
    """Update user's learning progress"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO learning_progress (user_id, topic, score, time_spent)
                 VALUES (?, ?, ?, ?)''',
              (user_id, topic, score, time_spent))
    conn.commit()
    conn.close()

def get_user_progress(user_id):
    """Get user's learning progress"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT topic, AVG(score) as avg_score, SUM(time_spent) as total_time
                 FROM learning_progress
                 WHERE user_id = ?
                 GROUP BY topic''', (user_id,))
    progress = [dict(row) for row in c.fetchall()]
    conn.close()
    return progress

def record_quiz_result(user_id, quiz_topic, score, total_questions):
    """Record quiz results"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO quiz_results (user_id, quiz_topic, score, total_questions)
                 VALUES (?, ?, ?, ?)''',
              (user_id, quiz_topic, score, total_questions))
    conn.commit()
    conn.close()

def get_quiz_history(user_id):
    """Get user's quiz history"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT quiz_topic, score, total_questions, completed_at
                 FROM quiz_results
                 WHERE user_id = ?
                 ORDER BY completed_at DESC''', (user_id,))
    history = [dict(row) for row in c.fetchall()]
    conn.close()
    return history

def start_study_session(user_id, topic, session_type):
    """Start a new study session"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO study_sessions (user_id, topic, session_type)
                 VALUES (?, ?, ?)''',
              (user_id, topic, session_type))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def end_study_session(session_id):
    """End a study session"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''UPDATE study_sessions
                 SET end_time = CURRENT_TIMESTAMP
                 WHERE id = ?''', (session_id,))
    conn.commit()
    conn.close()

def get_study_stats(user_id):
    """Get user's study statistics"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT 
                    COUNT(DISTINCT topic) as topics_studied,
                    SUM(strftime('%s', end_time) - strftime('%s', start_time)) as total_time,
                    COUNT(DISTINCT DATE(start_time)) as days_studied
                 FROM study_sessions
                 WHERE user_id = ? AND end_time IS NOT NULL''', (user_id,))
    stats = dict(c.fetchone())
    conn.close()
    return stats

def award_achievement(user_id, achievement_type):
    """Award an achievement to a user"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO achievements (user_id, achievement_type)
                 VALUES (?, ?)''',
              (user_id, achievement_type))
    conn.commit()
    conn.close()

def get_user_achievements(user_id):
    """Get user's achievements"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT achievement_type, earned_at
                 FROM achievements
                 WHERE user_id = ?
                 ORDER BY earned_at DESC''', (user_id,))
    achievements = [dict(row) for row in c.fetchall()]
    conn.close()
    return achievements

def get_study_sessions(user_id):
    """Get all study sessions for a user"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM study_sessions WHERE user_id = ? ORDER BY start_time ASC''', (user_id,))
    sessions = [dict(row) for row in c.fetchall()]
    conn.close()
    return sessions

# Initialize database when module is imported
init_db() 