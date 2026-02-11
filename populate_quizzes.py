import os
import django
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeVenture.settings')
django.setup()

from LearningResource.models import SubModule
from QuizChallengeSystem.models import Quiz, Question, Choice, Challenge

def create_quiz(submodule_name, quiz_name, questions_data):
    try:
        submodule = SubModule.objects.get(name=submodule_name)
    except SubModule.DoesNotExist:
        print(f"SubModule '{submodule_name}' not found. Skipping quiz creation.")
        return

    # Check if quiz already exists
    if hasattr(submodule, 'quiz'):
        print(f"Quiz for '{submodule_name}' already exists. Skipping.")
        return

    print(f"Creating quiz for {submodule_name}...")
    quiz = Quiz.objects.create(
        name=quiz_name,
        sub_module=submodule,
        deadline=timezone.now() + timezone.timedelta(days=365) # 1 year deadline default
    )

    for q_data in questions_data:
        question = Question.objects.create(
            quiz=quiz,
            text=q_data['text'],
            points=10
        )

        for choice_text, is_correct in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_text,
                is_correct=is_correct
            )
    print(f"Quiz '{quiz_name}' created successfully with {len(questions_data)} questions.")

def create_challenge(name, description, hints, solution_code, std_in, expected_output, sample_output):
    if Challenge.objects.filter(name=name).exists():
        print(f"Challenge '{name}' already exists. Skipping.")
        return

    print(f"Creating challenge '{name}'...")
    Challenge.objects.create(
        name=name,
        description=description,
        hints=hints,
        solution_code=solution_code,
        std_in=std_in,
        expected_output=expected_output,
        sample_output=sample_output
    )
    print(f"Challenge '{name}' created successfully.")

# --- Content Definitions ---

# 1. Introduction to Programming
quiz_intro_data = [
    {
        'text': "What is a computer program?",
        'choices': [
            ("A set of instructions for a computer to perform tasks", True),
            ("A physical part of the computer", False),
            ("The monitor display", False),
            ("A user manual", False)
        ]
    },
    {
        'text': "Which of these is a popular programming language?",
        'choices': [
            ("HTML", False),
            ("Python", True),
            ("English", False),
            ("JPEG", False)
        ]
    },
    {
        'text': "What does 'debugging' mean?",
        'choices': [
            ("Removing dust from the computer", False),
            ("Finding and fixing errors in code", True),
            ("Installing a new game", False),
            ("Writing comments in code", False)
        ]
    },
     {
        'text': "What is the primary function of a compiler?",
        'choices': [
            ("To execute code line by line", False),
            ("To translate high-level code into machine code", True),
            ("To edit text files", False),
            ("To organize files on the disk", False)
        ]
    },
    {
        'text': "Which of the following is NOT a programming paradigm?",
        'choices': [
            ("Object-Oriented", False),
            ("Functional", False),
            ("Hypothetical", True),
            ("Procedural", False)
        ]
    }
]

# 2. Variables and Data Types
quiz_vars_data = [
    {
        'text': "Which data type is used to store text?",
        'choices': [
            ("Integer", False),
            ("String", True),
            ("Boolean", False),
            ("Float", False)
        ]
    },
    {
        'text': "What creates a variable in Python?",
        'choices': [
            ("var x = 10", False),
            ("x = 10", True),
            ("int x = 10", False),
            ("variable x = 10", False)
        ]
    },
    {
        'text': "True or False: A boolean variable can have the value 'Maybe'.",
        'choices': [
            ("True", False),
            ("False", True)
        ]
    },
    {
        'text': "What creates a comment in Python?",
        'choices': [
            ("// Comment", False),
            ("# Comment", True),
            ("/* Comment */", False),
            ("<!-- Comment -->", False)
        ]
    },
    {
        'text': "Which variable name is invalid in Python?",
        'choices': [
            ("my_var", False),
            ("myVar", False),
            ("2myVar", True),
            ("_myVar", False)
        ]
    }
]

# 3. Control Flow
quiz_control_data = [
    {
        'text': "Which keyword is used for conditional checks?",
        'choices': [
            ("loop", False),
            ("if", True),
            ("check", False),
            ("condition", False)
        ]
    },
    {
        'text': "What does 'else' do?",
        'choices': [
            ("It starts a loop", False),
            ("It executes if the 'if' condition is False", True),
            ("It defines a variable", False),
            ("It ends the program", False)
        ]
    },
     {
        'text': "Which loop continues as long as a condition is true?",
        'choices': [
            ("for", False),
            ("while", True),
            ("until", False),
            ("repeat", False)
        ]
    },
    {
        'text': "What does the 'break' statement do in a loop?",
        'choices': [
            ("Skips to the next iteration", False),
            ("Exits the loop immediately", True),
            ("Restarts the loop", False),
            ("Pauses execution", False)
        ]
    },
    {
        'text': "What is the output of: for i in range(3): print(i)",
        'choices': [
            ("1 2 3", False),
            ("0 1 2", True),
            ("0 1 2 3", False),
            ("1 2", False)
        ]
    }
]

