import streamlit as st
from openai import Client
# from config import openai_api_key  # Import the API key
import os

openai_api_key = os.getenv("OPENAI_API_KEY")

openai = Client(openai_api_key) 
# Test cases (replace with your actual test cases)
test_cases = [
    "Write a poem about a sunflower.",
    "Generate a creative story about a robot who falls in love with a human.",
    "Summarize the key points of the article on climate change.",
]

# Prompt evaluation function (adjust evaluation criteria as needed)
def evaluate_prompt(prompt, generated_text):
    # Placeholder evaluation logic (replace with your actual metrics)
    fluency = 0.8  # Assess fluency and coherence
    relevance = 0.7  # Assess relevance to prompt
    creativity = 0.9  # Assess originality and creativity
    overall_score = (fluency + relevance + creativity) / 3
    return overall_score

# Define the main app layout
def main():
    st.title("OpenAI Text Generation with Streamlit")

    # Prompt input and test case selection
    prompt_source = st.radio("Prompt Source", ["User Input", "Test Cases"])
    if prompt_source == "User Input":
        prompt = st.text_input("Enter your prompt:")
    else:
        selected_test_case = st.selectbox("Choose a test case", test_cases)
        prompt = selected_test_case

    if st.button("Generate Text"):
        response = openai.create_completion(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.7  # Adjust for creativity
        )

        generated_text = response.choices[0].text

        # Display generated text and evaluation
        st.write("Generated Text:")
        st.write(generated_text)

        evaluation_score = evaluate_prompt(prompt, generated_text)
        st.write("Evaluation Score:", evaluation_score)

if __name__ == "__main__":
    main()
