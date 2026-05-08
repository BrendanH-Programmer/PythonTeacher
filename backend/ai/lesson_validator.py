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
# GENERIC HELPERS
# =========================================================
def get_nodes(tree, node_type):

    return [
        n for n in ast.walk(tree)
        if isinstance(n, node_type)
    ]


def assigned_names(tree):

    names = []

    for node in get_nodes(tree, ast.Assign):

        for target in node.targets:

            if isinstance(target, ast.Name):
                names.append(target.id)

    return names


def has_type(tree, py_type):

    return any(
        isinstance(node, ast.Constant)
        and isinstance(node.value, py_type)
        for node in ast.walk(tree)
    )


# =========================================================
# PRINT HELPERS
# =========================================================
def has_print(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "print":
                    return True

    return False


def print_has_argument(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "print":

                    return len(node.args) > 0

    return False


def print_uses_variable(tree, variable_name):

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "print":

                    for arg in node.args:

                        if isinstance(arg, ast.Name):

                            if arg.id == variable_name:
                                return True

    return False


# =========================================================
# LESSON 1
# DISPLAY NAME
# =========================================================
def valid_name_print(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "print":

                    if len(node.args) == 0:
                        return False

                    arg = node.args[0]

                    # must print text/string
                    if isinstance(arg, ast.Constant):

                        if isinstance(arg.value, str):
                            return True

    return False


# =========================================================
# LESSON 2
# AGE VARIABLE + PRINT
# =========================================================
def valid_age_variable(tree):

    has_age_assignment = False
    has_age_print = False

    for node in ast.walk(tree):

        # age = something
        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    if target.id == "age":
                        has_age_assignment = True

        # print(age)
        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "print":

                    for arg in node.args:

                        if isinstance(arg, ast.Name):

                            if arg.id == "age":
                                has_age_print = True

    return has_age_assignment and has_age_print


# =========================================================
# LESSON 3
# STRING + INT + FLOAT
# =========================================================
def valid_data_types(tree):

    return (
        has_type(tree, str)
        and has_type(tree, int)
        and has_type(tree, float)
    )


# =========================================================
# LESSON 4
# POSITIVE NUMBER CHECK
# =========================================================
def valid_positive_check(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.If):

            test = node.test

            if isinstance(test, ast.Compare):

                # variable > 0
                if (
                    isinstance(test.left, ast.Name)
                    and len(test.comparators) > 0
                    and isinstance(test.comparators[0], ast.Constant)
                    and isinstance(
                        test.comparators[0].value,
                        (int, float)
                    )
                ):

                    if isinstance(
                        test.ops[0],
                        (ast.Gt, ast.GtE)
                    ):

                        return True

    return False


# =========================================================
# LESSON 5
# LOOP PRINTING NUMBERS
# =========================================================
def valid_loop(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.For):

            # must use range(...)
            if not isinstance(node.iter, ast.Call):
                continue

            if not isinstance(node.iter.func, ast.Name):
                continue

            if node.iter.func.id != "range":
                continue

            args = node.iter.args

            # must be range(1, 11)
            if len(args) != 2:
                continue

            if not (
                isinstance(args[0], ast.Constant)
                and args[0].value == 1
            ):
                continue

            if not (
                isinstance(args[1], ast.Constant)
                and args[1].value == 10
            ):
                continue

            # loop variable
            if not isinstance(node.target, ast.Name):
                continue

            loop_var = node.target.id

            # must print(loop_var)
            for child in ast.walk(node):

                if isinstance(child, ast.Call):

                    if isinstance(child.func, ast.Name):

                        if child.func.id == "print":

                            for arg in child.args:

                                if isinstance(arg, ast.Name):

                                    if arg.id == loop_var:
                                        return True

    return False


# =========================================================
# LESSON 6
# AGE INPUT
# =========================================================
def valid_age_input(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            # age = input(...)
            if isinstance(node.value, ast.Call):

                if isinstance(node.value.func, ast.Name):

                    if node.value.func.id == "input":

                        for target in node.targets:

                            if isinstance(target, ast.Name):

                                if target.id == "age":
                                    return True

    return False


# =========================================================
# LESSON 7
# FUNCTION WITH PRINT
# =========================================================
def valid_function(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            for child in ast.walk(node):

                if isinstance(child, ast.Call):

                    if isinstance(child.func, ast.Name):

                        if child.func.id == "print":

                            if len(child.args) > 0:
                                return True

    return False


# =========================================================
# LESSON 8
# LIST CREATION
# =========================================================
def valid_list(tree):

    return any(
        isinstance(node, ast.List)
        for node in ast.walk(tree)
    )


# =========================================================
# LESSON 9
# LOOP THROUGH LIST + PRINT ITEM
# =========================================================
def valid_list_loop(tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.For):

            loop_var = None

            # for item in items
            if isinstance(node.target, ast.Name):
                loop_var = node.target.id

            if not loop_var:
                continue

            # must print(loop_var)
            for child in ast.walk(node):

                if isinstance(child, ast.Call):

                    if isinstance(child.func, ast.Name):

                        if child.func.id == "print":

                            for arg in child.args:

                                if isinstance(arg, ast.Name):

                                    if arg.id == loop_var:
                                        return True

    return False


# =========================================================
# LESSON 10
# FULL CALCULATOR
# =========================================================
def valid_calculator(tree):

    has_input = False

    has_add = False
    has_sub = False
    has_mult = False
    has_div = False

    uses_int_conversion = False

    for node in ast.walk(tree):

        # int(input())
        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "int":

                    if len(node.args) > 0:

                        inner = node.args[0]

                        if isinstance(inner, ast.Call):

                            if (
                                isinstance(inner.func, ast.Name)
                                and inner.func.id == "input"
                            ):

                                uses_int_conversion = True
                                has_input = True

        # operators
        if isinstance(node, ast.BinOp):

            if isinstance(node.op, ast.Add):
                has_add = True

            elif isinstance(node.op, ast.Sub):
                has_sub = True

            elif isinstance(node.op, ast.Mult):
                has_mult = True

            elif isinstance(node.op, ast.Div):
                has_div = True

    return (
        has_input
        and uses_int_conversion
        and has_add
        and has_sub
        and has_mult
        and has_div
    )


# =========================================================
# MAIN VALIDATOR
# =========================================================
def validate_lesson(code, lesson):

    tree = parse_tree(code)

    if tree is None:
        return False

    lesson_id = lesson.get("order")


    # =====================================================
    # LESSON 1
    # =====================================================
    if lesson_id == 1:
        return valid_name_print(tree)


    # =====================================================
    # LESSON 2
    # =====================================================
    if lesson_id == 2:
        return valid_age_variable(tree)


    # =====================================================
    # LESSON 3
    # =====================================================
    if lesson_id == 3:
        return valid_data_types(tree)


    # =====================================================
    # LESSON 4
    # =====================================================
    if lesson_id == 4:
        return valid_positive_check(tree)


    # =====================================================
    # LESSON 5
    # =====================================================
    if lesson_id == 5:
        return valid_loop(tree)


    # =====================================================
    # LESSON 6
    # =====================================================
    if lesson_id == 6:
        return valid_age_input(tree)


    # =====================================================
    # LESSON 7
    # =====================================================
    if lesson_id == 7:
        return valid_function(tree)


    # =====================================================
    # LESSON 8
    # =====================================================
    if lesson_id == 8:
        return valid_list(tree)


    # =====================================================
    # LESSON 9
    # =====================================================
    if lesson_id == 9:
        return valid_list_loop(tree)


    # =====================================================
    # LESSON 10
    # =====================================================
    if lesson_id == 10:
        return valid_calculator(tree)


    # =====================================================
    # SAFE DEFAULT
    # =====================================================
    return False