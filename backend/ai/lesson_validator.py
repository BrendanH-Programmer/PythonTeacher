import ast


# -------------------------
# SAFE PARSE
# -------------------------
def parse_tree(code):
    try:
        return ast.parse(code)
    except:
        return None


# -------------------------
# CHECK: PRINT USAGE
# -------------------------
def has_print_call(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id == "print":
                    return True
    return False


# -------------------------
# CHECK: ASSIGNMENT EXISTS
# -------------------------
def has_assignment(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            return True
    return False


# -------------------------
# CHECK: IF STATEMENT EXISTS
# -------------------------
def has_if_statement(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            return True
    return False


# -------------------------
# MAIN VALIDATOR
# -------------------------
def validate_lesson(code, lesson):

    tree = parse_tree(code)

    if tree is None:
        return False

    rule = lesson.get("validation_rule", "")

    # -------------------------
    # LESSON 1: PRINT
    # -------------------------
    if rule == "must use print()":
        return has_print_call(tree)

    # -------------------------
    # LESSON 2: VARIABLES
    # -------------------------
    if rule == "correct assignment":
        return has_assignment(tree)

    # -------------------------
    # LESSON 4: IF STATEMENTS
    # -------------------------
    if rule == "must use if":
        return has_if_statement(tree)

    # -------------------------
    # DEFAULT FALLBACK
    # -------------------------
    return True