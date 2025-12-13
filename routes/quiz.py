from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.database import Database
from utils.helpers import calculate_score, render_markdown

quiz = Blueprint('quiz', __name__, url_prefix='/quiz')
db = Database()

@quiz.route('/<int:quiz_id>/start')
def start(quiz_id):
    """Start a quiz"""
    quiz_data = db.get_quiz(quiz_id)
    
    if not quiz_data:
        return redirect(url_for('main.home'))
    
    # Initialize session data
    session[f'quiz_{quiz_id}_answers'] = {}
    session[f'quiz_{quiz_id}_current'] = 0
    session.modified = True
    
    return redirect(url_for('quiz.question', quiz_id=quiz_id, q=0))

@quiz.route('/<int:quiz_id>/question/<int:q>')
def question(quiz_id, q):
    """Display a specific question"""
    quiz_data = db.get_quiz(quiz_id)
    
    if not quiz_data:
        return redirect(url_for('main.home'))
    
    questions = quiz_data['questions']
    total = len(questions)
    
    # Validate question index
    if q < 0 or q >= total:
        return redirect(url_for('quiz.question', quiz_id=quiz_id, q=0))
    
    # Get current answers
    answers = session.get(f'quiz_{quiz_id}_answers', {})
    current_answer = answers.get(str(q))
    
    return render_template(
        'quiz/take.html',
        quiz=quiz_data,
        quiz_id=quiz_id,
        question=questions[q],
        question_index=q,
        total_questions=total,
        current_answer=current_answer,
        render_markdown=render_markdown
    )

@quiz.route('/<int:quiz_id>/submit', methods=['POST'])
def submit_answer(quiz_id):
    """Submit answer for current question"""
    quiz_data = db.get_quiz(quiz_id)
    
    if not quiz_data:
        return jsonify({'error': 'Quiz not found'}), 404
    
    question_index = int(request.form.get('question_index', 0))
    answer = request.form.get('answer')
    
    # Store answer
    answers_key = f'quiz_{quiz_id}_answers'
    if answers_key not in session:
        session[answers_key] = {}
    
    if answer is not None:
        session[answers_key][str(question_index)] = int(answer)
        session.modified = True
    
    # Determine next action
    action = request.form.get('action', 'next')
    total = len(quiz_data['questions'])
    
    if action == 'prev' and question_index > 0:
        return redirect(url_for('quiz.question', quiz_id=quiz_id, q=question_index - 1))
    elif action == 'next' and question_index < total - 1:
        return redirect(url_for('quiz.question', quiz_id=quiz_id, q=question_index + 1))
    elif action == 'submit' or (action == 'next' and question_index >= total - 1):
        return redirect(url_for('quiz.complete', quiz_id=quiz_id))
    
    return redirect(url_for('quiz.question', quiz_id=quiz_id, q=question_index))

@quiz.route('/<int:quiz_id>/complete')
def complete(quiz_id):
    """Complete quiz and show results"""
    quiz_data = db.get_quiz(quiz_id)
    
    if not quiz_data:
        return redirect(url_for('main.home'))
    
    # Get answers
    answers_dict = session.get(f'quiz_{quiz_id}_answers', {})
    questions = quiz_data['questions']
    
    # Convert answers dict to list (with -1 for unanswered)
    answers_list = []
    for i in range(len(questions)):
        answers_list.append(answers_dict.get(str(i), -1))
    
    # Calculate score
    score, total, percentage = calculate_score(answers_list, questions)
    
    # Save result
    db.save_result(quiz_id, quiz_data['title'], score, total, percentage, answers_list)
    
    # Store for review page
    session[f'quiz_{quiz_id}_result'] = {
        'score': score,
        'total': total,
        'percentage': percentage,
        'answers': answers_list
    }
    session.modified = True
    
    # Clear timer from localStorage (will be done on client side)
    return render_template(
        'quiz/result.html',
        quiz=quiz_data,
        quiz_id=quiz_id,
        score=score,
        total=total,
        percentage=percentage,
        clear_timer=True
    )

@quiz.route('/<int:quiz_id>/review')
def review(quiz_id):
    """Review quiz answers"""
    quiz_data = db.get_quiz(quiz_id)
    
    if not quiz_data:
        return redirect(url_for('main.home'))
    
    # Get result from session
    result = session.get(f'quiz_{quiz_id}_result')
    
    if not result:
        return redirect(url_for('main.home'))
    
    questions = quiz_data['questions']
    answers = result['answers']
    
    # Build review data
    review_data = []
    for i, question in enumerate(questions):
        user_answer = answers[i] if i < len(answers) else -1
        correct_answer = question['correct']
        
        review_data.append({
            'number': i + 1,
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': user_answer == correct_answer
        })
    
    return render_template(
        'quiz/review.html',
        quiz=quiz_data,
        quiz_id=quiz_id,
        result=result,
        review_data=review_data,
        render_markdown=render_markdown
    )