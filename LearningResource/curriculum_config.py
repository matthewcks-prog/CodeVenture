"""
Curriculum configuration: single source of truth for learning modules and submodules.

Used by seed_data and tests. Keeps module/submodule/video data DRY and maintainable.
"""

# Structure: list of module dicts. Each module has:
#   name, short_name, description, thumbnail, submodules (list of dicts)
# Each submodule: name, difficulty_level, description, video_name, video_id

MODULES = [
    {
        "name": "Basic Modules",
        "short_name": "basics",
        "description": "Fundamental programming concepts for beginners. Start your coding journey here!",
        "thumbnail": "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400",
        "submodules": [
            {
                "name": "Introduction to Programming",
                "difficulty_level": "Basic",
                "description": "Learn what programming is and why it's important. Understand how computers execute instructions.",
                "video_name": "Intro to Programming",
                "video_id": "zOjov-2OZ0E",
            },
            {
                "name": "Variables and Data Types",
                "difficulty_level": "Basic",
                "description": "Understand how to store and manipulate data using variables. Learn about different data types.",
                "video_name": "Variables and Data Types",
                "video_id": "LKFrQXaoSMQ",
            },
            {
                "name": "Control Flow",
                "difficulty_level": "Basic",
                "description": "Master if statements, loops, and decision-making in your programs.",
                "video_name": "Control Flow",
                "video_id": "Zp5MuPOtsSY",
            },
            {
                "name": "Functions",
                "difficulty_level": "Basic",
                "description": "Learn to write reusable code with functions. Understand parameters and return values.",
                "video_name": "Functions",
                "video_id": "89cGQjB5R4M",
            },
        ],
    },
    {
        "name": "Python Fundamentals",
        "short_name": "python",
        "description": "Deep dive into Python programming. Learn syntax, data structures, and best practices.",
        "thumbnail": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400",
        "submodules": [
            {
                "name": "Python Syntax Basics",
                "difficulty_level": "Basic",
                "description": "Learn Python's clean and readable syntax. Master indentation and basic structure.",
                "video_name": "Python Fundamentals Part 1",
                "video_id": "fWjsdhR3z3c",
            },
            {
                "name": "Lists and Dictionaries",
                "difficulty_level": "Intermediate",
                "description": "Master Python's powerful built-in data structures for organizing information.",
                "video_name": "Python Fundamentals Part 2",
                "video_id": "Gx5qb1uHss4",
            },
        ],
    },
    {
        "name": "Web Development",
        "short_name": "web",
        "description": "Build modern websites and web applications. Learn HTML, CSS, JavaScript, and frameworks.",
        "thumbnail": "https://images.unsplash.com/photo-1547658719-da2b51169166?w=400",
        "submodules": [
            {
                "name": "HTML & CSS Basics",
                "difficulty_level": "Basic",
                "description": "Create and style web pages. Learn the building blocks of the web.",
                "video_name": "Web Development Fundamentals Part 1",
                "video_id": "hu-q2zYwEYs",
            },
            {
                "name": "JavaScript Essentials",
                "difficulty_level": "Intermediate",
                "description": "Add interactivity to your websites. Master the language of the web.",
                "video_name": "Web Development Fundamentals Part 2",
                "video_id": "zFZrkCIc2Oc",
            },
        ],
    },
    {
        "name": "Computational Process Engineering",
        "short_name": "cpe",
        "description": (
            "Apply Python and scientific computing to process engineering: numerical methods, "
            "tabular data, visualization, simulation, and optimisation. Essential for chemical "
            "and process engineers who use code for design and analysis."
        ),
        "thumbnail": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400",
        "submodules": [
            {
                "name": "Python Basics",
                "difficulty_level": "Basic",
                "description": (
                    "Core Python for process engineering: variables, control flow, functions, and "
                    "basic I/O. Build a solid foundation before using scientific libraries."
                ),
                "video_name": "CPE Python Basics",
                "video_id": "LHBE6Q9XlzI",
            },
            {
                "name": "Numerical Computing – NumPy",
                "difficulty_level": "Intermediate",
                "description": (
                    "Efficient arrays and numerical operations with NumPy. Vectorisation, broadcasting, "
                    "linear algebra, and handling real-world process data at scale."
                ),
                "video_name": "CPE Numerical Computing NumPy",
                "video_id": "QUT1VHiLmmI",
            },
            {
                "name": "Tabular Data – Pandas",
                "difficulty_level": "Intermediate",
                "description": (
                    "Load, clean, and analyse tabular data with Pandas. DataFrames, indexing, "
                    "aggregation, and time series for process data and experiments."
                ),
                "video_name": "CPE Tabular Data Pandas",
                "video_id": "2uvysYbKdjM",
            },
            {
                "name": "Plotting & Visualization – Matplotlib",
                "difficulty_level": "Intermediate",
                "description": (
                    "Create publication-quality plots with Matplotlib: time series, scatter plots, "
                    "histograms, and multi-panel figures for reports and dashboards."
                ),
                "video_name": "CPE Plotting Matplotlib",
                "video_id": "wB9C0Mz9gSo",
            },
            {
                "name": "Simulation & Modelling",
                "difficulty_level": "Advanced",
                "description": (
                    "Dynamic and steady-state process models, ODEs, and discrete-event simulation. "
                    "Translate engineering models into code and interpret results."
                ),
                "video_name": "CPE Simulation and Modelling",
                "video_id": "RMIEezW-cG8",
            },
            {
                "name": "Optimisation – SciPy",
                "difficulty_level": "Advanced",
                "description": (
                    "Formulate and solve optimisation problems with SciPy: linear and nonlinear "
                    "programming, curve fitting, and constrained optimisation for process design."
                ),
                "video_name": "CPE Optimisation SciPy",
                "video_id": "G0yP_TM-oag",
            },
        ],
    },
]
