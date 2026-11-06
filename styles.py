import streamlit as st


APP_STYLES = """
<style>
    :root {
        --teal: #0F766E;
        --green: #22C55E;
        --aqua: #14B8A6;
        --sky: #0EA5E9;
        --deep-blue: #0C4A6E;
        --mint: #F0FDFA;
    }

    .stApp {
        background: var(--mint);
        color: var(--deep-blue);
    }

    [data-testid="stHeader"] {
        background: rgba(240, 253, 250, 0.92);
    }

    [data-testid="stMain"] .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, p, label {
        color: var(--deep-blue);
    }

    .hero-banner {
        padding: 2.5rem 2.75rem;
        margin: 0 0 1.5rem;
        border-radius: 20px;
        color: #FFFFFF;
        background: linear-gradient(125deg, var(--teal), var(--aqua) 52%, var(--sky));
        box-shadow: 0 12px 28px rgba(12, 74, 110, 0.17);
    }

    .hero-banner h1,
    .hero-banner p {
        color: #FFFFFF;
        margin: 0;
    }

    .hero-banner h1 {
        font-size: clamp(2rem, 5vw, 3.2rem);
        line-height: 1.12;
        margin-bottom: 0.8rem;
    }

    .hero-banner p {
        font-size: 1.05rem;
        max-width: 760px;
    }

    .section-heading {
        margin: 1.8rem 0 0.7rem;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--deep-blue);
    }

    .team-card,
    .stat-card,
    .how-card {
        height: 100%;
        padding: 1.15rem 1.25rem;
        border: 1px solid rgba(15, 118, 110, 0.12);
        border-radius: 14px;
        background: #FFFFFF;
        box-shadow: 0 5px 16px rgba(12, 74, 110, 0.08);
    }

    .team-card {
        min-height: 112px;
        border-top: 4px solid var(--aqua);
    }

    .team-card strong,
    .stat-card strong,
    .how-card strong {
        display: block;
        color: var(--deep-blue);
    }

    .team-card strong {
        margin-bottom: 0.35rem;
        font-size: 1.03rem;
    }

    .team-card span,
    .stat-card span,
    .how-card span {
        color: #315B6C;
        font-size: 0.93rem;
    }

    .stat-card {
        min-height: 96px;
        border-left: 4px solid var(--green);
    }

    .stat-card strong {
        margin-top: 0.35rem;
        font-size: 1.65rem;
    }

    .how-card {
        min-height: 120px;
        border-top: 4px solid var(--sky);
    }

    .how-card strong {
        margin-bottom: 0.45rem;
        font-size: 1.05rem;
    }

    .sidebar-brand {
        padding: 1rem 1.1rem;
        margin: 0 0 1.1rem;
        border-radius: 14px;
        color: #FFFFFF;
        background: linear-gradient(125deg, var(--teal), var(--green), var(--sky));
        font-size: 1.2rem;
        font-weight: 750;
        box-shadow: 0 6px 16px rgba(12, 74, 110, 0.15);
    }

    [data-testid="stSidebar"] {
        background: #E6FFFA;
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] {
        padding: 0.85rem;
        border: 1px solid rgba(15, 118, 110, 0.12);
        border-radius: 12px;
        background: #FFFFFF;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 0.45rem 0.6rem;
        border-radius: 9px;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: #CCFBF1;
        box-shadow: inset 3px 0 0 var(--teal);
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
        color: var(--deep-blue);
        font-weight: 700;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(15, 118, 110, 0.13) !important;
        border-radius: 14px !important;
        background: #FFFFFF;
        box-shadow: 0 5px 16px rgba(12, 74, 110, 0.07);
    }

    textarea {
        border-radius: 10px !important;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace !important;
        font-size: 0.94rem !important;
        line-height: 1.55 !important;
    }

    [data-testid="stCodeBlock"] {
        border: 1px solid rgba(15, 118, 110, 0.16);
        border-radius: 12px;
        background: #F8FFFE;
    }

    div.stButton > button {
        min-height: 2.7rem;
        border: 0;
        border-radius: 10px;
        color: #FFFFFF;
        background: linear-gradient(110deg, var(--teal), var(--green), var(--sky));
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.18);
        transition: transform 150ms ease, box-shadow 150ms ease;
    }

    div.stButton > button:hover {
        color: #FFFFFF;
        border: 0;
        transform: translateY(-1px);
        box-shadow: 0 7px 16px rgba(15, 118, 110, 0.24);
    }

    div.stButton > button:focus {
        color: #FFFFFF;
        border-color: var(--deep-blue);
    }

    [data-testid="stAlert"][kind="error"] {
        border-color: #FCA5A5;
        background: #FEF2F2;
        color: #7F1D1D;
    }

    [data-testid="stAlert"][kind="success"] {
        border-color: #86EFAC;
        background: #F0FDF4;
        color: #14532D;
    }

    .points-popup {
        padding: 1rem 1.25rem;
        margin: 0.5rem 0 1rem;
        border: 1px solid #86EFAC;
        border-left: 5px solid var(--green);
        border-radius: 14px;
        color: #14532D;
        background: linear-gradient(110deg, #F0FDF4, #ECFEFF);
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.12);
        animation: points-appear 550ms ease-out both;
    }

    .points-popup strong {
        color: #14532D;
        font-size: 1.15rem;
    }

    @keyframes points-appear {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (max-width: 640px) {
        [data-testid="stMain"] .block-container {
            padding: 1rem 0.8rem 2rem;
        }

        .hero-banner {
            padding: 1.5rem 1.25rem;
            border-radius: 16px;
        }

        .hero-banner h1 {
            font-size: 2rem;
        }

        .team-card,
        .how-card,
        .stat-card {
            min-height: auto;
            padding: 1rem;
        }
    }
</style>
"""


def apply_styles():
    st.markdown(APP_STYLES, unsafe_allow_html=True)
