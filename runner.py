from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
import traceback


ERROR_TIPS = {
    "SyntaxError": "Check that quotes, parentheses, colons, and dictionary commas are paired correctly.",
    "IndentationError": "Check that each indented block uses the same four-space indentation.",
    "NameError": "Check the spelling of each variable and make sure it has a value before use.",
    "TypeError": "Check that each operation uses values of compatible types.",
    "KeyError": "Check that the dictionary contains the key you are trying to use.",
    "IndexError": "Check that the list index is within the list's length.",
    "ZeroDivisionError": "A calculation tried to divide by zero. Check the divisor.",
    "ValueError": "Check that the value has the format expected by the operation.",
    "AttributeError": "Check that this value supports the attribute or method you used.",
}

DEFAULT_TIP = "Read the error and check the nearby line of code."

FEEDBACK = {
    "record": "{detail}",
    "burn": "The program ran, but the choice for burn degree {burn_degree} was not correct. Check each branch and its exact text.",
    "pick": "The function ran, but it did not return the highest-scoring name for the test data.",
    "shelf": "Check that the shelf contains every required material and that the count matches the list.",
    "samples": "Check the total and make sure the name with the largest measurement is returned.",
    "triage": "Check the combined-risk condition and each single-risk case.",
    "debug": "One or more repaired scripts did not return the expected result.",
    "boss": "Check the patient limit and compare scores only for eligible dressings.",
}

SAFE_BUILTINS = {
    "print": print,
    "range": range,
    "len": len,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "tuple": tuple,
    "set": set,
    "sum": sum,
    "min": min,
    "max": max,
    "round": round,
    "sorted": sorted,
    "enumerate": enumerate,
    "zip": zip,
    "abs": abs,
    "isinstance": isinstance,
    "reversed": reversed,
}


@dataclass
class Result:
    ok: bool
    output: str
    ns: dict
    error: dict


def run_code(code, prelude="", inject=None):
    namespace = {"__builtins__": SAFE_BUILTINS}
    captured_output = StringIO()
    injected_values = {}
    if inject is not None:
        injected_values = inject

    try:
        with redirect_stdout(captured_output):
            if prelude:
                exec(compile(prelude, "<prelude>", "exec"), namespace, namespace)
            namespace.update(injected_values)
            exec(compile(code, "<learner>", "exec"), namespace, namespace)
        return Result(True, captured_output.getvalue(), namespace, None)
    except Exception as error:
        error_line = getattr(error, "lineno", None)
        trace_frames = traceback.extract_tb(error.__traceback__)
        for frame in trace_frames:
            if frame.filename == "<learner>":
                error_line = frame.lineno

        error_name = type(error).__name__
        error_details = {
            "name": error_name,
            "line": error_line,
            "tip": ERROR_TIPS.get(error_name, DEFAULT_TIP),
        }
        return Result(False, captured_output.getvalue(), namespace, error_details)


def check_level(level, code):
    if "___" in code:
        return False, "Replace every ___ blank before running the program.", ""

    required_words = level.get("must_contain", [])
    for required_word in required_words:
        if required_word not in code:
            message = "Your code needs to use " + required_word + "."
            return False, message, ""

    prelude = level.get("prelude", "")
    base_inject = level.get("base_inject", {})
    first_result = run_code(code, prelude, base_inject)
    if not first_result.ok:
        error = first_result.error
        message = error["name"] + " on line " + str(error["line"]) + ": " + error["tip"]
        return False, message, first_result.output

    custom_check = level.get("custom_check")
    if custom_check is not None:
        custom_passed, custom_message = custom_check(first_result.ns)
        if not custom_passed:
            return False, custom_message, first_result.output

    tests = level.get("tests", [])
    for test_case in tests:
        test_result = run_code(code, prelude, test_case["inject"])
        if not test_result.ok:
            error = test_result.error
            message = error["name"] + " during a test: " + error["tip"]
            return False, message, first_result.output
        actual_value = test_result.ns.get(test_case["variable"])
        if actual_value != test_case["expected"]:
            feedback_message = FEEDBACK.get(level.get("feedback_key"), "Check the result and try another case.")
            if level.get("feedback_key") == "burn":
                details = {"burn_degree": test_case["inject"].get("burn_degree", "")}
                message = feedback_message.format(**details)
            else:
                message = feedback_message
            return False, message, first_result.output

    function_tests = level.get("function_tests", [])
    for test_case in function_tests:
        function_name = test_case["function"]
        learner_function = first_result.ns.get(function_name)
        if not callable(learner_function):
            message = "Define a function named " + function_name + "."
            return False, message, first_result.output
        try:
            actual_value = learner_function(*test_case["arguments"])
        except Exception as error:
            error_name = type(error).__name__
            message = error_name + " in function test: " + ERROR_TIPS.get(error_name, DEFAULT_TIP)
            return False, message, first_result.output
        if actual_value != test_case["expected"]:
            message = FEEDBACK.get(level.get("feedback_key"), "Check the result and try another case.")
            return False, message, first_result.output

    return True, "All checks passed.", first_result.output