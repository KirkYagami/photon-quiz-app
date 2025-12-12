import yaml
import re
import html

def parse_gift(content):
    """Parse GIFT format questions with full HTML and special character support"""
    questions = []
    
    # More robust pattern that handles various question formats
    # Matches ::ID:: question text { answers }
    pattern = r'::([^:]+)::\s*([^{]+?)\s*\{([^}]+)\}'
    matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        question_id = match.group(1).strip()
        question_text = match.group(2).strip()
        answers_block = match.group(3).strip()
        
        # Unescape GIFT special characters in question
        question_text = unescape_gift_text(question_text)
        
        # Parse options from answer block
        options = []
        correct_index = None
        
        # Split by lines and process each
        lines = answers_block.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines or lines with only whitespace/tabs
            if not line:
                continue
            
            # Check for correct answer (starts with =)
            if line.startswith('='):
                correct_index = len(options)
                option_text = line[1:].strip()
                option_text = unescape_gift_text(option_text)
                if option_text:  # Only add non-empty options
                    options.append(option_text)
            
            # Check for incorrect answer (starts with ~)
            elif line.startswith('~'):
                option_text = line[1:].strip()
                option_text = unescape_gift_text(option_text)
                if option_text:  # Only add non-empty options
                    options.append(option_text)
        
        # Only add question if it has text, at least 2 options, and a correct answer
        if question_text and len(options) >= 2 and correct_index is not None:
            questions.append({
                'text': question_text,
                'options': options,
                'correct': correct_index
            })
    
    return questions

def unescape_gift_text(text):
    """Unescape GIFT special characters and handle HTML properly"""
    if not text:
        return ""
    
    # First handle GIFT escape sequences
    text = text.replace('\\n', '\n')
    text = text.replace('\\t', '\t')
    text = text.replace('\\\\', '\\')
    text = text.replace('\\:', ':')
    text = text.replace('\\=', '=')
    text = text.replace('\\{', '{')
    text = text.replace('\\}', '}')
    text = text.replace('\\~', '~')
    text = text.replace('\\#', '#')
    text = text.replace('\\"', '"')
    text = text.replace("\\'", "'")
    
    # Don't escape HTML - let it render as-is
    # This allows <!-- comment --> to display correctly
    
    return text.strip()

def parse_yaml(content):
    """Parse YAML format questions with markdown support"""
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format: {str(e)}")
    
    questions = []
    
    if not isinstance(data, list):
        raise ValueError("YAML must contain a list of questions")
    
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            continue
            
        # Check required fields
        if 'question' not in item:
            raise ValueError(f"Question {idx + 1} missing 'question' field")
        if 'options' not in item:
            raise ValueError(f"Question {idx + 1} missing 'options' field")
        if 'correct' not in item:
            raise ValueError(f"Question {idx + 1} missing 'correct' field")
        
        # Validate options
        if not isinstance(item['options'], list) or len(item['options']) < 2:
            raise ValueError(f"Question {idx + 1} must have at least 2 options")
        
        # Validate correct answer index
        if not isinstance(item['correct'], int) or item['correct'] < 0 or item['correct'] >= len(item['options']):
            raise ValueError(f"Question {idx + 1} has invalid 'correct' index")
        
        # Filter out empty options
        options = [str(opt).strip() for opt in item['options'] if str(opt).strip()]
        
        if len(options) < 2:
            raise ValueError(f"Question {idx + 1} must have at least 2 non-empty options")
        
        questions.append({
            'text': str(item['question']),
            'options': options,
            'correct': item['correct']
        })
    
    if not questions:
        raise ValueError("No valid questions found in YAML")
    
    return questions

def validate_questions(questions):
    """Validate parsed questions with detailed error reporting"""
    if not questions:
        return False, "No questions found"
    
    for idx, q in enumerate(questions):
        q_num = idx + 1
        
        # Check question text
        if not q.get('text') or not str(q['text']).strip():
            return False, f"Question {q_num} has no text"
        
        # Check options exist
        if not q.get('options'):
            return False, f"Question {q_num} has no options"
        
        # Check minimum options
        if len(q['options']) < 2:
            return False, f"Question {q_num} has only {len(q['options'])} option(s), need at least 2"
        
        # Check that all options have content
        for opt_idx, opt in enumerate(q['options']):
            if not opt or not str(opt).strip():
                return False, f"Question {q_num}, option {opt_idx + 1} is empty"
        
        # Check correct answer
        if q.get('correct') is None:
            return False, f"Question {q_num} has no correct answer specified"
        
        if q['correct'] < 0 or q['correct'] >= len(q['options']):
            return False, f"Question {q_num} has invalid correct answer index {q['correct']} (only {len(q['options'])} options)"
    
    return True, None