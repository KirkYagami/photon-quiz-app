import markdown
import html as html_module

def render_markdown(text):
    """Convert markdown text to HTML, handling code and HTML entities properly"""
    if not text:
        return ""
    
    # Convert text to string if it isn't already
    text = str(text)
    
    # Check if text contains HTML tags (but not markdown code blocks)
    has_html_tags = ('<' in text and '>' in text and '```' not in text)
    
    # If it's just HTML tags/code without markdown formatting, escape and wrap in code tag
    if has_html_tags and not any(marker in text for marker in ['**', '*', '#', '`', '[', ']']):
        return f'<code>{html_module.escape(text)}</code>'
    
    # If it contains code blocks, process with markdown
    if '```' in text or '`' in text:
        md = markdown.Markdown(
            extensions=[
                'fenced_code',
                'codehilite',
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'linenums': False,
                    'guess_lang': False,
                }
            }
        )
        return md.convert(text)
    
    # For regular text, just return as-is (no markdown processing needed)
    # Replace newlines with <br> tags
    return text.replace('\n', '<br>')

def calculate_score(answers, questions):
    """Calculate quiz score"""
    if not answers or not questions:
        return 0, 0, 0
    
    score = sum(1 for i, ans in enumerate(answers) 
                if i < len(questions) and ans == questions[i]['correct'])
    total = len(questions)
    percentage = round((score / total) * 100, 1) if total > 0 else 0
    
    return score, total, percentage

def format_time(seconds):
    """Format seconds to MM:SS"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"