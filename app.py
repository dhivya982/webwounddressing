import pandas as pd
import streamlit as st

from bio_content import BURN_DEGREES, WHY_DRESSINGS_MATTER, WOUND_HEALING_STAGES
from info_content import BURN_DEGREES as INFO_BURN_DEGREES
from info_content import DISCLAIMER, SOURCES as INFO_SOURCES
from info_content import WOUND_HEALING_STAGES as INFO_WOUND_HEALING_STAGES
from info_content import WHY_DRESSINGS_MATTER as INFO_WHY_DRESSINGS_MATTER
from levels import LEVELS
from materials_b import DRESSINGS, SOURCES, WEIGHTS
from materials_c import DESCRIPTIONS
from runner import check_level
from styles import apply_styles


st.set_page_config(page_title="Learn Python with Wound Dressings", layout="wide")
apply_styles()


TEAM_MEMBERS = [
    {"name": "Dhivyadharshini M", "field": "Materials Science"},
    {"name": "Anitha ", "field": "Biotechnology"},
    {"name": "Lakshanna V", "field": "Materials Science"},
]


def get_level_key(level_number):
    return "level_" + str(level_number)


def go_to_next_level(next_level, level_key, level_number):
    st.session_state["current_level"] = next_level
    st.session_state["attempts_" + str(next_level)] = 0
    st.session_state[level_key] = ""
    st.session_state.pop("result_" + str(level_number), None)
    st.session_state["page_to_restore"] = "Level " + str(next_level)


