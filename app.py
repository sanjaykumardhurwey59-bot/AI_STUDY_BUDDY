import os
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

if "notes_input" not in st.session_state:
    st.session_state.notes_input = ""

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)
st.markdown("""
<style>

.main {
    padding: 2rem;
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

.stTextArea textarea {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI API ----------------

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)
# ---------- HISTORY ----------

if "history" not in st.session_state:

    st.session_state.history = []
# ---------------- LOAD MODEL ----------------

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-2.5-flash")

model = load_model()

# ---------------- SIDEBAR ----------------

st.sidebar.title("📚 AI Study Buddy")

st.sidebar.write("AI-Powered Personalized Learning Assistant")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Select Feature",
    [
        "🏠 Home",
        "🧠 Explain Topic",
        "📝 Summarize Notes",
        "❓ Quiz Generator",
        "🗂️ Flashcards",
        "📄 PDF Upload",
        "💬 History"
    ]
)

st.sidebar.markdown("---")
# ---------------- HOME ----------------

if menu == "🏠 Home":

    st.title("📚 AI Study Buddy")

    st.subheader("AI-Powered Personalized Learning Assistant")

    st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background:linear-gradient(90deg,#4F46E5,#06B6D4);
color:white;
text-align:center;
">

<h2>📚 AI Study Buddy</h2>

<p>AI-Powered Personalized Learning Assistant</p>

</div>
""", unsafe_allow_html=True)
    

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Features", "5")

    with col2:
        st.metric("AI Status", "Active")

    with col3:
        st.metric("Platform", "Online")

    st.divider()

    st.info("💡 Tip: Use the left sidebar to access all tools.")
# ---------------- EXPLAIN TOPIC ----------------

elif menu == "🧠 Explain Topic":

    st.title("🧠 Explain Topic")

    topic = st.text_input(
    "Enter a topic",
    key="topic_input"
)
    if st.button("Explain"):

        if topic.strip() == "":

            st.warning("Please enter a topic.")

        else:

            prompt = f"""
You are an expert teacher.

Explain this topic.

Topic: {topic}

Give:

1. Definition

2. Explanation

3. Key points

4. Real-life example

Use simple language.
"""

            try:

                with st.spinner("Generating answer..."):

                    response = model.generate_content(prompt)

                st.markdown(response.text)
                st.session_state.history.append({

    "feature": "🧠 Explain Topic",

    "title": topic,

    "answer": response.text

})

                st.download_button(
                    
    label="📥 Download Explanation",
    data=response.text,
    file_name="explanation.txt",
    mime="text/plain"
     
)
                
                

            except Exception as e:

                st.error(e)

# ---------------- SUMMARIZE NOTES ----------------

elif menu == "📝 Summarize Notes":

    st.title("📝 Summarize Notes")

    notes = st.text_area(
    "Paste your notes",
    height=250,
    key="notes_input"
)
    if st.button("Summarize"):

        if notes.strip() == "":

            st.warning("Please enter notes.")

        else:

            prompt = f"""
Summarize these notes.

Rules:

- Short explanation

- Bullet points

Notes:

{notes}
"""

            try:

                with st.spinner("Summarizing..."):

                    response = model.generate_content(prompt)

                st.markdown(response.text)
                st.session_state.history.append({

    "feature": "📝 Summarize Notes",

    "title": "Notes Summary",

    "answer": response.text

})
                st.download_button(
    label="📥 Download Summary",
    data=response.text,
    file_name="summary.txt",
    mime="text/plain"
)

            except Exception as e:

                st.error(e)

# ---------------- QUIZ GENERATOR ----------------

elif menu == "❓ Quiz Generator":

    st.title("❓ Quiz Generator")

    topic = st.text_input(
        "Enter a topic",
    
    )

    if st.button("Generate Quiz"):

        if topic.strip() == "":

            st.warning("Please enter a topic.")

        else:

            prompt = f"""
Create 5 MCQ questions.

Topic: {topic}

Each question should have:

A)

B)

C)

D)

Correct Answer:
"""

            try:

                with st.spinner("Generating quiz..."):

                    response = model.generate_content(prompt)

                st.markdown(response.text)
                
                st.session_state.history.append({

    "feature": "❓ Quiz Generator",

    "title": topic,

    "answer": response.text

})
                st.download_button(
    label="📥 Download Quiz",
    data=response.text,
    file_name="quiz.txt",
    mime="text/plain"
)

            except Exception as e:

                st.error(e)

# ---------------- FLASHCARDS ----------------

elif menu == "🗂️ Flashcards":

    st.title("🗂️ Flashcards")

    topic = st.text_input(
        "Enter a topic",

    )

    if st.button("Generate Flashcards"):

        if topic.strip() == "":

            st.warning("Please enter a topic.")

        else:

            prompt = f"""
Create 5 flashcards.

Topic: {topic}

Format:

Flashcard 1

Question:

Answer:
"""

            try:

                with st.spinner("Generating flashcards..."):

                    response = model.generate_content(prompt)

                st.markdown(response.text)
                st.session_state.history.append({

    "feature": "🗂️ Flashcards",

    "title": topic,

    "answer": response.text

})
                st.download_button(
    label="📥 Download Flashcards",
    data=response.text,
    file_name="flashcards.txt",
    mime="text/plain"
)

            except Exception as e:

                st.error(e)

# ---------------- PDF UPLOAD ----------------

elif menu == "📄 PDF Upload":

    st.title("📄 PDF Upload")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        try:

            reader = PdfReader(uploaded_file)

            text = ""

            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:

                    text += extracted

            st.success("PDF uploaded successfully")

            if st.button("Summarize PDF"):

                with st.spinner("Analyzing PDF..."):

                    response = model.generate_content(
                        f"Summarize this PDF:\n{text[:10000]}"
                    )

                st.markdown(response.text)
                st.session_state.history.append({

    "feature": "📄 PDF Upload",

    "title": uploaded_file.name,

    "answer": response.text

})
        except Exception as e:

            st.error(e)
            # ---------------- HISTORY ----------------

elif menu == "💬 History":

    st.title("💬 History")

    if st.session_state.history:

        st.write(f"Total History: {len(st.session_state.history)}")

        st.divider()

        for item in reversed(st.session_state.history):

            feature = item.get(
                "feature",
                "🧠 Explain Topic"
            )

            title = item.get(
                "title",
                item.get("topic", "Untitled")
            )

            answer = item.get(
                "answer",
                "No answer available"
            )

            with st.container():

                st.markdown(f"### {feature}")

                st.caption(title)

                with st.expander("📖 View Answer"):

                    st.markdown(answer)

                st.divider()

    else:

        st.info("No history available.")

# ---------------- FOOTER ----------------

st.divider()

st.caption("© 2026 AI Study Buddy | Developed by Sanjay Kumar Dhurwey")