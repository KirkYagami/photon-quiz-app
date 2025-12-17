from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import Database
from datetime import datetime

support = Blueprint('support', __name__, url_prefix='/support')
db = Database()

@support.route('/')
def donate():
    """Support/Donation page"""
    return render_template('support/donate.html')

@support.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form"""
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
            flash('Thank you! Your message has been sent successfully. We\'ll get back to you soon!', 'success')
            return redirect(url_for('support.contact'))
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
            return render_template('support/contact.html')
    
    return render_template('support/contact.html')

@support.route('/thank-you')
def thank_you():
    """Thank you page after donation"""
    return render_template('support/thank_you.html')