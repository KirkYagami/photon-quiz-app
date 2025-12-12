import sqlite3
import json
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
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
        
        conn.commit()
        conn.close()
    
    def create_quiz(self, title, questions, timer_minutes=30):
        """Create a new quiz"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        questions_json = json.dumps(questions)
        cursor.execute(
            'INSERT INTO quizzes (title, questions, timer_minutes) VALUES (?, ?, ?)',
            (title, questions_json, timer_minutes)
        )
        
        quiz_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return quiz_id
    
    def get_quiz(self, quiz_id):
        """Get a quiz by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM quizzes WHERE id = ?', (quiz_id,))
        row = cursor.fetchone()
        conn.close()
        
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
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM quizzes ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        quizzes = []
        for row in rows:
            quizzes.append({
                'id': row['id'],
                'title': row['title'],
                'questions': json.loads(row['questions']),
                'timer_minutes': row['timer_minutes'],
                'created_at': row['created_at']
            })
        
        return quizzes
    
    def delete_quiz(self, quiz_id):
        """Delete a quiz"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM quizzes WHERE id = ?', (quiz_id,))
        cursor.execute('DELETE FROM results WHERE quiz_id = ?', (quiz_id,))
        
        conn.commit()
        conn.close()
    
    def save_result(self, quiz_id, quiz_title, score, total, percentage, answers):
        """Save quiz result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        answers_json = json.dumps(answers)
        cursor.execute(
            'INSERT INTO results (quiz_id, quiz_title, score, total, percentage, answers) VALUES (?, ?, ?, ?, ?, ?)',
            (quiz_id, quiz_title, score, total, percentage, answers_json)
        )
        
        result_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return result_id
    
    def get_results(self, limit=50):
        """Get recent results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM results ORDER BY taken_at DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'quiz_id': row['quiz_id'],
                'quiz_title': row['quiz_title'],
                'score': row['score'],
                'total': row['total'],
                'percentage': row['percentage'],
                'answers': json.loads(row['answers']),
                'taken_at': row['taken_at']
            })
        
        return results