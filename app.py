import streamlit as st
import random
import re

# -----------------------------
# Helper Functions
# -----------------------------

def extract_keywords(text, top_n=5):
    """
    Simple keyword extractor:
    - Splits into words
    - Keeps longer words
    - Removes duplicates
    """
    words = re.findall(r"[A-Za-z]{5,}", text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    # Sort by frequency
    keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [k for k, v in keywords[:top_n]]


def generate_assignment_questions(keywords):
    """
    Generates 2 essay-style assignment questions
    based on extracted keywords.
    """
    questions = []
    if not keywords:
        keywords = ["topic"]

    q1 = f"Explain the significance of {keywords[0]} in the context of the provided topic."
    q2 = f"Discuss how {keywords[1] if len(keywords)>1 else keywords[0]} influences the broader themes presented in the text."

    return [q1, q2]


def generate_mcqs(text, keywords):
    """
    Generates 3 simple MCQ questions.
    Builds them using keywords and generic distractors.
    """
    if not keywords:
        keywords = ["topic"]

    distractors = ["communication", "analysis", "structure", "model", "system", "framework"]
    random.shuffle(distractors)

    mcqs = []
    for i, kw in enumerate(keywords[:3]):
        correct_answer = kw.capitalize()

        options = random.sample(distractors, 3)
        options.append(correct_answer)
        random.shuffle(options)

        question = {
            "question": f"What is a key concept mentioned in the text related to '{kw}'?",
            "options": options,
            "answer": correct_answer
        }
        mcqs.append(question)

    # Pad to 3 questions if keywords < 3
    while len(mcqs) < 3:
        mcqs.append({
            "question": "Which of the following best relates to the topic discussed?",
            "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
            "answer": "Concept A"
        })

    return mcqs[:3]


# -----------------------------
# Streamlit Front-End
# -----------------------------

st.title("📘 Assignment & Quiz Generator")
st.write("Generate essay assignments and MCQs from any text or topic.")

input_text = st.text_area("Enter your document or topic here:")

if st.button("Generate"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        # Extract keywords
        keywords = extract_keywords(input_text)

        # Generate assignments
        assignments = generate_assignment_questions(keywords)

        # Generate MCQs
        mcqs = generate_mcqs(input_text, keywords)

        # Display results
        st.subheader("📝 Assignment Questions")
        for i, q in enumerate(assignments, 1):
            st.write(f"**{i}. {q}**")

        st.subheader("❓ Multiple-Choice Quiz Questions")
        for i, item in enumerate(mcqs, 1):
            st.write(f"**{i}. {item['question']}**")
            for opt in item['options']:
                st.write(f"- {opt}")
            st.write(f"**Answer:** {item['answer']}")
            st.write("---")
