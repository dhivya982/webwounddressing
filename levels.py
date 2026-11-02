AUTHOR = "(add name)"


def check_dressing_record(namespace):
    dressing = namespace.get("dressing")
    if not isinstance(dressing, dict):
        return False, "Create a dictionary named dressing."

    required_properties = ["absorbency", "antibacterial", "cost"]
    for property_name in required_properties:
        if property_name not in dressing:
            return False, "Add the " + property_name + " property to dressing."
        property_value = dressing[property_name]
        if not isinstance(property_value, int):
            return False, "Use whole numbers from 1 to 10 for each property."
        if property_value < 1 or property_value > 10:
            return False, "Use whole numbers from 1 to 10 for each property."

    return True, "Your dressing record has three whole-number properties from 1 to 10."


def make_materials_prelude():
    from materials_b import DRESSINGS, WEIGHTS

    prelude = "dressings = " + repr(DRESSINGS) + "\n"
    prelude += "weights = " + repr(WEIGHTS) + "\n"
    prelude += "def score(d):\n"
    prelude += "    absorbency_points = d['absorbency'] * weights['absorbency']\n"
    prelude += "    antibacterial_points = d['antibacterial'] * weights['antibacterial']\n"
    prelude += "    cost_points = d['cost'] * weights['cost']\n"
    prelude += "    return absorbency_points + antibacterial_points - cost_points\n"
    return prelude


