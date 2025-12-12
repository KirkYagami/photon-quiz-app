"""
Database inspector - Shows what's actually stored in your quiz database
Run: python inspect_db.py
"""

import sqlite3
import json
import os

DB_PATH = 'quiz_app.db'

def inspect_database():
    if not os.path.exists(DB_PATH):
        print(f"✗ Database not found at {DB_PATH}")
        print("  Run the app first to create the database: python app.py")
        return
    
    print("=" * 70)
    print("DATABASE INSPECTION")
    print("=" * 70)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all quizzes
    cursor.execute('SELECT * FROM quizzes')
    quizzes = cursor.fetchall()
    
    print(f"\nFound {len(quizzes)} quiz(zes) in database\n")
    
    for quiz in quizzes:
        print(f"\n{'='*70}")
        print(f"Quiz ID: {quiz['id']}")
        print(f"Title: {quiz['title']}")
        print(f"Timer: {quiz['timer_minutes']} minutes")
        print(f"Created: {quiz['created_at']}")
        print(f"{'='*70}")
        
        # Parse questions JSON
        try:
            questions = json.loads(quiz['questions'])
            print(f"\nTotal Questions: {len(questions)}")
            
            # Check each question
            issues = []
            for idx, q in enumerate(questions, 1):
                q_text = q.get('text', '')
                q_opts = q.get('options', [])
                q_correct = q.get('correct', -1)
                
                print(f"\nQuestion {idx}:")
                print(f"  Text: {q_text[:80]}{'...' if len(q_text) > 80 else ''}")
                print(f"  Options: {len(q_opts)}")
                
                if len(q_opts) == 0:
                    issues.append(f"Q{idx}: No options!")
                    print(f"    ✗ ERROR: No options!")
                else:
                    for i, opt in enumerate(q_opts):
                        marker = "✓" if i == q_correct else " "
                        # Show first 50 chars of option
                        opt_preview = str(opt)[:50] + ('...' if len(str(opt)) > 50 else '')
                        print(f"    [{marker}] {i+1}. {opt_preview}")
                        
                        if not opt or str(opt).strip() == '':
                            issues.append(f"Q{idx}, Option {i+1}: Empty!")
                            print(f"        ✗ Empty option!")
                
                if q_correct < 0 or q_correct >= len(q_opts):
                    issues.append(f"Q{idx}: Invalid correct answer index!")
                    print(f"    ✗ ERROR: Invalid correct answer!")
            
            # Summary
            print(f"\n{'-'*70}")
            if issues:
                print(f"⚠ Found {len(issues)} issue(s):")
                for issue in issues:
                    print(f"  - {issue}")
                print("\nRecommendation: Delete and re-upload this quiz")
            else:
                print("✓ All questions look good!")
            print(f"{'-'*70}")
            
        except json.JSONDecodeError as e:
            print(f"✗ ERROR: Could not parse questions JSON: {e}")
    
    # Get recent results
    cursor.execute('SELECT COUNT(*) as count FROM results')
    result_count = cursor.fetchone()['count']
    print(f"\n{'='*70}")
    print(f"Quiz Results: {result_count} total")
    print(f"{'='*70}")
    
    conn.close()
    
    print("\nCommands:")
    print("  - To delete database: rm quiz_app.db (or del quiz_app.db on Windows)")
    print("  - To re-upload quiz: Go to /admin and upload again")
    print("=" * 70)

if __name__ == '__main__':
    inspect_database()