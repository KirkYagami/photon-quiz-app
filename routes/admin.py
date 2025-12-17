from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import Database
from utils.parsers import parse_gift, parse_yaml, validate_questions
from config import Config

admin = Blueprint('admin', __name__, url_prefix='/admin')
db = Database()

def admin_required(f):
    """Decorator to require admin login"""
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == Config.ADMIN_PASSWORD:
            session['admin'] = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid password', 'error')
    
    return render_template('admin/login.html')

@admin.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.home'))

@admin.route('/')
@admin_required
def dashboard():
    """Admin dashboard"""
    quizzes = db.get_all_quizzes()
    results = db.get_results(limit=20)
    
    # Get unread message count
    messages = db.get_contact_messages(limit=5, unread_only=True)
    unread_count = len(messages)
    
    return render_template('admin/dashboard.html', 
                         quizzes=quizzes, 
                         results=results,
                         unread_count=unread_count)

@admin.route('/messages')
@admin_required
def messages():
    """View contact messages"""
    all_messages = db.get_contact_messages(limit=100)
    return render_template('admin/messages.html', messages=all_messages)

@admin.route('/messages/<int:message_id>/read', methods=['POST'])
@admin_required
def mark_read(message_id):
    """Mark message as read"""
    try:
        db.mark_message_read(message_id)
        flash('Message marked as read', 'success')
    except Exception as e:
        flash('Error updating message', 'error')
    return redirect(url_for('admin.messages'))

@admin.route('/upload', methods=['POST'])
@admin_required
def upload():
    """Upload new quiz"""
    title = request.form.get('title', '').strip()
    format_type = request.form.get('format', 'yaml')
    content = request.form.get('content', '').strip()
    timer_minutes = int(request.form.get('timer_minutes', Config.DEFAULT_QUIZ_TIMER))
    
    if not title:
        flash('Quiz title is required', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if not content:
        flash('Quiz content is required', 'error')
        return redirect(url_for('admin.dashboard'))
    
    try:
        # Parse questions based on format
        if format_type == 'gift':
            questions = parse_gift(content)
        else:
            questions = parse_yaml(content)
        
        # Validate questions
        valid, error_msg = validate_questions(questions)
        if not valid:
            flash(f'Validation error: {error_msg}', 'error')
            return redirect(url_for('admin.dashboard'))
        
        # Create quiz
        quiz_id = db.create_quiz(title, questions, timer_minutes)
        flash(f'Quiz "{title}" created successfully with {len(questions)} questions', 'success')
        
    except Exception as e:
        flash(f'Error parsing quiz: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete/<int:quiz_id>', methods=['POST'])
@admin_required
def delete(quiz_id):
    """Delete a quiz"""
    try:
        db.delete_quiz(quiz_id)
        flash('Quiz deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting quiz: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))