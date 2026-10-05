import streamlit as st

from ollama_chat import get_chat_response
from tax_calculator import calculate_taxable_income


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TaxMate",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 25px;
    }

    /* Warning box */
    .warning {
        padding: 15px;
        border-radius: 10px;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        margin-bottom: 20px;
    }

    /* Calculator result */
    .calculator-result {
        padding: 15px;
        border-radius: 10px;
        background-color: #e8f5e9;
        border: 1px solid #c8e6c9;
        margin-top: 10px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">💰 TaxMate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Tax Filing Assistant</div>',
    unsafe_allow_html=True
)


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown(
    """
    <div class="warning">
        ⚠️ <b>Disclaimer:</b>
        TaxMate provides general educational information only.
        Tax rules, rates and deadlines may change.
        Please verify important information with the latest
        official government sources or a qualified tax professional.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📋 TaxMate Menu")

    # --------------------------------------------------------
    # QUICK QUESTIONS
    # --------------------------------------------------------

    st.subheader("💬 Quick Questions")

    quick_questions = [
        "What is taxable income?",
        "What documents are needed for tax filing?",
        "What are tax deductions?",
        "What is a tax refund?",
        "Explain the tax filing process.",
        "What is Form 16?",
        "What is TDS?",
        "What is the difference between old and new tax regime?"
    ]

    for question in quick_questions:

        if st.button(
            question,
            use_container_width=True
        ):

            st.session_state.selected_question = question

            # Rerun so the question is processed immediately
            st.rerun()


    st.divider()


    # ========================================================
    # TAX CALCULATOR
    # ========================================================

    st.header("🧮 Taxable Income Calculator")

    gross_income = st.number_input(
        "Gross Annual Income (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        format="%.2f"
    )

    deductions = st.number_input(
        "Eligible Deductions (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        format="%.2f"
    )


    if st.button(
        "Calculate Taxable Income",
        use_container_width=True
    ):

        taxable_income = calculate_taxable_income(
            gross_income,
            deductions
        )

        st.success(
            f"Estimated Taxable Income: ₹{taxable_income:,.2f}"
        )


    st.divider()


    # ========================================================
    # CLEAR CHAT
    # ========================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        if "selected_question" in st.session_state:
            del st.session_state.selected_question

        st.rerun()


# ============================================================
# PROCESS QUICK QUESTION
# ============================================================

if "selected_question" in st.session_state:

    question = st.session_state.selected_question

    # Remove selected question so it isn't processed again
    del st.session_state.selected_question


    # Add user question to chat
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Generate Ollama response
    try:

        answer = get_chat_response(
            question,
            st.session_state.messages[:-1]
        )

    except Exception as error:

        answer = (
            "⚠️ **Unable to connect to Ollama.**\n\n"
            "Please make sure:\n"
            "1. Ollama is installed.\n"
            "2. Ollama is running.\n"
            "3. The `llama3.2` model is installed.\n\n"
            "You can check by running `ollama list` "
            "in PowerShell."
        )


    # Add AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# DISPLAY PREVIOUS CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask TaxMate anything about tax filing..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_input:

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)


    # --------------------------------------------------------
    # Generate AI response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("TaxMate is thinking..."):

            try:

                # Send current question + previous conversation
                answer = get_chat_response(
                    user_input,
                    st.session_state.messages[:-1]
                )

            except Exception as error:

                answer = (
                    "⚠️ **Sorry, I could not generate a response.**\n\n"
                    "Please make sure Ollama is running and "
                    "the `llama3.2` model is installed.\n\n"
                    "Run these commands in PowerShell:\n\n"
                    "```text\n"
                    "ollama list\n"
                    "ollama run llama3.2\n"
                    "```"
                )


        # Display AI response
        st.markdown(answer)


    # --------------------------------------------------------
    # Save AI response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
