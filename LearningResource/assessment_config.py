"""
Assessment configuration for curriculum modules: quizzes and coding challenges.

Currently covers:
- Python Fundamentals (quizzes only)
- Web Development (quizzes only)
- Computational Process Engineering (quizzes + coding challenges)
"""

# Submodule name -> { "quiz": {...} } for Python Fundamentals
PYTHON_SUBMODULE_ASSESSMENTS = {
    "Python Syntax Basics": {
        "quiz": {
            "name": "Python Syntax Basics Quiz",
            "questions": [
                {
                    "text": "Which of the following is valid Python syntax for defining a function?",
                    "points": 1,
                    "choices": [
                        {"text": "function my_func():", "is_correct": False},
                        {"text": "def my_func():", "is_correct": True},
                        {"text": "func my_func() ->", "is_correct": False},
                        {"text": "define my_func[]:", "is_correct": False},
                    ],
                },
                {
                    "text": "What does indentation represent in Python?",
                    "points": 1,
                    "choices": [
                        {"text": "It is purely for style and has no effect.", "is_correct": False},
                        {"text": "It marks the start and end of code blocks.", "is_correct": True},
                        {"text": "It is only required inside functions.", "is_correct": False},
                        {"text": "It is only required in comments.", "is_correct": False},
                    ],
                },
                {
                    "text": "Which line correctly prints 'Hello' in Python 3?",
                    "points": 1,
                    "choices": [
                        {"text": "print 'Hello'", "is_correct": False},
                        {"text": "echo('Hello')", "is_correct": False},
                        {"text": "printf('Hello')", "is_correct": False},
                        {"text": "print('Hello')", "is_correct": True},
                    ],
                },
                {
                    "text": "What will happen if you forget the colon at the end of an if statement?",
                    "points": 1,
                    "choices": [
                        {"text": "Python will automatically add it.", "is_correct": False},
                        {"text": "The code will run but skip the if block.", "is_correct": False},
                        {"text": "You will get a SyntaxError.", "is_correct": True},
                        {"text": "It will only warn you, not fail.", "is_correct": False},
                    ],
                },
            ],
        },
    },
    "Lists and Dictionaries": {
        "quiz": {
            "name": "Python Collections Quiz",
            "questions": [
                {
                    "text": "Which literal creates a list in Python?",
                    "points": 1,
                    "choices": [
                        {"text": "{1, 2, 3}", "is_correct": False},
                        {"text": "[1, 2, 3]", "is_correct": True},
                        {"text": "(1, 2, 3)", "is_correct": False},
                        {"text": "list:1,2,3", "is_correct": False},
                    ],
                },
                {
                    "text": "Given my_list = [1, 2, 3], what is my_list[0]?",
                    "points": 1,
                    "choices": [
                        {"text": "0", "is_correct": False},
                        {"text": "1", "is_correct": True},
                        {"text": "2", "is_correct": False},
                        {"text": "IndexError", "is_correct": False},
                    ],
                },
                {
                    "text": "Which option correctly creates a dictionary mapping 'name' to 'Alice'?",
                    "points": 1,
                    "choices": [
                        {"text": "['name' = 'Alice']", "is_correct": False},
                        {"text": "{'name': 'Alice'}", "is_correct": True},
                        {"text": "dict('name', 'Alice')", "is_correct": False},
                        {"text": "('name' => 'Alice')", "is_correct": False},
                    ],
                },
                {
                    "text": "What does my_dict.get('age', 0) do?",
                    "points": 1,
                    "choices": [
                        {"text": "Always raises a KeyError.", "is_correct": False},
                        {"text": "Returns 0 and removes the key 'age'.", "is_correct": False},
                        {"text": "Returns the value for 'age' or 0 if it is missing.", "is_correct": True},
                        {"text": "Creates the key 'age' with value 0.", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


# Submodule name -> { "quiz": {...} } for Web Development
WEB_SUBMODULE_ASSESSMENTS = {
    "HTML & CSS Basics": {
        "quiz": {
            "name": "HTML & CSS Basics Quiz",
            "questions": [
                {
                    "text": "Which HTML tag is used to create a hyperlink?",
                    "points": 1,
                    "choices": [
                        {"text": "<a>", "is_correct": True},
                        {"text": "<link>", "is_correct": False},
                        {"text": "<h1>", "is_correct": False},
                        {"text": "<p>", "is_correct": False},
                    ],
                },
                {
                    "text": "Where is the correct place to link an external CSS file in an HTML document?",
                    "points": 1,
                    "choices": [
                        {"text": "Inside the <body> element", "is_correct": False},
                        {"text": "Inside the <head> element", "is_correct": True},
                        {"text": "At the very end of the file, after </html>", "is_correct": False},
                        {"text": "It does not matter where it goes", "is_correct": False},
                    ],
                },
                {
                    "text": "Which CSS property changes the text color?",
                    "points": 1,
                    "choices": [
                        {"text": "font-style", "is_correct": False},
                        {"text": "background-color", "is_correct": False},
                        {"text": "color", "is_correct": True},
                        {"text": "text-align", "is_correct": False},
                    ],
                },
                {
                    "text": "What does the 'class' attribute in HTML allow you to do?",
                    "points": 1,
                    "choices": [
                        {"text": "Create a JavaScript class.", "is_correct": False},
                        {"text": "Apply CSS styles to one or more elements.", "is_correct": True},
                        {"text": "Define the page title.", "is_correct": False},
                        {"text": "Set the document type.", "is_correct": False},
                    ],
                },
            ],
        },
    },
    "JavaScript Essentials": {
        "quiz": {
            "name": "JavaScript Essentials Quiz",
            "questions": [
                {
                    "text": "Which HTML tag is used to include JavaScript code?",
                    "points": 1,
                    "choices": [
                        {"text": "<js>", "is_correct": False},
                        {"text": "<script>", "is_correct": True},
                        {"text": "<code>", "is_correct": False},
                        {"text": "<javascript>", "is_correct": False},
                    ],
                },
                {
                    "text": "How do you declare a variable that can be reassigned in modern JavaScript?",
                    "points": 1,
                    "choices": [
                        {"text": "const myVar = 1;", "is_correct": False},
                        {"text": "var myVar = 1;", "is_correct": True},
                        {"text": "let myVar = 1;", "is_correct": True},
                        {"text": "Both 'var' and 'let' can be used", "is_correct": False},
                    ],
                },
                {
                    "text": "Which expression correctly compares two values for equality in both value and type?",
                    "points": 1,
                    "choices": [
                        {"text": "a == b", "is_correct": False},
                        {"text": "a = b", "is_correct": False},
                        {"text": "a === b", "is_correct": True},
                        {"text": "a => b", "is_correct": False},
                    ],
                },
                {
                    "text": "What is the result of console.log(typeof([])) in JavaScript?",
                    "points": 1,
                    "choices": [
                        {"text": "'array'", "is_correct": False},
                        {"text": "'object'", "is_correct": True},
                        {"text": "'list'", "is_correct": False},
                        {"text": "'[]'", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


# Submodule name -> { "quiz": {...}, "challenge": {...} } for Computational Process Engineering
CPE_SUBMODULE_ASSESSMENTS = {
    "Python Basics": {
        "quiz": {
            "name": "Python Basics Quiz",
            "questions": [
                {
                    "text": "What is the result of: 3 * 2 ** 2 in Python?",
                    "points": 2,
                    "choices": [
                        {"text": "36", "is_correct": False},
                        {"text": "12", "is_correct": True},
                        {"text": "18", "is_correct": False},
                        {"text": "144", "is_correct": False},
                    ],
                },
                {
                    "text": "After a = [1, 2]; b = a; b.append(3), what is len(a)?",
                    "points": 2,
                    "choices": [
                        {"text": "2", "is_correct": False},
                        {"text": "3", "is_correct": True},
                        {"text": "1", "is_correct": False},
                        {"text": "An error is raised", "is_correct": False},
                    ],
                },
                {
                    "text": "Which expression evaluates to a float in Python 3?",
                    "points": 1,
                    "choices": [
                        {"text": "5 / 2", "is_correct": True},
                        {"text": "5 // 2", "is_correct": False},
                        {"text": "5 % 2", "is_correct": False},
                        {"text": "5 * 2", "is_correct": False},
                    ],
                },
                {
                    "text": "def f(x, L=[]): L.append(x); return L. What is f(1) + f(2)?",
                    "points": 2,
                    "choices": [
                        {"text": "[1, 2]", "is_correct": False},
                        {"text": "[1] + [2]", "is_correct": False},
                        {"text": "[1, 2, 1, 2] or similar (mutable default trap)", "is_correct": True},
                        {"text": "TypeError", "is_correct": False},
                    ],
                },
            ],
        },
        "challenge": {
            "name": "Temperature converter",
            "description": "Read one float from stdin (Celsius). Print the value in Fahrenheit rounded to one decimal. Formula: F = C * 9/5 + 32.",
            "hints": "Use input() and float(). Use round(x, 1) or format for one decimal.",
            "solution_code": "c = float(input())\nprint(round(c * 9 / 5 + 32, 1))",
            "std_in": "25.0",
            "expected_output": "77.0\n",
        },
    },
    "Numerical Computing – NumPy": {
        "quiz": {
            "name": "NumPy Quiz",
            "questions": [
                {
                    "text": "What is np.array([1, 2, 3]) * 2?",
                    "points": 1,
                    "choices": [
                        {"text": "[2, 4, 6]", "is_correct": True},
                        {"text": "[[2], [4], [6]]", "is_correct": False},
                        {"text": "[1, 2, 3, 1, 2, 3]", "is_correct": False},
                        {"text": "Raises an error", "is_correct": False},
                    ],
                },
                {
                    "text": "a = np.array([[1,2],[3,4]]). What does a[:, 0] return?",
                    "points": 2,
                    "choices": [
                        {"text": "array([1, 3])", "is_correct": True},
                        {"text": "array([1, 2])", "is_correct": False},
                        {"text": "array([[1], [3]])", "is_correct": False},
                        {"text": "array([0, 0])", "is_correct": False},
                    ],
                },
                {
                    "text": "Which best describes NumPy broadcasting?",
                    "points": 2,
                    "choices": [
                        {"text": "Smaller array is repeated to match larger shape", "is_correct": True},
                        {"text": "Larger array is cropped to smaller shape", "is_correct": False},
                        {"text": "Only same-shape arrays can be combined", "is_correct": False},
                        {"text": "Broadcasting only applies to 1D arrays", "is_correct": False},
                    ],
                },
                {
                    "text": "np.nan == np.nan evaluates to:",
                    "points": 1,
                    "choices": [
                        {"text": "True", "is_correct": False},
                        {"text": "False", "is_correct": True},
                        {"text": "np.nan", "is_correct": False},
                        {"text": "Raises ValueError", "is_correct": False},
                    ],
                },
            ],
        },
        "challenge": {
            "name": "Vector norm",
            "description": "Read a single line of space-separated floats from stdin. Compute the L2 (Euclidean) norm and print it rounded to 2 decimal places. Use NumPy.",
            "hints": "np.fromstring or np.array with split(); np.linalg.norm.",
            "solution_code": "import numpy as np\nx = np.array(input().split(), dtype=float)\nprint(round(np.linalg.norm(x), 2))",
            "std_in": "3 4",
            "expected_output": "5.0\n",
        },
    },
    "Tabular Data – Pandas": {
        "quiz": {
            "name": "Pandas Quiz",
            "questions": [
                {
                    "text": "After df.dropna(), the original DataFrame df is:",
                    "points": 2,
                    "choices": [
                        {"text": "Unchanged (dropna returns a new DataFrame by default)", "is_correct": True},
                        {"text": "Modified in place", "is_correct": False},
                        {"text": "Deleted", "is_correct": False},
                        {"text": "Replaced with None", "is_correct": False},
                    ],
                },
                {
                    "text": "df.loc[0] and df.iloc[0] are always the same when:",
                    "points": 2,
                    "choices": [
                        {"text": "The index is the default RangeIndex 0,1,2,...", "is_correct": True},
                        {"text": "The DataFrame has exactly one row", "is_correct": False},
                        {"text": "Always; loc and iloc are synonymous", "is_correct": False},
                        {"text": "When the index is sorted", "is_correct": False},
                    ],
                },
                {
                    "text": "Which can cause SettingWithCopyWarning?",
                    "points": 2,
                    "choices": [
                        {"text": "Modifying a slice of a DataFrame without .loc or explicit copy", "is_correct": True},
                        {"text": "Using .loc to assign", "is_correct": False},
                        {"text": "Calling .copy() before modifying", "is_correct": False},
                        {"text": "Reading a column with df['col']", "is_correct": False},
                    ],
                },
                {
                    "text": "df.groupby('A')['B'].mean() returns:",
                    "points": 1,
                    "choices": [
                        {"text": "A Series indexed by unique values of A", "is_correct": True},
                        {"text": "A DataFrame with columns A and B", "is_correct": False},
                        {"text": "A single scalar", "is_correct": False},
                        {"text": "A GroupBy object only", "is_correct": False},
                    ],
                },
            ],
        },
        "challenge": {
            "name": "CSV column sum",
            "description": "Read a CSV from stdin with header. First column is 'id', second is 'value'. Print the sum of the 'value' column as an integer (no decimals).",
            "hints": "pd.read_csv(sys.stdin or io.StringIO(...)); column sum; int().",
            "solution_code": "import pandas as pd\nimport sys\ndf = pd.read_csv(sys.stdin)\nprint(int(df['value'].sum()))",
            "std_in": "id,value\n1,10\n2,20\n3,15",
            "expected_output": "45\n",
        },
    },
    "Plotting & Visualization – Matplotlib": {
        "quiz": {
            "name": "Matplotlib Quiz",
            "questions": [
                {
                    "text": "In matplotlib, the 'figure' object represents:",
                    "points": 1,
                    "choices": [
                        {"text": "The entire figure (window or image)", "is_correct": True},
                        {"text": "A single subplot", "is_correct": False},
                        {"text": "The legend", "is_correct": False},
                        {"text": "The title only", "is_correct": False},
                    ],
                },
                {
                    "text": "plt.show() in a script:",
                    "points": 2,
                    "choices": [
                        {"text": "Displays the figure and blocks until the window is closed", "is_correct": True},
                        {"text": "Saves the figure to disk", "is_correct": False},
                        {"text": "Clears the current figure", "is_correct": False},
                        {"text": "Does nothing in non-interactive mode", "is_correct": False},
                    ],
                },
                {
                    "text": "To get an axes object with fig, ax = plt.subplots(2, 2), ax is:",
                    "points": 2,
                    "choices": [
                        {"text": "A 2x2 numpy array of Axes", "is_correct": True},
                        {"text": "A single Axes", "is_correct": False},
                        {"text": "A list of 4 Axes", "is_correct": False},
                        {"text": "The Figure object", "is_correct": False},
                    ],
                },
                {
                    "text": "Which backend is typically used for saving to PNG in headless environments?",
                    "points": 1,
                    "choices": [
                        {"text": "Agg", "is_correct": True},
                        {"text": "TkAgg", "is_correct": False},
                        {"text": "GTK", "is_correct": False},
                        {"text": "Inline", "is_correct": False},
                    ],
                },
            ],
        },
        "challenge": {
            "name": "Plot and save",
            "description": "Create a single plot: x = [1,2,3], y = [2,4,6]. Plot y vs x as a line, set title 'Line'. Save to 'plot.png' (no display). Use a non-interactive backend so no window is required.",
            "hints": "import matplotlib; matplotlib.use('Agg'); plt.plot; plt.title; plt.savefig.",
            "solution_code": "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nplt.plot([1,2,3], [2,4,6])\nplt.title('Line')\nplt.savefig('plot.png')",
            "std_in": "",
            "expected_output": "",
        },
    },
    "Simulation & Modelling": {
        "quiz": {
            "name": "Simulation & Modelling Quiz",
            "questions": [
                {
                    "text": "For a first-order ODE dy/dt = -k*y, the solution y(t) is:",
                    "points": 2,
                    "choices": [
                        {"text": "Exponential decay: y0 * exp(-k*t)", "is_correct": True},
                        {"text": "Linear: y0 - k*t", "is_correct": False},
                        {"text": "Sinusoidal", "is_correct": False},
                        {"text": "Constant", "is_correct": False},
                    ],
                },
                {
                    "text": "solve_ivp from SciPy returns an object whose 't' attribute is:",
                    "points": 2,
                    "choices": [
                        {"text": "Array of time points at which solution was evaluated", "is_correct": True},
                        {"text": "The initial time only", "is_correct": False},
                        {"text": "The derivative dy/dt", "is_correct": False},
                        {"text": "A callable function", "is_correct": False},
                    ],
                },
                {
                    "text": "In discrete-event simulation, 'event' typically means:",
                    "points": 1,
                    "choices": [
                        {"text": "A point in time when state or logic changes", "is_correct": True},
                        {"text": "Any random number draw", "is_correct": False},
                        {"text": "The end of the simulation", "is_correct": False},
                        {"text": "A single iteration of a loop", "is_correct": False},
                    ],
                },
                {
                    "text": "Numerical instability in ODE solvers often appears as:",
                    "points": 2,
                    "choices": [
                        {"text": "Oscillating or exploding values when step size is too large", "is_correct": True},
                        {"text": "Slower execution only", "is_correct": False},
                        {"text": "Immediate ValueError", "is_correct": False},
                        {"text": "Correct but delayed results", "is_correct": False},
                    ],
                },
            ],
        },
        "challenge": {
            "name": "Euler step",
            "description": "Read y0, k, dt, n from stdin (one per line, floats). Simulate n steps of dy/dt = -k*y using Euler method: y_{i+1} = y_i - k*y_i*dt. Print the final y value rounded to 4 decimals.",
            "hints": "Loop n times; y = y - k*y*dt; round(y, 4).",
            "solution_code": "y = float(input())\nk = float(input())\ndt = float(input())\nn = int(float(input()))\nfor _ in range(n):\n    y = y - k * y * dt\nprint(round(y, 4))",
            "std_in": "1.0\n1.0\n0.01\n100",
            "expected_output": "0.3660\n",
        },
    },
    "Optimisation – SciPy": {
        "quiz": {
            "name": "SciPy Optimisation Quiz",
            "questions": [
                {
                    "text": "minimize(fun, x0) with no constraints finds:",
                    "points": 1,
                    "choices": [
                        {"text": "A local minimum (not necessarily global)", "is_correct": True},
                        {"text": "Always the global minimum", "is_correct": False},
                        {"text": "The gradient at x0", "is_correct": False},
                        {"text": "The maximum of fun", "is_correct": False},
                    ],
                },
                {
                    "text": "For curve_fit(f, xdata, ydata), f must:",
                    "points": 2,
                    "choices": [
                        {"text": "Take (x, *params) and return model values", "is_correct": True},
                        {"text": "Take only x", "is_correct": False},
                        {"text": "Return residuals (ydata - model)", "is_correct": False},
                        {"text": "Be a linear function only", "is_correct": False},
                    ],
                },
                {
                    "text": "Equality constraint g(x)=0 in minimize is passed as:",
                    "points": 2,
                    "choices": [
                        {"text": "constraints={'type': 'eq', 'fun': g} (for SLSQP/trust-constr)", "is_correct": True},
                        {"text": "bounds=(0, None)", "is_correct": False},
                        {"text": "args=(g,)", "is_correct": False},
                        {"text": "equality=g", "is_correct": False},
                    ],
                },
                {
                    "text": "Which method is suitable for bounded unconstrained minimization?",
                    "points": 1,
                    "choices": [
                        {"text": "L-BFGS-B", "is_correct": True},
                        {"text": "Powell (ignores bounds)", "is_correct": False},
                        {"text": "CG (no bounds support)", "is_correct": False},
                        {"text": "Nelder-Mead with bounds in fun", "is_correct": False},
                    ],
                },
            ],
        },
        "challenge": {
            "name": "Minimize quadratic",
            "description": "Minimize f(x) = (x - 2)**2 + 1 over x. Use scipy.optimize.minimize with initial guess x0=0. Print the optimal x rounded to 2 decimals.",
            "hints": "Define fun(x); minimize(fun, [0]); result.x[0].",
            "solution_code": "from scipy.optimize import minimize\nf = lambda x: (x[0] - 2)**2 + 1\nr = minimize(f, [0.0])\nprint(round(r.x[0], 2))",
            "std_in": "",
            "expected_output": "2.0\n",
        },
    },
}
