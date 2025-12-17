from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from models.database import Database
from config import Config
from datetime import datetime
import traceback

support = Blueprint('support', __name__, url_prefix='/support')
db = Database()

def get_mail():
    """Get mail instance from current app"""
    from app import mail
    return mail

@support.route('/')
def donate():
    """Support/Donation page"""
    return render_template('support/donate.html')

@support.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form with email functionality"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        if not all([name, email, subject, message]):
            flash('All fields are required', 'error')
            return render_template('support/contact.html')
        
        # Save contact message to database
        try:
            db.save_contact_message(name, email, subject, message)
            
            # Send email notification to admin (if configured)
            if Config.ADMIN_EMAIL and Config.MAIL_USERNAME:
                try:
                    mail = get_mail()
                    msg = Message(
                        subject=f'QuizFlow Contact: {subject}',
                        sender=Config.MAIL_DEFAULT_SENDER,
                        recipients=[Config.ADMIN_EMAIL]
                    )
                    msg.body = f"""
New contact form submission from QuizFlow:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """
                    mail.send(msg)
                    current_app.logger.info(f"Email sent successfully to {Config.ADMIN_EMAIL}")
                except Exception as e:
                    current_app.logger.error(f"Email sending failed: {str(e)}")
                    current_app.logger.error(traceback.format_exc())
                    # Don't fail the entire submission if email fails
            
            flash('Thank you! Your message has been sent successfully. We\'ll get back to you soon!', 'success')
            return redirect(url_for('support.contact'))
            
        except Exception as e:
            current_app.logger.error(f"Database error: {str(e)}")
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
            return render_template('support/contact.html')
    
    return render_template('support/contact.html')

@support.route('/thank-you')
def thank_you():
    """Thank you page after donation"""
    return render_template('support/thank_you.html')