
import streamlit as st
from resume_parser import extract_resume_text
from interview import generate_questions, evaluate_answer

st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Mock Interview Platform")
st.write("Practice interviews with personalized AI feedback.")

if "questions" not in st.session_state:
    st.session_state.questions = []

if "report" not in st.session_state:
    st.session_state.report = []

with st.sidebar:
    st.header("Interview Setup")

    job_role = st.text_input(
        "Target Job Role",
        placeholder="e.g. AI/ML Engineer"
    )

    resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if st.button("Generate Questions", type="primary"):
        if not job_role.strip():
            st.error("Please enter a job role.")

        elif not resume:
            st.error("Please upload your resume.")

        else:
            try:
                with st.spinner("AI is preparing your interview..."):
                    resume_text = extract_resume_text(resume)

                    if not resume_text.strip():
                        st.error(
                            "Resume se text nahi mila. "
                            "Please try another PDF."
                        )
                    else:
                        result = generate_questions(
                            job_role,
                            resume_text
                        )

                        # Debug: AI ka response screen par dikhayega
                       

                        questions = [
                            line.strip()
                            for line in result.splitlines()
                            if line.strip()
                        ]

                        st.session_state.questions = questions[:5]
                        st.session_state.report = []

                        if not st.session_state.questions:
                            st.error(
                                "AI ne questions return nahi kiye. "
                                "Please try again."
                            )
                        else:
                            st.success("Questions generated!")

            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.questions:
    st.subheader("Your Interview Questions")

    with st.form("interview_form"):
        answers = []

        for i, question in enumerate(
            st.session_state.questions
        ):
            st.markdown(f"**Question {i + 1}:** {question}")

            answer = st.text_area(
                "Your answer",
                key=f"answer_{i}",
                height=120
            )
            answers.append(answer)

        submitted = st.form_submit_button(
            "Evaluate My Answers",
            type="primary"
        )

    if submitted:
        report = []

        for question, answer in zip(
            st.session_state.questions,
            answers
        ):
            if answer.strip():
                try:
                    with st.spinner("Evaluating your answer..."):
                        feedback = evaluate_answer(
                            question,
                            answer
                        )

                    report.append({
                        "question": question,
                        "answer": answer,
                        "feedback": feedback
                    })

                except Exception as e:
                    st.error(f"Evaluation failed: {e}")

        st.session_state.report = report

if st.session_state.report:
    st.divider()
    st.header("📊 Your Interview Feedback")

    for i, item in enumerate(
        st.session_state.report,
        start=1
    ):
        with st.expander(f"Question {i}", expanded=True):
            st.write("**Question:**", item["question"])
            st.write("**Your answer:**", item["answer"])
            st.markdown(item["feedback"])

    report_text = "\n\n".join(
        f"Question: {item['question']}\n"
        f"Your answer: {item['answer']}\n"
        f"Feedback:\n{item['feedback']}"
        for item in st.session_state.report
    )

    st.download_button(
        "Download Interview Report",
        data=report_text,
        file_name="interview_report.txt",
        mime="text/plain"
    )