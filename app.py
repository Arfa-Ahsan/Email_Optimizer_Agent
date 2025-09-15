import streamlit as st

from email_optimizer import optimizer_workflow

st.set_page_config(page_title="Email Optimizer", layout="wide")

# Centered Title
st.markdown("<h1 style='text-align: center;'>Email Content Optimizer</h1>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='text-align: center;'>Feedback</h2>", unsafe_allow_html=True)
google_api_key = st.text_input("Enter your GROQ API Key:", type="password")
if not google_api_key:
    st.sidebar.warning("Please enter your GROQ API Key to continue.")
    st.stop()

# --- Input section ---
topic = st.text_input("Describe what the email should be about:", placeholder="e.g., Ask your manager for sick leave")

if st.button("Optimize Email") and topic:
    with st.spinner("Generating and evaluating email..."):
        try:
            result = optimizer_workflow.invoke(topic)

            if "error" in result:
                st.error(result["error"])
            else:
                initial_email = result["initial_email"]
                final_email = result["final_email"]
                fb = result["initial_feedback"]
                final_fb = result["final_feedback"]

                # --- Sidebar Feedback ---
                with st.sidebar.expander("Initial Feedback", expanded=True):
                    st.markdown(f"- **Tone**: {fb['tone']}")
                    st.markdown(f"- **Clarity**: {fb['clarity_score']} / 10")
                    st.markdown(f"- **Professionalism**: {fb['professionalism_score']} / 10")
                    st.markdown(f"- **Grammar/Spelling**: {fb['grammar_spelling_score']} / 10")
                    st.markdown(f"- **Conciseness**: {fb['conciseness_score']} / 10")
                    st.markdown(f"- **Call to Action**: {'Yes' if fb['call_to_action_present'] else 'No'}")
                    st.markdown(f"- **Actionability**: {'Yes' if fb['actionability'] else 'No'}")
                    st.markdown(f"- **Audience Appropriateness**: {'Yes' if fb['audience_appropriateness'] else 'No'}")
                    st.markdown(f"- **Subject Line Suggestion**: {fb['subject_line_suggestion']}")
                    st.markdown("**Suggestions:**")
                    for suggestion in fb["suggestions"]:
                        st.markdown(f"- {suggestion}")

                with st.sidebar.expander("Final Feedback", expanded=True):
                    st.markdown(f"- **Tone**: {final_fb['tone']}")
                    st.markdown(f"- **Clarity**: {final_fb['clarity_score']} / 10")
                    st.markdown(f"- **Professionalism**: {final_fb['professionalism_score']} / 10")
                    st.markdown(f"- **Grammar/Spelling**: {final_fb['grammar_spelling_score']} / 10")
                    st.markdown(f"- **Conciseness**: {final_fb['conciseness_score']} / 10")
                    st.markdown(f"- **Call to Action**: {'Yes' if final_fb['call_to_action_present'] else 'No'}")
                    st.markdown(f"- **Actionability**: {'Yes' if final_fb['actionability'] else 'No'}")
                    st.markdown(f"- **Audience Appropriateness**: {'Yes' if final_fb['audience_appropriateness'] else 'No'}")
                    st.markdown(f"- **Subject Line Suggestion**: {final_fb['subject_line_suggestion']}")
                    st.markdown("**Suggestions:**")
                    for suggestion in final_fb["suggestions"]:
                        st.markdown(f"- {suggestion}")

                # --- Display Emails ---
                st.subheader("Initial Email")
                st.markdown(
                    f"""<div style='background-color: #1e1e2f; color: white; padding: 1rem; border-radius: 10px; font-family: monospace; white-space: pre-wrap;'>{initial_email}</div>""",
                    unsafe_allow_html=True)

                st.subheader("Final Optimized Email")
                st.markdown(
                    f"""<div style='background-color: #1e1e2f; color: white; padding: 1rem; border-radius: 10px; font-family: monospace; white-space: pre-wrap;'>{final_email}</div>""",
                    unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Request failed: {e}")
else:
    st.info("Enter a topic and press 'Optimize Email'.")
