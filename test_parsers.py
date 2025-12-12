"""
Test script to debug GIFT parser
Run: python test_parser.py
"""

from utils.parsers import parse_gift, validate_questions
import sys

# Test your problematic questions
test_gift = """
::Q3:: How do you declare an HTML5 document type? {
=<!DOCTYPE html>
~<!doctype html>
~<html>
~<head>
~<meta charset\="utf-8">
}

::Q7:: Which HTML element represents a self-contained composition?{
=<article>
~<section>
~<div>
~<post>
}

::Q8:: How do you create a comment in HTML?{
=<!-- comment -->
~// comment
~/* comment */
~# comment
}
"""

print("=" * 70)
print("TESTING GIFT PARSER - DEBUG MODE")
print("=" * 70)

try:
    questions = parse_gift(test_gift)
    print(f"\n✓ Successfully parsed {len(questions)} questions\n")
    
    if not questions:
        print("✗ ERROR: No questions were parsed!")
        print("\nThis could mean:")
        print("  - Question format is incorrect")
        print("  - Special characters need escaping")
        print("  - Curly braces don't match")
        sys.exit(1)
    
    for idx, q in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {idx}:")
        print(f"{'='*60}")
        print(f"Text: {q['text']}")
        print(f"\nOptions ({len(q['options'])}):")
        
        if not q['options']:
            print("  ✗ ERROR: No options found!")
        else:
            for i, opt in enumerate(q['options']):
                marker = "✓ CORRECT" if i == q['correct'] else "  "
                print(f"  [{i}] {marker} '{opt}'")
                if not opt or not opt.strip():
                    print(f"      ⚠ WARNING: Option {i} is empty or whitespace!")
    
    print(f"\n{'='*60}")
    print("VALIDATION CHECK")
    print(f"{'='*60}")
    
    # Validate
    valid, error = validate_questions(questions)
    if valid:
        print("✓ All questions are VALID!")
        print("\nYou can safely upload this quiz.")
    else:
        print(f"✗ Validation FAILED: {error}")
        print("\nPlease fix the errors before uploading.")
    
    print(f"\n{'='*60}")
    
except Exception as e:
    print(f"\n✗ PARSER ERROR: {e}\n")
    import traceback
    print("Full traceback:")
    print("-" * 60)
    traceback.print_exc()
    print("-" * 60)
    print("\nCommon issues:")
    print("  1. Missing curly braces { }")
    print("  2. Unescaped special characters (use \\=, \\:, \\{, \\})")
    print("  3. No = for correct answer")
    print("  4. Empty option lines")
    print("\nExample correct format:")
    print("::Q1:: Question text here?{")
    print("=Correct answer")
    print("~Wrong answer 1")
    print("~Wrong answer 2")
    print("}")
    sys.exit(1)

print("\nTo test your own GIFT file:")
print("  1. Save your GIFT content to a file (e.g., my_quiz.gift)")
print("  2. Modify this script to read from that file")
print("  3. Or paste your GIFT content into the test_gift variable above")
print("=" * 70)