# 4. Functions
quiz_funcs_data = [
    {
        'text': "Which keyword defines a function in Python?",
        'choices': [
            ("func", False),
            ("def", True),
            ("function", False),
            ("define", False)
        ]
    },
    {
        'text': "What is a 'parameter'?",
        'choices': [
            ("A variable inside a function", False),
            ("A value passed into a function", True),
            ("The return value", False),
            (" The function name", False)
        ]
    },
    {
        'text': "What does 'return' do?",
        'choices': [
            ("Prints to the screen", False),
            ("Sends a value back from the function", True),
            ("Stops the program", False),
            ("Repeats the function", False)
        ]
    },
    {
        'text': "Can a function call itself?",
        'choices': [
            ("Yes, it's called recursion", True),
            ("No, that causes an error", False),
            ("Only in Java", False),
            ("Only once", False)
        ]
    },
     {
        'text': "What is the scope of a variable defined inside a function?",
        'choices': [
            ("Global", False),
            ("Local", True),
            ("Universal", False),
            ("Module-level", False)
        ]
    }
]

# 5. Python Syntax Basics
quiz_syntax_data = [
    {
        'text': "How do you indent code in Python?",
        'choices': [
            ("Curly braces {}", False),
            ("Whitespace (tabs or spaces)", True),
            ("Semicolons ;", False),
            ("Parentheses ()", False)
        ]
    },
    {
        'text': "What causes a SyntaxError?",
        'choices': [
            ("Dividing by zero", False),
            ("Using an undefined variable", False),
            ("Typing valid code incorrectly (e.g., missing :)", True),
            ("The program running too long", False)
        ]
    },
    {
        'text': "Which of these is essential for Python control structures?",
        'choices': [
            ("Colons (:)", True),
            ("Semicolons (;)", False),
            ("Dollars ($)", False),
            ("Hashes (#)", False)
        ]
    },
    {
        'text': "How do you check if 'a' is equal to 'b'?",
        'choices': [
            ("a = b", False),
            ("a == b", True),
            ("a equals b", False),
            ("a != b", False)
        ]
    },
    {
        'text': "What is the correct way to print 'Hello'?",
        'choices': [
            ("echo 'Hello'", False),
            ("print('Hello')", True),
            ("System.out.println('Hello')", False),
            ("console.log('Hello')", False)
        ]
    }

]

# 6. Lists and Dictionaries
quiz_lists_data = [
    {
        'text': "How do you access the first element of a list 'my_list'?",
        'choices': [
            ("my_list[1]", False),
            ("my_list[0]", True),
            ("my_list.first()", False),
            ("my_list(0)", False)
        ]
    },
    {
        'text': "What kind of brackets do dictionaries use?",
        'choices': [
            ("Square []", False),
            ("Round ()", False),
            ("Curly {}", True),
            ("Angle <>", False)
        ]
    },
    {
        'text': "Which method adds an item to a list?",
        'choices': [
            ("add()", False),
            ("push()", False),
            ("append()", True),
            ("insert_end()", False)
        ]
    },
    {
        'text': "A dictionary stores data in...",
        'choices': [
            ("Ordered index", False),
            ("Key-Value pairs", True),
            ("Linked lists", False),
            ("Binary trees", False)
        ]
    },
    {
        'text': "Are lists mutable (changeable)?",
        'choices': [
            ("Yes", True),
            ("No", False)
        ]
    }
]

# 7. HTML & CSS Basics
quiz_html_data = [
    {
        'text': "What does HTML stand for?",
        'choices': [
            ("Hyper Text Markup Language", True),
            ("High Tech Modern Language", False),
            ("Hyperlink Text Management Language", False),
            ("Home Tool Markup Language", False)
        ]
    },
    {
        'text': "Which tag is used for the largest heading?",
        'choices': [
            ("<head>", False),
            ("<h6>", False),
            ("<h1>", True),
            ("<header>", False)
        ]
    },
    {
        'text': "What does CSS stand for?",
        'choices': [
            ("Creative Style Sheets", False),
            ("Cascading Style Sheets", True),
            ("Computer Style System", False),
            ("Colorful Style Sheets", False)
        ]
    },
    {
        'text': "Which HTML attribute is used to define inline styles?",
        'choices': [
            ("class", False),
            ("style", True),
            ("font", False),
            ("styles", False)
        ]
    },
    {
        'text': "Which selector selects an element by id?",
        'choices': [
            (".", False),
            ("#", True),
            ("*", False),
            ("!", False)
        ]
    }
]