def make_page_options():
    page_options = ["Home", "🔬 Wound Healing Science", "🧬 Dressing Materials"]
    for level in LEVELS:
        if level["number"] in st.session_state["unlocked_levels"]:
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
    st.markdown(
        """
        <div class="hero-banner">
            <h1>Learn Python with Wound Dressings</h1>
            <p>Explore Python through wound-healing science and sample dressing data.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "A beginner course that uses sample wound-dressing properties to teach core Python concepts. "
        "The material is educational and is not medical advice."
    )
    total_stars = 0
    levels_completed = 0
    for level in LEVELS:
        level_number = level["number"]
        total_stars += st.session_state.get("stars_" + str(level_number), 0)
        if st.session_state.get("done_" + str(level_number), False):
            levels_completed += 1

    st.markdown('<div class="section-heading">Your progress</div>', unsafe_allow_html=True)
    stats_columns = st.columns(3)
    stat_items = [
        ("Levels completed", str(levels_completed) + " / " + str(len(LEVELS))),
        ("Total points", str(st.session_state["total_score"])),
        ("Total stars", str(total_stars) + " / 24"),
    ]
    for column, stat_item in zip(stats_columns, stat_items):
        label, value = stat_item
        column.markdown(
            '<div class="stat-card"><span>' + label + '</span><strong>' + value + "</strong></div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">Meet the team</div>', unsafe_allow_html=True)
    team_columns = st.columns(3)
    for column, member in zip(team_columns, TEAM_MEMBERS):
        column.markdown(
            '<div class="team-card"><strong>' + member["name"] + "</strong><span>"
            + member["field"] + "</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">How it works</div>', unsafe_allow_html=True)
    how_columns = st.columns(3)
    how_steps = [
        ("1. Learn", "Discover a Python concept and the science behind it."),
        ("2. Code", "Edit the starter code and check your solution."),
        ("3. Heal the burn", "Use what you learned to solve the next challenge."),
    ]
    for column, step in zip(how_columns, how_steps):
        title, description = step
        column.markdown(
            '<div class="how-card"><strong>' + title + "</strong><span>"
            + description + "</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">Ready to begin?</div>', unsafe_allow_html=True)
    st.write(
        "Choose a page from the sidebar. Read the science and materials pages, then work through the "
        "eight independent levels. Edit the starter code, run the checks, and use hints or solutions when needed."
    )
    if st.button("Start Level 1", key="start_level_1"):
        st.session_state["page_to_restore"] = "Level 1"
        st.rerun()


def show_science_background():
    st.title("🔬 Wound Healing Science")
    st.write(WHY_DRESSINGS_MATTER)

    def show_entries(entries):
        for entry in entries:
            if isinstance(entry, dict):
                entry_name = entry.get("name")
                entry_description = entry.get("description")
            elif isinstance(entry, (tuple, list)) and len(entry) >= 2:
                entry_name, entry_description = entry[0], entry[1]
            else:
                continue
            if entry_name is not None:
                st.markdown("**" + str(entry_name) + "**")
                st.write(entry_description)

    st.subheader("Wound healing stages")
    show_entries(WOUND_HEALING_STAGES)
    st.subheader("Burn degrees")
    show_entries(BURN_DEGREES)


def show_materials():
    st.title("🧬 Dressing Materials")
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


def show_level_info():
    info_panel = st.popover("⭐ Info") if hasattr(st, "popover") else st.expander("⭐ Info")
    with info_panel:
        science_tab, materials_tab, sources_tab = st.tabs(
            ["🔬 Wound Healing Science", "🧬 Dressing Materials", "📚 Sources"]
        )
        with science_tab:
            st.subheader("Why Dressings Matter")
            st.markdown(INFO_WHY_DRESSINGS_MATTER)
            st.subheader("The 4 Stages of Wound Healing")
            st.markdown(
                "Healing happens in four overlapping phases, so one stage doesn't stop neatly "
                "before the next begins."
            )
            for stage_name, stage_description in INFO_WOUND_HEALING_STAGES:
                with st.expander(stage_name):
                    st.markdown(stage_description)
            st.subheader("Burn degrees")
            for burn_name, burn_description in INFO_BURN_DEGREES:
                with st.expander(burn_name):
                    st.markdown(burn_description)
        with materials_tab:
            for material_name in DESCRIPTIONS:
                st.subheader(material_name)
                st.write(DESCRIPTIONS[material_name])
        with sources_tab:
            for source_name, source_url in INFO_SOURCES:
                st.markdown("[" + source_name + "](" + source_url + ")")
            st.caption(DISCLAIMER)


def show_level(level):
    level_number = level["number"]
    st.session_state["current_level"] = level_number
    level_key = get_level_key(level_number)
    attempts_key = "attempts_" + str(level_number)
    if attempts_key not in st.session_state:
        st.session_state[attempts_key] = 0
    if level_key not in st.session_state:
        st.session_state[level_key] = level["starter"]

    levels_completed = 0
    for course_level in LEVELS:
        if st.session_state.get("done_" + str(course_level["number"]), False):
            levels_completed += 1
    st.progress(
        levels_completed / len(LEVELS),
        text="Course progress: " + str(levels_completed) + " of " + str(len(LEVELS)) + " levels completed",
    )
    st.title("Level " + str(level_number) + ": " + level["title"])
    show_level_info()
    attempts = st.session_state[attempts_key]
    if st.session_state.get("done_" + str(level_number), False):
        attempt_number = min(max(attempts, 1), 3)
    else:
        attempt_number = min(attempts + 1, 3)
    st.caption("Attempt " + str(attempt_number) + " of 3")
    st.markdown("**Concept:** " + level["concept"])
    with st.container(border=True):
        st.subheader("Story")
        st.write(level["story"])
    with st.container(border=True):
        st.subheader("Lesson")
        st.write(level["lesson"])
    with st.container(border=True):
        st.subheader("Task")
        st.write(level["task"])

    code = st.text_area("Your code", key=level_key, height=230)
    button_columns = st.columns(2)
    run_clicked = button_columns[0].button(
        "Run and check",
        key="run_" + str(level_number),
        disabled=st.session_state.get("done_" + str(level_number), False),
    )
    reset_clicked = button_columns[1].button("Reset code", key="reset_" + str(level_number))

    if reset_clicked:
        st.session_state[level_key] = level["starter"]
        st.session_state.pop("result_" + str(level_number), None)
        st.rerun()

    if run_clicked:
        st.session_state[attempts_key] += 1
        attempt_number = st.session_state[attempts_key]
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
            points_by_attempt = {1: 10, 2: 7, 3: 4}
            points = (
                0
                if st.session_state.get("solution_viewed_" + str(level_number), False)
                else points_by_attempt[attempt_number]
            )
            st.session_state["total_score"] += points
            st.session_state["pending_points_popup"] = points
            if st.session_state.get("solution_viewed_" + str(level_number), False):
                st.session_state["stars_" + str(level_number)] = 1
            elif st.session_state.get("hint_viewed_" + str(level_number), False):
                st.session_state["stars_" + str(level_number)] = 2
            else:
                st.session_state["stars_" + str(level_number)] = 3
        elif not passed and attempt_number == 3:
            st.session_state["solution_revealed_" + str(level_number)] = True
            st.session_state["done_" + str(level_number)] = True
            st.session_state["stars_" + str(level_number)] = 0
            st.session_state["solution_viewed_" + str(level_number)] = True
        if st.session_state.get("done_" + str(level_number), False):
            next_level = level_number + 1
            if next_level <= len(LEVELS) and next_level not in st.session_state["unlocked_levels"]:
                st.session_state["unlocked_levels"].append(next_level)
            st.session_state["page_to_restore"] = "Level " + str(level_number)
        st.rerun()

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
            st.info("Hint: " + level["hint"])

    hint_panel = st.expander(
        "Hint",
        key="hint_panel_" + str(level_number),
        on_change="rerun",
    )
    with hint_panel:
        st.write(level["hint"])
    if hint_panel.open:
        st.session_state["hint_viewed_" + str(level_number)] = True

    if st.session_state.get("solution_revealed_" + str(level_number), False):
        st.subheader("Model solution")
        st.code(level["solution"], language="python")
    elif st.session_state.get("done_" + str(level_number), False):
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

    if st.session_state.get("done_" + str(level_number), False):
        if level_number == len(LEVELS):
            st.success("You finished all levels! Final score: " + str(st.session_state["total_score"]))
        else:
            st.button(
                "Next Level ➡️",
                key="next_level_button_" + str(level_number),
                on_click=go_to_next_level,
                args=(level_number + 1, level_key, level_number),
            )


if "unlocked_levels" not in st.session_state:
    st.session_state["unlocked_levels"] = [1]
    for level in LEVELS:
        level_number = level["number"]
        if (
            level_number in st.session_state["unlocked_levels"]
            and st.session_state.get("done_" + str(level_number), False)
        ):
            next_level = level_number + 1
            if next_level <= len(LEVELS):
                st.session_state["unlocked_levels"].append(next_level)
if "total_score" not in st.session_state:
    st.session_state["total_score"] = 0

if "pending_points_popup" in st.session_state:
    earned_points = st.session_state.pop("pending_points_popup")
    st.toast("+" + str(earned_points) + " points!", icon="🎉")
    st.markdown(
        '<div class="points-popup"><strong>+' + str(earned_points)
        + ' points!</strong> Great work — keep going!</div>',
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    '<div class="sidebar-brand">Course pages</div>',
    unsafe_allow_html=True,
)
st.sidebar.metric("Total points", st.session_state["total_score"])
if "page_to_restore" in st.session_state:
    st.session_state["course_page"] = st.session_state.pop("page_to_restore")
selected_page = st.sidebar.radio(
    "Pages",
    make_page_options(),
    format_func=format_page_option,
    key="course_page",
)

if selected_page == "Home":
    show_home()
elif selected_page == "🔬 Wound Healing Science":
    show_science_background()
elif selected_page == "🧬 Dressing Materials":
    show_materials()
else:
    selected_level = None
    for level in LEVELS:
        level_label = "Level " + str(level["number"])
        if selected_page == level_label:
            selected_level = level
    if selected_level is not None:
        show_level(selected_level)