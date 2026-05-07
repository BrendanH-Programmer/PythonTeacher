LESSONS = {

    1: {
        "title": "Python Basics",
        "order": 1,
        "sections": {

            "intro": {
                "content": (
                    "Welcome to Python! Python is one of the most beginner-friendly programming languages in the world. "
                    "It is used in web development, artificial intelligence, data science, and automation. "
                    "In this lesson, you will learn how Python communicates information using output."
                )
            },

            "outcomes": {
                "content": [
                    "Understand what Python is used for in the real world",
                    "Learn how to display output using print()",
                    "Understand that code runs line by line"
                ]
            },

            "demo": {
                "code": 'print("Hello World")',
                "explanation": (
                    "The print() function is one of the most important starting tools in Python. "
                    "It sends information from your program to the screen so the user can see it. "
                    "In this example, we are printing the text 'Hello World'. "
                    "Text must always be placed inside quotation marks, and print must use parentheses."
                )
            },

            "practice": {
                "task": (
                    "Try printing your own name using print(). "
                    "Remember: text must be inside quotes and inside parentheses."
                )
            },

            "review": {
                "summary": (
                    "You learned that Python uses print() to display output. "
                    "This is the foundation of all programs, because without output, your program is invisible."
                )
            }
        }
    },

    2: {
        "title": "Variables",
        "order": 2,
        "sections": {

            "intro": {
                "content": (
                    "Variables allow programs to store information so it can be reused later. "
                    "Instead of repeating values, we store them in named containers."
                )
            },

            "outcomes": {
                "content": [
                    "Understand what a variable is",
                    "Learn how to store text and numbers",
                    "Understand assignment using ="
                ]
            },

            "demo": {
                "code": 'name = "Alex"\nage = 20',
                "explanation": (
                    "A variable is like a labelled box that stores data. "
                    "Here, we store the text 'Alex' inside the variable name, and the number 20 inside age. "
                    "The = sign means 'store this value inside the variable' — it does NOT mean equals like in maths."
                )
            },

            "practice": {
                "task": (
                    "Create a variable called age and store your own age in it. "
                    "Then try printing it using print(age)."
                )
            },

            "review": {
                "summary": (
                    "You learned how variables store information. "
                    "This allows programs to remember and reuse data."
                )
            }
        }
    },

    3: {
        "title": "Data Types",
        "order": 3,
        "sections": {

            "intro": {
                "content": (
                    "Python stores different kinds of data in different formats called data types. "
                    "These include text (strings), whole numbers (integers), and decimal numbers (floats)."
                )
            },

            "outcomes": {
                "content": [
                    "Understand strings, integers, and floats",
                    "Recognise differences between types",
                    "Understand why types matter in programming"
                ]
            },

            "demo": {
                "code": 'name = "John"\nage = 25\nheight = 1.75',
                "explanation": (
                    "Each value in Python has a type. "
                    "Text like 'John' is a string (because it is in quotes). "
                    "Whole numbers like 25 are integers. "
                    "Decimal numbers like 1.75 are floats. "
                    "Understanding types is important because Python treats each differently."
                )
            },

            "practice": {
                "task": (
                    "Create three variables: one string, one integer, and one float. "
                    "Try printing each one."
                )
            },

            "review": {
                "summary": (
                    "You learned that Python uses different data types for different kinds of information."
                )
            }
        }
    },

    4: {
        "title": "If Statements",
        "order": 4,
        "sections": {

            "intro": {
                "content": (
                    "If statements allow your program to make decisions. "
                    "They let your code behave differently depending on conditions."
                )
            },

            "outcomes": {
                "content": [
                    "Understand conditional logic",
                    "Use if statements in Python",
                    "Learn comparison operators like >=, >, <"
                ]
            },

            "demo": {
                "code": 'age = 18\nif age >= 18:\n    print("Adult")',
                "explanation": (
                    "This code checks a condition: is age greater than or equal to 18? "
                    "If the condition is true, Python runs the indented code underneath. "
                    "Indentation is very important in Python — it defines what belongs inside the if statement."
                )
            },

            "practice": {
                "task": (
                    "Write an if statement that checks if a number is positive. "
                    "Try testing different values."
                )
            },

            "review": {
                "summary": (
                    "You learned how programs can make decisions using if statements."
                )
            }
        }
    },

    5: {
        "title": "Loops",
        "order": 5,
        "sections": {

            "intro": {
                "content": (
                    "Loops allow you to repeat actions without rewriting code. "
                    "They are essential for efficiency in programming."
                )
            },

            "outcomes": {
                "content": [
                    "Understand repetition in code",
                    "Use for loops",
                    "Understand range()"
                ]
            },

            "demo": {
                "code": 'for i in range(5):\n    print(i)',
                "explanation": (
                    "This loop runs 5 times. "
                    "Each time, i takes a new value starting from 0 up to 4. "
                    "Loops are useful when you need repetition without writing code multiple times."
                )
            },

            "practice": {
                "task": (
                    "Print numbers from 1 to 10 using a loop. "
                    "Think about how range() works."
                )
            },

            "review": {
                "summary": (
                    "You learned how loops help automate repetitive tasks."
                )
            }
        }
    }
}