# 8. JavaScript Essentials
quiz_js_data = [
    {
        'text': "Where is JavaScript usually run?",
        'choices': [
            ("In the web browser", True),
            ("On the graphics card", False),
            ("In the database", False),
            ("In the printer", False)
        ]
    },
    {
        'text': "How do you declare a variable in modern JavaScript?",
        'choices': [
            ("v myVar;", False),
            ("let myVar;", True),
            ("variable myVar;", False),
            ("dim myVar;", False)
        ]
    },
    {
        'text': "How do you write 'Hello World' in an alert box?",
        'choices': [
            ("msg('Hello World');", False),
            ("alert('Hello World');", True),
            ("msgBox('Hello World');", False),
            ("alertBox('Hello World');", False)
        ]
    },
    {
        'text': "Which sign is used for concatenation (joining strings)?",
        'choices': [
            ("&", False),
            ("+", True),
            (".", False),
            ("*", False)
        ]
    },
    {
        'text': "Is JavaScript the same as Java?",
        'choices': [
            ("Yes", False),
            ("No, they are completely different", True)
        ]
    }
]


# --- Challenges Data ---

challenges_data = [
    {
        'name': "FizzBuzz",
        'description': "Write a program that prints numbers from 1 to 100. multiple of 3, print 'Fizz'. For multiples of 5, print 'Buzz'. For multiples of both, print 'FizzBuzz'.",
        'hints': "Use the modulus operator % to check for remainders. Check for % 15 first (or both % 3 and % 5).",
        'solution_code': """def fizzbuzz(n):
    results = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            results.append("FizzBuzz")
        elif i % 3 == 0:
            results.append("Fizz")
        elif i % 5 == 0:
            results.append("Buzz")
        else:
            results.append(str(i))
    return "\\n".join(results)

if __name__ == "__main__":
    import sys
    n = int(sys.stdin.read())
    print(fizzbuzz(n))""",
        'std_in': "15",
        'expected_output': "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
        'sample_output': "1\n2\nFizz\n4\nBuzz"
    },
    {
        'name': "Factorial",
        'description': "Write a function to calculate the factorial of a non-negative integer n. The factorial of n is the product of all positive integers less than or equal to n.",
        'hints': "Recursive approach: f(n) = n * f(n-1). Base case: f(0) = 1. Iterative approach: loop from 1 to n and multiply.",
        'solution_code': """def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    import sys
    n = int(sys.stdin.read())
    print(factorial(n))""",
        'std_in': "5",
        'expected_output': "120",
        'sample_output': "120"
    },
    {
        'name': "Palindrome Checker",
        'description': "Write a function that checks if a given string is a palindrome (reads the same forwards and backwards). Return 'True' or 'False'.",
        'hints': "You can use string slicing [::-1] to reverse a string in Python.",
        'solution_code': """def is_palindrome(s):
    cleaned = ''.join(e for e in s if e.isalnum()).lower()
    return cleaned == cleaned[::-1]

if __name__ == "__main__":
    import sys
    s = sys.stdin.read().strip()
    print(is_palindrome(s))""",
        'std_in': "Racecar",
        'expected_output': "True",
        'sample_output': "True"
    },
    {
        'name': "Fibonacci Sequence",
        'description': "Write a function to return the nth Fibonacci number. F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).",
        'hints': "Handle base cases 0 and 1. Use a loop or recursion.",
        'solution_code': """def fibonacci(n):
    if n <= 0: return 0
    elif n == 1: return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    import sys
    n = int(sys.stdin.read())
    print(fibonacci(n))""",
        'std_in': "10",
        'expected_output': "55",
        'sample_output': "55"
    },
     {
        'name': "Prime Checker",
        'description': "Write a number to check if a number n is prime. Print 'Prime' or 'Not Prime'.",
        'hints': "Loop from 2 to sqrt(n). If n is divisible by any, it's not prime.",
        'solution_code': """def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    import sys
    n = int(sys.stdin.read())
    if is_prime(n):
        print("Prime")
    else:
        print("Not Prime")""",
        'std_in': "17",
        'expected_output': "Prime",
        'sample_output': "Prime"
    }
]

# --- Execution ---

if __name__ == '__main__':
    print("Starting content population...")

    # Create Quizzes
    create_quiz("Introduction to Programming", "Intro to Programming Quiz", quiz_intro_data)
    create_quiz("Variables and Data Types", "Variables Quiz", quiz_vars_data)
    create_quiz("Control Flow", "Control Flow Quiz", quiz_control_data)
    create_quiz("Functions", "Functions Quiz", quiz_funcs_data)
    create_quiz("Python Syntax Basics", "Python Syntax Quiz", quiz_syntax_data)
    create_quiz("Lists and Dictionaries", "Data Structures Quiz", quiz_lists_data)
    create_quiz("HTML & CSS Basics", "Web Basics Quiz", quiz_html_data)
    create_quiz("JavaScript Essentials", "JS Essentials Quiz", quiz_js_data)

    # Create Challenges
    for chall in challenges_data:
        create_challenge(
            chall['name'],
            chall['description'],
            chall['hints'],
            chall['solution_code'],
            chall['std_in'],
            chall['expected_output'],
            chall['sample_output']
        )

    print("\nPopulation script finished.")
