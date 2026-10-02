import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors


# --------------------------------------------------
# SETUP
# --------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="The Manipulator",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("🔑 Google API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #0f1117 0%, #161a23 100%);
        }

        h1 {
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .subtitle {
            color: #9aa4b2;
            font-size: 1.05rem;
            margin-top: -0.6rem;
            margin-bottom: 1.8rem;
        }

        .section-label {
            font-weight: 700;
            font-size: 1rem;
            color: #e6e9ef;
            margin-bottom: 0.3rem;
            margin-top: 1.2rem;
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 10px;
            border: 1px solid #2a2f3a;
        }

        div[data-testid="stButton"] button {
            width: 100%;
            border-radius: 10px;
            font-weight: 700;
            padding: 0.7rem 0;
            background: linear-gradient(90deg, #6d5efc, #8b5cf6);
            border: none;
            color: white;
            transition: transform 0.15s ease;
        }

        div[data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            filter: brightness(1.08);
        }

        .result-card {
            background: #1a1d27;
            border: 1px solid #2a2f3a;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧠 The Manipulator")

st.markdown(
    '<p class="subtitle">'
    "Analyze two conflicting accounts and compare AI judgment with a human decision."
    "</p>",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-label">⚖️ Conflicting Accounts</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    account1 = st.text_area(
        "Account 1",
        placeholder="Enter the first person's account here...",
        height=160,
    )

with col2:
    account2 = st.text_area(
        "Account 2",
        placeholder="Enter the second person's account here...",
        height=160,
    )


st.markdown(
    '<div class="section-label">🙋 Human Decision</div>',
    unsafe_allow_html=True,
)

human_decision = st.text_area(
    "What is the human decision?",
    placeholder="Enter the decision made by the human...",
    height=120,
    label_visibility="collapsed",
)

st.write("")


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

analyze_clicked = st.button(
    "Analyze Dispute",
    use_container_width=True,
)


if analyze_clicked:

    if not account1 or not account2 or not human_decision:
        st.warning("⚠️ Please fill in all three fields before analyzing.")
        st.stop()

    prompt = f"""
You are an impartial dispute analysis system called "The Manipulator".

Analyze the two conflicting accounts below.

ACCOUNT 1:
{account1}

ACCOUNT 2:
{account2}

HUMAN DECISION:
{human_decision}

Provide the analysis in the following structure:

1. KEY FACTS FROM ACCOUNT 1
List only the important factual claims.

2. KEY FACTS FROM ACCOUNT 2
List only the important factual claims.

3. AGREEMENTS
Identify facts or details both accounts agree on.

4. CONTRADICTIONS
Identify specific differences between the accounts.

5. IMPORTANT EVIDENCE
Identify which details are most relevant to deciding the dispute.
Do not invent evidence.

6. AI ANALYSIS
Give a neutral assessment based only on the information provided.
Explain which claims are supported, unsupported, or uncertain.

7. AI VS HUMAN DECISION
Compare the AI analysis with the human decision.
Explain where they agree and where they differ.

Do not invent facts or assume information that was not provided.
"""

    model_name = os.getenv("GEMINI_MODEL")

    if not model_name:
        st.error("⚙️ GEMINI_MODEL is not configured in your .env file.")
        st.stop()

    max_retries = 3
    base_delay = 2

    response = None
    last_error = None

    with st.spinner("Analyzing accounts..."):

        for attempt in range(1, max_retries + 1):

            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )

                last_error = None
                break

            except genai_errors.ServerError as e:

                last_error = e

                if attempt < max_retries:
                    st.toast(
                        f"Model is busy "
                        f"(attempt {attempt}/{max_retries}). Retrying...",
                        icon="⏳",
                    )

                    time.sleep(base_delay * attempt)

            except Exception as e:

                last_error = e
                break

    if response is not None:

        st.success("✅ Analysis complete")

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### 📋 AI Analysis")
        st.write(response.text)

        st.markdown("</div>", unsafe_allow_html=True)

    elif last_error is not None:

        st.error(
            f"The model is currently unavailable after "
            f"{max_retries} attempts.\n\n"
            f"Please try again in a moment.\n\n"
            f"Details: {last_error}"
        )


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.caption(
    "Disclaimer: This tool provides AI-generated analysis based only on "
    "the information supplied by the user. It does not determine factual "
    "truth, legal responsibility, or guilt."
)
