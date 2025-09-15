# Email Content Optimizer

## Overview

Email Content Optimizer is an AI-powered tool that helps users generate, evaluate, and refine professional emails. It leverages advanced language models and agent systems to ensure your emails are clear, actionable, and tailored to your audience.

## Problem Statement

Writing effective emails is challenging—users often struggle with tone, clarity, professionalism, and ensuring their message prompts the desired action. This app solves the problem by automatically generating an email, evaluating it using an AI agent, and iteratively improving it based on structured feedback. The process follows the **Reflect Evaluator Pattern** for optimal results.

## Features

- Generate professional emails from a topic or instruction
- AI-powered feedback on tone, clarity, professionalism, grammar, and more
- Iterative improvement using structured feedback
- Suggestions for subject lines and actionable content
- User-friendly Streamlit interface

## Technologies Used

- **Groq Langchain**: For fast, reliable language model integration
- **MoonshotAI Kimi K2 Instruct 0905**: The LLM model used for email generation and evaluation
- **LangGraph**: To build the AI agent system and workflow
- **Reflect Evaluator Pattern**: For iterative email optimization
- **Streamlit**: For the interactive web interface

## How It Works

1. Get your Groq API key from [Groq Console](https://console.groq.com/keys).
2. Enter your Groq API key and describe the email you want to write.
3. The app generates an initial email draft.
4. An AI agent evaluates the draft and provides structured feedback.
5. The email is refined based on feedback, repeating until high quality is achieved.
6. View both the initial and optimized emails, along with detailed feedback.

## Getting Started

1. Clone the repository:
   ```
   git clone <your-repo-url>
   ```
2. Create and activate a Python virtual environment:
   ```
   python -m venv my_venv
   .\my_venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```
   streamlit run sample.py
   ```

## Usage

- Enter your Groq API key in the app.
- Describe the email you want to generate (e.g., "Ask my manager for sick leave").
- Click "Optimize Email" to view the results and feedback.

---

**Built with Groq Langchain, LangGraph, and the Reflect Evaluator Pattern.**
