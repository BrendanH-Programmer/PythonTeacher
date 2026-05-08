import ast


# =========================================================
# SAFE PARSING
# =========================================================
def parse_tree(code):
    try:
        return ast.parse(code)
    except:
        return None


# =========================================================
# AST HELPERS (DEEP ANALYSIS)
# =========================================================
def get_nodes(tree, node_type):
    return [n for n in ast.walk(tree) if isinstance(n, node_type)]


def has_call(tree, name):
    return any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id == name
        for n in ast.walk(tree)
    )


def has_assignment(tree):
    return any(isinstance(n, ast.Assign) for n in ast.walk(tree))


def assigned_names(tree):
    names = []
    for n in get_nodes(tree, ast.Assign):
        for t in n.targets:
            if isinstance(t, ast.Name):
                names.append(t.id)
    return names


def has_if(tree):
    return any(isinstance(n, ast.If) for n in ast.walk(tree))


def has_loop(tree):
    return any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(tree))


def has_list(tree):
    return any(isinstance(n, ast.List) for n in ast.walk(tree))


def has_function(tree):
    return any(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))


def has_input(tree):
    return has_call(tree, "input")


def has_print(tree):
    return has_call(tree, "print")


def print_has_argument(tree):
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id == "print":
                return len(n.args) > 0
    return False


def print_uses_variable(tree, var):
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id == "print":
                for arg in n.args:
                    if isinstance(arg, ast.Name) and arg.id == var:
                        return True
    return False


def has_type(tree, py_type):
    return any(
        isinstance(n, ast.Constant) and isinstance(n.value, py_type)
        for n in ast.walk(tree)
    )


def uses_operator(tree, op):
    return any(
        isinstance(n, ast.BinOp) and isinstance(n.op, op)
        for n in ast.walk(tree)
    )


def code_str(tree):
    return ast.unparse(tree)


# =========================================================
# LESSON VALIDATION CORE
# =========================================================
def validate_lesson(code, lesson):

    tree = parse_tree(code)

    if tree is None:
        return False

    lesson_id = lesson.get("order")


    # =====================================================
    # LESSON 1: PRINT
    # =====================================================
    if lesson_id == 1:
        return has_print(tree) and print_has_argument(tree)


    # =====================================================
    # LESSON 2: VARIABLES + PRINT AGE
    # must use variable AND print it
    # =====================================================
    if lesson_id == 2:
        return (
            has_assignment(tree)
            and "age" in assigned_names(tree)
            and print_uses_variable(tree, "age")
        )


    # =====================================================
    # LESSON 3: DATA TYPES
    # must include string, int, float
    # =====================================================
    if lesson_id == 3:
        return (
            has_type(tree, str)
            and has_type(tree, int)
            and has_type(tree, float)
        )


    # =====================================================
    # LESSON 4: IF STATEMENTS
    # =====================================================
    if lesson_id == 4:
        return has_if(tree)


    # =====================================================
    # LESSON 5: LOOPS
    # =====================================================
    if lesson_id == 5:
        return has_loop(tree)


    # =====================================================
    # LESSON 6: INPUT (must be AGE)
    # =====================================================
    if lesson_id == 6:
        return has_input(tree) and "age" in code.lower()


    # =====================================================
    # LESSON 7: FUNCTIONS
    # =====================================================
    if lesson_id == 7:
        return has_function(tree)


    # =====================================================
    # LESSON 8: LISTS
    # =====================================================
    if lesson_id == 8:
        return has_list(tree)


    # =====================================================
    # LESSON 9: LOOP + LIST USAGE
    # must iterate over list properly
    # =====================================================
    if lesson_id == 9:
        return has_loop(tree) and has_list(tree)


    # =====================================================
    # LESSON 10: FULL CALCULATOR (STRICT)
    # must support + - * /
    # =====================================================
    if lesson_id == 10:
        return (
            has_input(tree)
            and uses_operator(tree, ast.Add)
            and uses_operator(tree, ast.Sub)
            and uses_operator(tree, ast.Mult)
            and uses_operator(tree, ast.Div)
        )


    # =====================================================
    # SAFE DEFAULT (NO BYPASS)
    # =====================================================
    return False