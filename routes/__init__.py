# models/__init__.py
# Empty file - just create this

# routes/__init__.py
# Empty file - just create this

# utils/__init__.py
# Empty file - just create this

# ===== SAMPLE QUIZ FILES =====

# sample_quiz.yaml
"""
- question: "What is the output of the following Python code?\n```python\nprint(2 ** 3)\n```"
  options:
    - "6"
    - "8"
    - "9"
    - "Error"
  correct: 1

- question: "Which CSS property is used to change the text color?"
  options:
    - "color"
    - "text-color"
    - "font-color"
    - "text-style"
  correct: 0

- question: "What does HTML stand for?"
  options:
    - "Hyper Text Markup Language"
    - "High Tech Modern Language"
    - "Home Tool Markup Language"
    - "Hyperlinks and Text Markup Language"
  correct: 0

- question: "Which of the following is NOT a JavaScript data type?"
  options:
    - "String"
    - "Boolean"
    - "Float"
    - "Undefined"
  correct: 2

- question: "What is the correct syntax for a for loop in Python?\n```python\n# Option A\nfor i in range(5):\n    print(i)\n```"
  options:
    - "for i in range(5):"
    - "for (i = 0; i < 5; i++)"
    - "foreach i in range(5)"
    - "for i = 0 to 5"
  correct: 0
"""

# sample_quiz.gift
"""
::Q1:: What is the output of the following Python code?\n```python\nprint(2 ** 3)\n```{
=8
~6
~9
~Error
}

::Q2:: Which CSS property is used to change the text color?{
=color
~text-color
~font-color
~text-style
}

::Q3:: What does HTML stand for?{
=Hyper Text Markup Language
~High Tech Modern Language
~Home Tool Markup Language
~Hyperlinks and Text Markup Language
}

::Q4:: Which of the following is NOT a JavaScript data type?{
=Float
~String
~Boolean
~Undefined
}

::Q5:: What is the correct syntax for a for loop in Python?\n```python\n# Option A\nfor i in range(5):\\n    print(i)\n```{
=for i in range(5)\:
~for (i = 0; i < 5; i++)
~foreach i in range(5)
~for i = 0 to 5
}
"""