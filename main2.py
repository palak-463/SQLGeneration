import openai
import os

# Set your OpenAI API key here
os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define system context to guide the model
SYSTEM_CONTEXT = """
You are a SQL query generator. You understand the following database structure:
    Employee Name VARCHAR(255),
    Employee ID VARCHAR(50),
    Department VARCHAR(255),
    Designation VARCHAR(255),
    Salary INT,
    Manager VARCHAR(255)

Your task is to:
1. Check if the user's question relates to the above table structure.
2. If valid, generate a corresponding SQL query.
3. If not valid, respond with "Invalid question. Please ask about the Employee table or related fields."
"""

def call_model(user_question):
    """Call the OpenAI model to validate and generate the SQL query based on the user question."""
    prompt = f"""
    {SYSTEM_CONTEXT}
    User question: {user_question}
    """

    # Call the OpenAI API for response
    response = openai.Completion.create(
        model="gpt-4o-mini",  # You can use a model like GPT-4 or GPT-3.5
        prompt=prompt,
        max_tokens=150,
        temperature=0
    )

    # Get the generated response from the model
    generated_query = response.choices[0].text.strip()
    return generated_query

def main():
    """Main function to run the SQL query generator."""
    print("\nWelcome to the SQL Query Generator!")
    print("Ask SQL-related questions about the Employee table. Type 'exit' to exit.\n")
    
    while True:
        user_question = input("Please enter your question: ").strip()
        
        if user_question.lower() == 'exit':
            print("Exiting the SQL Query Generator. Goodbye!")
            break
        else:
            # Call the model to validate and generate the SQL query
            generated_query = call_model(user_question)
            print(f"\nGenerated SQL Query:\n{generated_query}\n")

if __name__ == "__main__":
    main()
