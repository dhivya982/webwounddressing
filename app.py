import pandas as pd
import streamlit as st

from bio_content import BURN_DEGREES, WHY_DRESSINGS_MATTER, WOUND_HEALING_STAGES
from levels import LEVELS
from materials_b import DRESSINGS, SOURCES, WEIGHTS
from materials_c import DESCRIPTIONS
from runner import check_level


st.set_page_config(page_title="Learn Python with Wound Dressings", layout="wide")


def get_level_key(level_number):
    return "level_" + str(level_number)


def make_page_options():
    page_options = ["Home", "Science background", "Materials"]
    for level in LEVELS:
        page_options.append("Level " + str(level["number"]))
    return page_options


def format_page_option(page):
    for level in LEVELS:
        level_label = "Level " + str(level["number"])
        if page == level_label:
            option_label = level_label + ": " + level["title"]
            if st.session_state.get("done_" + str(level["number"]), False):
                option_label += " (done)"
            star_count = st.session_state.get("stars_" + str(level["number"]), 0)
            if star_count > 0:
                option_label += " " + ("★" * star_count)
            return option_label
    return page


def show_home():
    st.title("Learn Python with Wound Dressings")
    st.write(
        "A beginner course that uses sample wound-dressing properties to teach core Python concepts. "
        "The material is educational and is not medical advice."
    )
    total_stars = 0
    for level in LEVELS:
        total_stars += st.session_state.get("stars_" + str(level["number"]), 0)
    st.subheader("Total stars: " + str(total_stars) + " / 24")
    st.subheader("How to use the course")
    st.write(
        "Choose a page from the sidebar. Read the science and materials pages, then work through the "
        "eight independent levels. Edit the starter code, run the checks, and use hints or solutions when needed."
    )
    st.subheader("Team")
    team_rows = [
        {"Role": "Biotechnology content", "Name": "(add name)"},
        {"Role": "Materials data and scoring", "Name": "(add name)"},
        {"Role": "Materials descriptions", "Name": "(add name)"},
    ]
    st.table(pd.DataFrame(team_rows))


def show_science_background():
    st.title("Science background")
    st.write(WHY_DRESSINGS_MATTER)
    st.subheader("Wound healing stages")
    for stage in WOUND_HEALING_STAGES:
        st.markdown("**" + stage["name"] + "**")
        st.write(stage["description"])
    st.subheader("Burn degrees")
    for burn in BURN_DEGREES:
        st.markdown("**" + burn["name"] + "**")
        st.write(burn["description"])


def show_materials():
    st.title("Materials")
    st.write("These placeholder scores are for learning Python only and are not clinical recommendations.")
    st.subheader("Material descriptions")
    for material_name in DESCRIPTIONS:
        st.markdown("**" + material_name + "**")
        st.write(DESCRIPTIONS[material_name])

    st.subheader("Sample properties")
    property_rows = []
    for dressing_name in DRESSINGS:
        property_row = {"Dressing": dressing_name}
        property_row.update(DRESSINGS[dressing_name])
        property_rows.append(property_row)
    property_table = pd.DataFrame(property_rows)
    property_table = property_table.set_index("Dressing")
    st.dataframe(property_table)

    st.subheader("Scoring formula")
    st.write(
        "score = absorbency x absorbency weight + antibacterial x antibacterial weight "
        "- cost x cost weight"
    )
    st.write("Weights: " + str(WEIGHTS))
    st.subheader("Sources")
    for source in SOURCES:
        st.write(source)


