LESSONS = {

    1: {
        "title": "Python Basics",
        "order": 1,
        "validation_rule": "must use print()",
        "sections": {
            "intro": {
                "content": (
                    "Welcome to Python! Python is widely used in web development, AI, data science and automation. "
                    "In this lesson you will learn how programs display output to the screen."
                )
            },
            "outcomes": {
                "content": [
                    "Understand what Python is used for",
                    "Learn how programs display output",
                    "Understand code runs top to bottom"
                ]
            },
            "demo": {
                "code": "In Python, we use a built-in function to show information on the screen.",
                "explanation": (
                    "Programs run instructions step by step from top to bottom. "
                    "When we want the user to see something, we use a special built-in tool called a function. "
                    "Functions take information inside brackets and display results or perform actions. "
                    "In this lesson, you will explore how Python shows output to the screen using this idea."
                )
            },
            "practice": {
                "task": "Write a program that displays your name on the screen."
            },
            "review": {
                "summary": (
                    "Great work completing your first lesson! "
                    "You’ve learned how Python communicates with the user. "
                    "This is the foundation of all programming."
                )
            }
        }
    },

    2: {
        "title": "Variables",
        "order": 2,
        "validation_rule": "must use print and assignment",
        "sections": {
            "intro": {
                "content": "Variables are used to store information so it can be reused later in a program."
            },
            "outcomes": {
                "content": [
                    "Understand what a variable is",
                    "Store information in memory",
                    "Use assignment to store values"
                ]
            },
            "demo": {
                "code": "Programs often need to remember information such as numbers or text.",
                "explanation": (
                    "Instead of rewriting information again and again, programmers store it in something called a variable. "
                    "A variable acts like a labelled container in memory. "
                    "It allows you to store a value and reuse it later in your program whenever needed."
                )
            },
            "practice": {
                "task": "Create a variable called age and display it using output."
            },
            "review": {
                "summary": (
                    "Nice work, you're starting to think like a programmer! "
                    "Variables are one of the most important concepts in programming."
                )
            }
        }
    },

    3: {
        "title": "Data Types",
        "order": 3,
        "validation_rule": "must use string int float",
        "sections": {
            "intro": {
                "content": (
                    "Different types of data are used in programming, such as text, whole numbers and decimal numbers."
                )
            },
            "outcomes": {
                "content": [
                    "Understand different data types",
                    "Recognise text vs numbers",
                    "Understand why types matter"
                ]
            },
            "demo": {
                "code": "Different values in programming behave differently depending on their type.",
                "explanation": (
                    "Not all data is treated the same in programming. "
                    "Text is handled differently from numbers, and numbers can also be split into whole numbers and decimals. "
                    "Understanding how data behaves helps prevent errors and makes your programs more reliable."
                )
            },
            "practice": {
                "task": "Create examples of different types of data: text, whole number, and decimal."
            },
            "review": {
                "summary": (
                    "Good job — you're now handling different types of information like a real developer."
                )
            }
        }
    },

    4: {
        "title": "If Statements",
        "order": 4,
        "validation_rule": "must use if and comparison",
        "sections": {
            "intro": {
                "content": "Programs can make decisions using conditions."
            },
            "outcomes": {
                "content": [
                    "Understand decision making in code",
                    "Use conditions to control flow"
                ]
            },
            "demo": {
                "code": "Programs can choose what to do based on conditions.",
                "explanation": (
                    "Sometimes programs need to behave differently depending on a situation. "
                    "This is called decision making. "
                    "A condition is checked, and depending on whether it is true or false, the program chooses a path to follow."
                )
            },
            "practice": {
                "task": "Write a condition that checks if a number is positive."
            },
            "review": {
                "summary": "Well done — your code can now make decisions."
            }
        }
    },

    5: {
        "title": "Loops",
        "order": 5,
        "validation_rule": "must use loop",
        "sections": {
            "intro": {
                "content": "Loops allow you to repeat actions efficiently."
            },
            "outcomes": {
                "content": [
                    "Understand repetition in code",
                    "Use loops to automate tasks"
                ]
            },
            "demo": {
                "code": "Programs can repeat actions without rewriting code.",
                "explanation": (
                    "When a task needs to happen many times, writing the same code repeatedly becomes inefficient. "
                    "Loops allow a program to repeat instructions automatically, making code shorter and more powerful."
                )
            },
            "practice": {
                "task": "Use a loop to print numbers from 1 to 10."
            },
            "review": {
                "summary": "Nice progress — loops are essential for real programs."
            }
        }
    },

    6: {
        "title": "User Input",
        "order": 6,
        "validation_rule": "must use input",
        "sections": {
            "intro": {
                "content": "Programs can interact with users using input."
            },
            "outcomes": {
                "content": [
                    "Understand user interaction",
                    "Collect information from users"
                ]
            },
            "demo": {
                "code": "Programs can receive information from the user while they run.",
                "explanation": (
                    "So far, programs have been one-way: they show information to the user. "
                    "Input allows the program to go the other way and receive information from the user while the program is running."
                )
            },
            "practice": {
                "task": "Ask the user for their age and store it."
            },
            "review": {
                "summary": "Good job — your program can now interact with users."
            }
        }
    },

    7: {
        "title": "Functions",
        "order": 7,
        "validation_rule": "must use function",
        "sections": {
            "intro": {
                "content": "Functions allow you to organise and reuse code."
            },
            "outcomes": {
                "content": [
                    "Understand reusable code blocks",
                    "Improve code organisation"
                ]
            },
            "demo": {
                "code": "Programs often need to reuse the same instructions multiple times.",
                "explanation": (
                    "Instead of rewriting the same code again and again, programmers group instructions into reusable blocks. "
                    "These blocks can be reused whenever needed, making programs easier to manage and understand."
                )
            },
            "practice": {
                "task": "Create a function that outputs a greeting."
            },
            "review": {
                "summary": "Great work — you're now writing reusable code."
            }
        }
    },

    8: {
        "title": "Lists",
        "order": 8,
        "validation_rule": "must use list",
        "sections": {
            "intro": {
                "content": "Lists store multiple pieces of data together."
            },
            "outcomes": {
                "content": [
                    "Store multiple values",
                    "Understand collections"
                ]
            },
            "demo": {
                "code": "Programs often need to store groups of related items.",
                "explanation": (
                    "Instead of storing values separately, programmers use collections to keep related data together. "
                    "This makes it easier to organise and process multiple values at once."
                )
            },
            "practice": {
                "task": "Create a list of your favourite items."
            },
            "review": {
                "summary": "Nice — you can now store groups of data efficiently."
            }
        }
    },

    9: {
        "title": "Loops + Lists",
        "order": 9,
        "validation_rule": "must use loop",
        "sections": {
            "intro": {
                "content": "You can combine loops with lists to process multiple items."
            },
            "outcomes": {
                "content": [
                    "Loop through collections",
                    "Process multiple items"
                ]
            },
            "demo": {
                "code": "Programs often need to process each item in a collection.",
                "explanation": (
                    "When working with collections of data, programs often need to go through each item one by one. "
                    "Combining repetition with collections allows programs to handle large amounts of data efficiently."
                )
            },
            "practice": {
                "task": "Loop through a list and display each item."
            },
            "review": {
                "summary": "Excellent — you're now combining concepts like a developer."
            }
        }
    },

    10: {
        "title": "Simple Calculator Project",
        "order": 10,
        "validation_rule": "must use input and operators",
        "sections": {
            "intro": {
                "content": "Final challenge: build a simple calculator program."
            },
            "outcomes": {
                "content": [
                    "Combine input, variables and operators",
                    "Build a working program"
                ]
            },
            "demo": {
                "code": "Programs can take input and perform calculations using different operations.",
                "explanation": (
                    "Programs can take values from users and perform mathematical operations on them. "
                    "Different operations allow programs to solve different types of problems, such as adding or dividing values."
                )
            },
            "practice": {
                "task": "Ask the user for two numbers, then display the results of adding, subtracting, multiplying and dividing them."
            },
            "review": {
                "summary": (
                    "Incredible work completing the course! "
                    "You've gone from basics to building a working calculator."
                )
            }
        }
    }
}