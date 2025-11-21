import streamlit as st
import openai

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="Legal Dictionary", layout="centered")
st.title("⚖️ Legal Dictionary (AI-Powered)")
st.write("Enter any legal term or phrase to get an updated, accurate definition.")

# ------------------------------------------------------
# LOAD PERSONAL API KEY (NO USER INPUT)
# ------------------------------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("API key missing. Add OPENAI_API_KEY to .streamlit/secrets.toml")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]
model_name = "gpt-4.1-mini"   # You can change this later

# ------------------------------------------------------
# LEGAL DICTIONARY SYSTEM INSTRUCTIONS
# ------------------------------------------------------
legal_prompt = """
You are an AI Legal Dictionary.

Your job:
- Provide clear, accurate, concise definitions for legal terms and phrases.
- Always explain the term as used in law, including its purpose, meaning, and relevance.
- If the term has different meanings in different jurisdictions, summarize briefly.
- Use plain English, but stay precise.
- NEVER give legal advice, predictions, or instructions. Only definitions.
- If a user asks for something unrelated to legal terminology, respond:
  "I can only provide definitions of legal terms and concepts."
"""

# ------------------------------------------------------
# SESSION MEMORY
# ------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------------------------------
# USER INPUT
# ------------------------------------------------------
query = st.text_input("Legal term:")

if query:
    st.session_state.history.append(("User", query))

    try:
        response = openai.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": legal_prompt},
                {"role": "user", "content": query}
            ]
        )

        # Correct extraction
        definition = response.choices[0].message.content

    except Exception as e:
        definition = f"Error: {str(e)}"

    st.session_state.history.append(("AI", definition))

# ------------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------------
for sender, message in st.session_state.history:
    if sender == "User":
        st.markdown(f"**🧑‍💬 User:** {message}")
    else:
        st.markdown(f"**🤖 Legal Dictionary:** {message}")