LEVELS = [
    {
        "number": 1,
        "title": "Record a Dressing",
        "concept": "Variables and dictionaries",
        "story": "A burn patient is being assessed in a classroom case, and the care team records sample dressing properties.",
        "lesson": "A variable gives a value a name. A dictionary stores related values under keys, such as absorbency and cost.",
        "task": "Complete the dressing dictionary. Replace each ___ with a whole number from 1 to 10.",
        "starter": "dressing = {\n    'absorbency': ___,\n    'antibacterial': ___,\n    'cost': ___,\n}\nprint(dressing)",
        "hint": "Use a number such as 5 after each colon. Keep the quotes around each property name.",
        "solution": "dressing = {\n    'absorbency': 7,\n    'antibacterial': 6,\n    'cost': 4,\n}\nprint(dressing)",
        "custom_check": check_dressing_record,
        "feedback_key": "record",
    },
    {
        "number": 2,
        "title": "Choose by Burn Degree",
        "concept": "if, elif, and else",
        "story": "A patient in a training case has a burn-degree label. Use branching logic to return the requested classroom label.",
        "lesson": "An if statement checks the first condition. elif checks another condition when the first is false. else handles the remaining cases.",
        "task": "Use burn_degree to set dressing_choice: degree 1 selects Hydrogel, degree 2 selects Hydrocolloid, and all other values select Refer to doctor.",
        "starter": "if burn_degree == ___:\n    dressing_choice = 'Hydrogel'\nelif burn_degree == ___:\n    dressing_choice = 'Hydrocolloid'\nelse:\n    dressing_choice = 'Refer to doctor'\nprint(dressing_choice)",
        "hint": "The injected variable is named burn_degree. Compare it with 1 and 2, and assign the exact requested text to dressing_choice.",
        "solution": "if burn_degree == 1:\n    dressing_choice = 'Hydrogel'\nelif burn_degree == 2:\n    dressing_choice = 'Hydrocolloid'\nelse:\n    dressing_choice = 'Refer to doctor'\nprint(dressing_choice)",
        "must_contain": ["if", "elif", "else"],
        "base_inject": {"burn_degree": 1},
        "tests": [
            {"inject": {"burn_degree": 1}, "variable": "dressing_choice", "expected": "Hydrogel"},
            {"inject": {"burn_degree": 2}, "variable": "dressing_choice", "expected": "Hydrocolloid"},
            {"inject": {"burn_degree": 3}, "variable": "dressing_choice", "expected": "Refer to doctor"},
            {"inject": {"burn_degree": 0}, "variable": "dressing_choice", "expected": "Refer to doctor"},
        ],
        "feedback_key": "burn",
    },
    {
        "number": 3,
        "title": "The Material Shelf",
        "concept": "Lists, append, and len",
        "story": "A patient needs a dressing in a classroom scenario, and a lab assistant checks which materials are on the shelf.",
        "lesson": "A list keeps items in order. append adds an item to the end, and len counts how many items are in the list.",
        "task": "Finish the materials list, add Chitosan, and store the number of materials in shelf_count.",
        "starter": "materials = ['Hydrogel', 'Alginate']\nmaterials.append(___)\nshelf_count = ___\nprint(materials)\nprint(shelf_count)",
        "hint": "Append the material name as a string, then call len with the list name.",
        "solution": "materials = ['Hydrogel', 'Alginate']\nmaterials.append('Chitosan')\nshelf_count = len(materials)\nprint(materials)\nprint(shelf_count)",
        "must_contain": ["append", "len"],
        "tests": [
            {"inject": {}, "variable": "shelf_count", "expected": 3},
            {"inject": {}, "variable": "materials", "expected": ["Hydrogel", "Alginate", "Chitosan"]},
        ],
        "custom_check": None,
        "feedback_key": "shelf",
    },
    {
        "number": 4,
        "title": "Test Every Sample",
        "concept": "For loops, totals, and finding a maximum",
        "story": "A technician is comparing absorbency measurements for samples prepared for a patient's classroom case.",
        "lesson": "A for loop processes each dictionary entry. A running total adds measurements, while a saved maximum keeps the largest value and its name.",
        "task": "Write summarize_samples(samples). Return a dictionary with total_absorbency and highest_name.",
        "starter": "",
        "hint": "Start the total at zero. Track the highest value and its name while looping through samples.",
        "solution": "def summarize_samples(samples):\n    total_absorbency = 0\n    highest_name = None\n    highest_value = None\n    for sample_name in samples:\n        current_value = samples[sample_name]['absorbency']\n        total_absorbency = total_absorbency + current_value\n        if highest_value is None or current_value > highest_value:\n            highest_value = current_value\n            highest_name = sample_name\n    result = {'total_absorbency': total_absorbency, 'highest_name': highest_name}\n    return result\n\nprint(summarize_samples(samples))",
        "must_contain": ["for"],
        "base_inject": {
            "samples": {
                "Sample A": {"absorbency": 4},
                "Sample B": {"absorbency": 9},
                "Sample C": {"absorbency": 6},
            }
        },
        "function_tests": [
            {
                "function": "summarize_samples",
                "arguments": [{"A": {"absorbency": 2}, "B": {"absorbency": 8}}],
                "expected": {"total_absorbency": 10, "highest_name": "B"},
            },
            {
                "function": "summarize_samples",
                "arguments": [{"Only": {"absorbency": 3}}],
                "expected": {"total_absorbency": 3, "highest_name": "Only"},
            },
            {
                "function": "summarize_samples",
                "arguments": [{}],
                "expected": {"total_absorbency": 0, "highest_name": None},
            },
        ],
        "bonus": {
            "title": "Bonus: count high-absorbency samples",
            "task": "Write count_high(samples, minimum) to return how many samples meet or exceed the minimum.",
            "starter": "",
            "solution": "def count_high(samples, minimum):\n    high_count = 0\n    for sample_name in samples:\n        if samples[sample_name]['absorbency'] >= minimum:\n            high_count = high_count + 1\n    return high_count",
            "function_tests": [
                {
                    "function": "count_high",
                    "arguments": [{"A": {"absorbency": 2}, "B": {"absorbency": 8}}, 5],
                    "expected": 1,
                }
            ],
        },
        "feedback_key": "samples",
    },
    {
        "number": 5,
        "title": "Pick the Best Dressing",
        "concept": "Functions and return values",
        "story": "A burn patient has several candidate dressing samples, and the materials team needs a repeatable comparison.",
        "lesson": "A function accepts information through parameters and sends a result back with return. A loop can compare every candidate.",
        "task": "Write pick_best(dressings) to return the name with the highest score. Use the provided score function.",
        "starter": "",
        "hint": "Keep the current best name and score. Update both when you find a larger score.",
        "solution": "def pick_best(dressings):\n    best_name = None\n    best_score = None\n    for dressing_name in dressings:\n        current_score = score(dressings[dressing_name])\n        if best_score is None or current_score > best_score:\n            best_name = dressing_name\n            best_score = current_score\n    return best_name\n\nprint(pick_best(dressings))",
        "must_contain": ["def pick_best", "return"],
        "prelude": make_materials_prelude(),
        "function_tests": [
            {
                "function": "pick_best",
                "arguments": [
                    {
                        "First": {"absorbency": 10, "antibacterial": 10, "cost": 1},
                        "Second": {"absorbency": 1, "antibacterial": 1, "cost": 10},
                    }
                ],
                "expected": "First",
            },
            {
                "function": "pick_best",
                "arguments": [
                    {
                        "North": {"absorbency": 1, "antibacterial": 1, "cost": 10},
                        "South": {"absorbency": 10, "antibacterial": 10, "cost": 1},
                    }
                ],
                "expected": "South",
            },
        ],
        "feedback_key": "pick",
    },
    {
        "number": 6,
        "title": "Smart Triage",
        "concept": "and, or, and nested if statements",
        "story": "A training case records whether infection is present and whether exudate is high.",
        "lesson": "and requires both conditions to be true. or requires at least one. A nested if lets one decision contain a second decision.",
        "task": "Write triage_patient(patient). Return Refer to clinician when infected and exudate is high, Close monitoring when either is true, otherwise Routine review.",
        "starter": "",
        "hint": "Check the combined high-risk condition first. In the other branch, use a nested if for the one-risk case.",
        "solution": "def triage_patient(patient):\n    if patient['infected'] and patient['exudate_level'] == 'high':\n        return 'Refer to clinician'\n    else:\n        if patient['infected'] or patient['exudate_level'] == 'high':\n            return 'Close monitoring'\n        else:\n            return 'Routine review'\n\nprint(triage_patient(patient))",
        "must_contain": ["def triage_patient", "and", "or"],
        "base_inject": {"patient": {"infected": True, "exudate_level": "high"}},
        "function_tests": [
            {
                "function": "triage_patient",
                "arguments": [{"infected": True, "exudate_level": "high"}],
                "expected": "Refer to clinician",
            },
            {
                "function": "triage_patient",
                "arguments": [{"infected": False, "exudate_level": "high"}],
                "expected": "Close monitoring",
            },
            {
                "function": "triage_patient",
                "arguments": [{"infected": False, "exudate_level": "low"}],
                "expected": "Routine review",
            },
        ],
        "bonus": {
            "title": "Bonus: explain the triage result",
            "task": "Write triage_note(patient) to return a short explanation for the selected category.",
            "starter": "",
            "solution": "def triage_note(patient):\n    if patient['infected'] and patient['exudate_level'] == 'high':\n        return 'Both risk signals are present'\n    else:\n        if patient['infected'] or patient['exudate_level'] == 'high':\n            return 'One risk signal is present'\n        else:\n            return 'Neither risk signal is present'",
            "function_tests": [
                {
                    "function": "triage_note",
                    "arguments": [{"infected": False, "exudate_level": "low"}],
                    "expected": "Neither risk signal is present",
                }
            ],
        },
        "feedback_key": "triage",
    },
    {
        "number": 7,
        "title": "Fix the Broken Lab",
        "concept": "Debugging syntax and logic errors",
        "story": "Three lab notebook scripts in a patient's sample report were damaged during a copy. Repair them before the class review.",
        "lesson": "A missing colon is a syntax error. A misspelled variable causes a name error. A wrong comparison can produce a valid but incorrect result.",
        "task": "Repair all three scripts: count usable samples, return a dressing name, and find the largest measurement.",
        "starter": "def count_usable(samples):\n    usable_count = 0\n    for sample in samples:\n        if sample['usable'] == True\n            usable_count = usable_count + 1\n    return usable_count\n\ndef get_dressing_name(dressing):\n    dressing_name = dressing['name']\n    return dressing_nam\n\ndef find_largest(values):\n    largest_value = values[0]\n    for value in values:\n        if value < largest_value:\n            largest_value = value\n    return largest_value",
        "hint": "Check the line ending the if condition, compare every name carefully, and make sure the maximum comparison keeps the larger number.",
        "solution": "def count_usable(samples):\n    usable_count = 0\n    for sample in samples:\n        if sample['usable'] == True:\n            usable_count = usable_count + 1\n    return usable_count\n\ndef get_dressing_name(dressing):\n    dressing_name = dressing['name']\n    return dressing_name\n\ndef find_largest(values):\n    largest_value = values[0]\n    for value in values:\n        if value > largest_value:\n            largest_value = value\n    return largest_value",
        "function_tests": [
            {
                "function": "count_usable",
                "arguments": [[{"usable": True}, {"usable": False}, {"usable": True}]],
                "expected": 2,
            },
            {
                "function": "get_dressing_name",
                "arguments": [{"name": "Alginate"}],
                "expected": "Alginate",
            },
            {
                "function": "find_largest",
                "arguments": [[4, 9, 2]],
                "expected": 9,
            },
            {
                "function": "count_usable",
                "arguments": [[{"usable": False}]],
                "expected": 0,
            },
            {
                "function": "get_dressing_name",
                "arguments": [{"name": "Hydrogel"}],
                "expected": "Hydrogel",
            },
            {
                "function": "find_largest",
                "arguments": [[-8, -3, -11]],
                "expected": -3,
            },
        ],
        "feedback_key": "debug",
    },
    {
        "number": 8,
        "title": "BOSS: Heal the Burn",
        "concept": "Combining functions, loops, and patient data",
        "story": "A simulated patient record includes a spending limit. Build a function that selects the highest-scoring eligible sample dressing.",
        "lesson": "A function can combine patient data with a collection of materials. Test it with different patient records so it handles more than one case.",
        "task": "Write heal_burn(patient). Return the name of the highest-scoring dressing whose cost is within patient['max_cost']; return Refer to clinician if none qualify.",
        "starter": "",
        "hint": "Loop through all dressings. Only compare scores for items that meet the patient's cost limit.",
        "solution": "def heal_burn(patient):\n    best_name = None\n    best_score = None\n    for dressing_name in dressings:\n        dressing_data = dressings[dressing_name]\n        if dressing_data['cost'] <= patient['max_cost']:\n            current_score = score(dressing_data)\n            if best_score is None or current_score > best_score:\n                best_name = dressing_name\n                best_score = current_score\n    if best_name is None:\n        return 'Refer to clinician'\n    return best_name\n\nprint(heal_burn(patient))",
        "must_contain": ["def heal_burn", "return"],
        "prelude": make_materials_prelude(),
        "base_inject": {"patient": {"max_cost": 6}},
        "function_tests": [
            {
                "function": "heal_burn",
                "arguments": [{"max_cost": 3}],
                "expected": "Hydrogel",
            },
            {
                "function": "heal_burn",
                "arguments": [{"max_cost": 5}],
                "expected": "Chitosan",
            },
            {
                "function": "heal_burn",
                "arguments": [{"max_cost": 1}],
                "expected": "Refer to clinician",
            },
        ],
        "bonus": {
            "title": "Bonus: compare two patient limits",
            "task": "Write compare_limits(first_patient, second_patient) to return both recommended dressing names in a list.",
            "starter": "",
            "prelude": make_materials_prelude() + "def heal_burn(patient):\n    best_name = None\n    best_score = None\n    for dressing_name in dressings:\n        dressing_data = dressings[dressing_name]\n        if dressing_data['cost'] <= patient['max_cost']:\n            current_score = score(dressing_data)\n            if best_score is None or current_score > best_score:\n                best_name = dressing_name\n                best_score = current_score\n    if best_name is None:\n        return 'Refer to clinician'\n    return best_name\n",
            "solution": "def compare_limits(first_patient, second_patient):\n    first_choice = heal_burn(first_patient)\n    second_choice = heal_burn(second_patient)\n    choices = [first_choice, second_choice]\n    return choices",
            "function_tests": [
                {
                    "function": "compare_limits",
                    "arguments": [{"max_cost": 3}, {"max_cost": 1}],
                    "expected": ["Hydrogel", "Refer to clinician"],
                }
            ],
        },
        "feedback_key": "boss",
    },
]