def show_level(level):
    level_number = level["number"]
    level_key = get_level_key(level_number)
    if level_key not in st.session_state:
        st.session_state[level_key] = level["starter"]

    st.title("Level " + str(level_number) + ": " + level["title"])
    st.markdown("**Concept:** " + level["concept"])
    st.subheader("Story")
    st.write(level["story"])
    st.subheader("Lesson")
    st.write(level["lesson"])
    st.subheader("Task")
    st.write(level["task"])

    code = st.text_area("Your code", key=level_key, height=230)
    button_columns = st.columns(2)
    run_clicked = button_columns[0].button("Run and check", key="run_" + str(level_number))
    reset_clicked = button_columns[1].button("Reset code", key="reset_" + str(level_number))

    if reset_clicked:
        st.session_state[level_key] = level["starter"]
        st.session_state.pop("result_" + str(level_number), None)
        st.rerun()

    if run_clicked:
        passed, message, output = check_level(level, code)
        run_result = {
            "passed": passed,
            "message": message,
            "output": output,
        }
        st.session_state["result_" + str(level_number)] = run_result
        already_done = st.session_state.get("done_" + str(level_number), False)
        if passed and not already_done:
            st.session_state["done_" + str(level_number)] = True
            if st.session_state.get("solution_viewed_" + str(level_number), False):
                st.session_state["stars_" + str(level_number)] = 1
            elif st.session_state.get("hint_viewed_" + str(level_number), False):
                st.session_state["stars_" + str(level_number)] = 2
            else:
                st.session_state["stars_" + str(level_number)] = 3

    last_result = st.session_state.get("result_" + str(level_number))
    if last_result is not None:
        st.subheader("Program output")
        if last_result["output"]:
            st.code(last_result["output"], language="text")
        else:
            st.write("(No output)")
        if last_result["passed"]:
            st.success(last_result["message"])
        else:
            st.error(last_result["message"])

    hint_panel = st.expander(
        "Hint",
        key="hint_panel_" + str(level_number),
        on_change="rerun",
    )
    with hint_panel:
        st.write(level["hint"])
    if hint_panel.open:
        st.session_state["hint_viewed_" + str(level_number)] = True

    solution_panel = st.expander(
        "Solution",
        key="solution_panel_" + str(level_number),
        on_change="rerun",
    )
    with solution_panel:
        st.code(level["solution"], language="python")
    if solution_panel.open:
        st.session_state["solution_viewed_" + str(level_number)] = True

    if level_number == 5 and st.session_state.get("done_5", False):
        st.subheader("Sample dressing scores")
        chart_names = []
        chart_scores = []
        for dressing_name in DRESSINGS:
            dressing_data = DRESSINGS[dressing_name]
            dressing_score = (
                dressing_data["absorbency"] * WEIGHTS["absorbency"]
                + dressing_data["antibacterial"] * WEIGHTS["antibacterial"]
                - dressing_data["cost"] * WEIGHTS["cost"]
            )
            chart_names.append(dressing_name)
            chart_scores.append(dressing_score)
        chart_data = pd.DataFrame({"Score": chart_scores}, index=chart_names)
        st.bar_chart(chart_data)

    if level_number == 8 and st.session_state.get("done_8", False):
        st.subheader("Illustrative healing over 14 days")
        st.write("Educational simulation only; this is not a healing prediction or medical guidance.")
        day_numbers = []
        healing_index = []
        current_index = 100
        for day_number in range(1, 15):
            day_numbers.append(day_number)
            healing_index.append(current_index)
            current_index = current_index - 3
        healing_data = pd.DataFrame({"Illustrative wound index": healing_index}, index=day_numbers)
        st.line_chart(healing_data)

    bonus = level.get("bonus")
    if bonus is not None:
        st.subheader(bonus["title"])
        st.write(bonus["task"])
        bonus_key = "bonus_code_" + str(level_number)
        if bonus_key not in st.session_state:
            st.session_state[bonus_key] = bonus["starter"]
        bonus_code = st.text_area("Bonus code", key=bonus_key, height=180)
        bonus_result_key = "bonus_result_" + str(level_number)
        if st.button("Check bonus", key="bonus_run_" + str(level_number)):
            bonus_passed, bonus_message, bonus_output = check_level(bonus, bonus_code)
            st.session_state[bonus_result_key] = {
                "passed": bonus_passed,
                "message": bonus_message,
                "output": bonus_output,
            }
        bonus_result = st.session_state.get(bonus_result_key)
        if bonus_result is not None:
            if bonus_result["output"]:
                st.code(bonus_result["output"], language="text")
            if bonus_result["passed"]:
                st.success(bonus_result["message"])
            else:
                st.error(bonus_result["message"])
        with st.expander("Bonus solution"):
            st.code(bonus["solution"], language="python")


st.sidebar.title("Course pages")
selected_page = st.sidebar.radio("Pages", make_page_options(), format_func=format_page_option)

if selected_page == "Home":
    show_home()
elif selected_page == "Science background":
    show_science_background()
elif selected_page == "Materials":
    show_materials()
else:
    selected_level = None
    for level in LEVELS:
        level_label = "Level " + str(level["number"])
        if selected_page == level_label:
            selected_level = level
    if selected_level is not None:
        show_level(selected_level)