from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import HumanMessage
from langgraph.func import entrypoint, task
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

# Helper to get LLM with user API key
def get_llm(api_key):
    return ChatGroq(
        model="moonshotai/kimi-k2-instruct-0905",
        temperature=0.2,
        api_key=api_key
    )

# Helper to get evaluator with user LLM
def get_evaluator(llm):
    return llm.with_structured_output(Feedback)

# ------------------ Structured Feedback Schema ------------------
class Feedback(BaseModel):
    tone: str = Field(..., description="Tone of the email, e.g., formal, informal, friendly, assertive, etc.")
    clarity_score: float = Field(..., description="Score (0–10) representing how clear and understandable the email is.")
    professionalism_score: float = Field(..., description="Score (0–10) representing how professional the email sounds.")
    call_to_action_present: bool = Field(..., description="Whether a clear call-to-action is present in the email.")
    suggestions: List[str] = Field(..., description="Suggestions to improve tone, clarity, or effectiveness.")
    grammar_spelling_score: float = Field(..., description="Score (0–10) for grammatical correctness and spelling.")
    actionability: bool = Field(..., description="Is it clear what the recipient should do next?")
    audience_appropriateness: bool = Field(..., description="Is the tone/style suitable for the intended recipient?")
    subject_line_suggestion: str = Field(..., description="Suggested subject line for the email.")
    conciseness_score: float = Field(..., description="Score (0–10) for how concise and to-the-point the email is.")



# ------------------ Email Generator ------------------
@task
def llm_email_generator(topic: str, feedback: Feedback = None, api_key: str = None):
    llm = get_llm(api_key)
    if feedback:
        prompt = f"""
        Write a professional email on the topic '{topic}'.

        Structure:
        1. Introduction: Begin with a polite opener and briefly state the purpose.
        2. Main Content: Provide details clearly and concisely.
        3. Conclusion: Summarize and close politely.

        IMPORTANT:
        - Only return the email content itself (no analysis, no extra commentary).
        - Incorporate improvements based on this feedback: {feedback}
        - Pay special attention to grammar, spelling, conciseness, actionability, and audience appropriateness.
        - Suggest a subject line at the top.
    """
    else:
        prompt = f"""
        Write a professional email about the topic: '{topic}'.

        Structure:
        1. Introduction: Begin with a polite opener and briefly state the purpose.
        2. Main Content: Provide details clearly and concisely.
        3. Conclusion: Summarize and close politely.

        IMPORTANT:
        - Only return the email content itself (no analysis, no extra commentary).
        - Suggest a subject line at the top.
        - Ensure the email is clear, professional, actionable, and appropriate for the recipient.
    """

    response = llm.invoke(prompt)
    return {"email": response.content.strip()}

# ------------------ Email Evaluator ------------------
@task
def llm_email_evaluator(email: str, api_key: str = None):
    llm = get_llm(api_key)
    evaluator = get_evaluator(llm)
    prompt = f"""
    Please analyze the following email and provide structured feedback for each of the following aspects:

    - Tone
    - Clarity (0–10)
    - Professionalism (0–10)
    - Call-to-action presence
    - Suggestions for improvement
    - Grammar and spelling (0–10)
    - Actionability (is the next step clear?)
    - Audience appropriateness
    - Subject line suggestion
    - Conciseness (0–10)

    Email:
    {email}
    """

    feedback = evaluator.invoke(prompt)
    return {"feedback": feedback}

# ------------------ Optimizer Workflow ------------------
@entrypoint()
def optimizer_workflow(inputs):
    topic = inputs["topic"]
    api_key = inputs["api_key"]

    def is_email_prompt(text):
        if not text or len(text.strip()) < 10:
            return False
        keywords = ["email", "write", "request", "ask", "inform", "invite", "apply", "resign", "leave", "meeting", "reminder", "follow up", "apology", "proposal", "update", "feedback", "manager", "team", "client", "customer"]
        text_lower = text.lower()
        if any(word in text_lower for word in keywords):
            return True
        if text_lower.startswith("how ") or text_lower.startswith("please ") or text_lower.endswith("?"):
            return True
        return False

    if not is_email_prompt(topic):
        return {
            "error": "Please enter a proper question or instruction for the email you want to generate (e.g., 'Write an email to ask my manager for sick leave')."
        }

    feedback = None
    initial_email = None
    initial_feedback = None

    max_iterations = 3
    iteration = 0

    while iteration < max_iterations:
        email = llm_email_generator(topic, feedback, api_key).result()

        if initial_email is None:
            initial_email = email["email"]

        feedback = llm_email_evaluator(email["email"], api_key).result()

        if initial_feedback is None:
            initial_feedback = feedback["feedback"]

        if (
            feedback["feedback"].clarity_score >= 9.0
            and feedback["feedback"].professionalism_score >= 9.0
            and feedback["feedback"].call_to_action_present
            and feedback["feedback"].grammar_spelling_score >= 9.0
            and feedback["feedback"].actionability
            and feedback["feedback"].audience_appropriateness
            and feedback["feedback"].conciseness_score >= 8.5
            and len(feedback["feedback"].suggestions) < 2
        ):
            break

        iteration += 1

    return {
        "initial_email": initial_email,
        "initial_feedback": initial_feedback.dict(),
        "final_email": email["email"],
        "final_feedback": feedback["feedback"].dict(),
    }
