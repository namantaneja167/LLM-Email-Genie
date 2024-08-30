import gradio as gr
import groq
import os
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()
# Initialize the Groq client
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize an empty list to store chat history
chat_history = []

def generate_email(name: str, job_title: str, company_name: str, purpose: str, tone: str, length: str, jargon: str):
    prompt = f"""Write a cold email with the following details:
    Recipient: {name}, {job_title} at {company_name}
    Purpose: {purpose}
    Tone: {tone}
    Length: {length}
    Include industry jargon: {jargon}

    Please write the email now:"""

    # Add user input to chat history
    chat_history.append(("User", prompt))

    # Generate email using Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert cold email writer. Your task is to write personalized and effective cold emails based on the given information."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",
        max_tokens=1000,
    )

    # Extract the generated email
    generated_email = chat_completion.choices[0].message.content

    # Add generated email to chat history
    chat_history.append(("Assistant", generated_email))

    return generated_email, chat_history

# Define the Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# Cold Email Generator")
    
    with gr.Row():
        with gr.Column():
            name = gr.Textbox(label="Recipient Name")
            job_title = gr.Textbox(label="Job Title")
            company_name = gr.Textbox(label="Company Name")
        
        with gr.Column():
            purpose = gr.Textbox(label="Purpose of the Email")
            tone = gr.Radio(["Formal", "Casual", "Friendly"], label="Desired Tone")
            length = gr.Radio(["Short", "Medium", "Long"], label="Preferred Email Length")
            jargon = gr.Radio(["Yes", "No"], label="Include Industry-Specific Jargon")
    
    generate_button = gr.Button("Generate Email")
    output = gr.Textbox(label="Generated Email")

    generate_button.click(
        generate_email,
        inputs=[name, job_title, company_name, purpose, tone, length, jargon],
        outputs=[output]
    )

app.launch()