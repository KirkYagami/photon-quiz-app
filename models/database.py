import sqlite3
import json
from datetime import datetime
from config import Config
from contextlib import contextmanager
import threading

class Database:
    _local = threading.local()
    
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """Get thread-safe database connection with context manager"""
        conn = getattr(self._local, 'connection', None)
        if conn is None:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            # Performance optimizations
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('PRAGMA synchronous=NORMAL')
            conn.execute('PRAGMA cache_size=-64000')
            conn.execute('PRAGMA temp_store=MEMORY')
            self._local.connection = conn
        
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    def init_db(self):
        """Initialize database tables with indexes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Quizzes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    questions TEXT NOT NULL,
                    timer_minutes INTEGER DEFAULT 30,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quiz_id INTEGER NOT NULL,
                    quiz_title TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    answers TEXT NOT NULL,
                    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
                )
            ''')
            
            # Contact messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contact_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    read BOOLEAN DEFAULT 0
                )
            ''')
            
            # Create indexes
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_results_quiz_id 
                ON results(quiz_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_results_taken_at 
                ON results(taken_at DESC)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_contact_messages_created_at 
                ON contact_messages(created_at DESC)
            ''')
    
    def create_quiz(self, title, questions, timer_minutes=30):
        """Create a new quiz"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            questions_json = json.dumps(questions)
            cursor.execute(
                'INSERT INTO quizzes (title, questions, timer_minutes) VALUES (?, ?, ?)',
                (title, questions_json, timer_minutes)
            )
            return cursor.lastrowid
    
    def get_quiz(self, quiz_id):
        """Get a quiz by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM quizzes WHERE id = ?', (quiz_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row['id'],
                    'title': row['title'],
                    'questions': json.loads(row['questions']),
                    'timer_minutes': row['timer_minutes'],
                    'created_at': row['created_at']
                }
            return None
    
    def get_all_quizzes(self):
        """Get all quizzes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM quizzes ORDER BY created_at DESC')
            rows = cursor.fetchall()
            
            return [{
                'id': row['id'],
                'title': row['title'],
                'questions': json.loads(row['questions']),
                'timer_minutes': row['timer_minutes'],
                'created_at': row['created_at']
            } for row in rows]
    
    def delete_quiz(self, quiz_id):
        """Delete a quiz and its results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM quizzes WHERE id = ?', (quiz_id,))
            cursor.execute('DELETE FROM results WHERE quiz_id = ?', (quiz_id,))
    
    def save_result(self, quiz_id, quiz_title, score, total, percentage, answers):
        """Save quiz result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            answers_json = json.dumps(answers)
            cursor.execute(
                'INSERT INTO results (quiz_id, quiz_title, score, total, percentage, answers) VALUES (?, ?, ?, ?, ?, ?)',
                (quiz_id, quiz_title, score, total, percentage, answers_json)
            )
            return cursor.lastrowid
    
    def get_results(self, limit=50):
        """Get recent results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM results ORDER BY taken_at DESC LIMIT ?', (limit,))
            rows = cursor.fetchall()
            
            return [{
                'id': row['id'],
                'quiz_id': row['quiz_id'],
                'quiz_title': row['quiz_title'],
                'score': row['score'],
                'total': row['total'],
                'percentage': row['percentage'],
                'answers': json.loads(row['answers']),
                'taken_at': row['taken_at']
            } for row in rows]
    
    def save_contact_message(self, name, email, subject, message):
        """Save contact form message"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                (name, email, subject, message)
            )
            return cursor.lastrowid
    
    def get_contact_messages(self, limit=50, unread_only=False):
        """Get contact messages"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if unread_only:
                cursor.execute('SELECT * FROM contact_messages WHERE read = 0 ORDER BY created_at DESC LIMIT ?', (limit,))
            else:
                cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT ?', (limit,))
            rows = cursor.fetchall()
            
            return [{
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'subject': row['subject'],
                'message': row['message'],
                'created_at': row['created_at'],
                'read': row['read']
            } for row in rows]
    
    def mark_message_read(self, message_id):
        """Mark contact message as read"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE contact_messages SET read = 1 WHERE id = ?', (message_id,))