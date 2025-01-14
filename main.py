import openai
import os

os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    """Call the OpenAI chat model to validate and generate the SQL query based on the user question."""
    messages = [
        {"role": "system", "content": SYSTEM_CONTEXT},
        {"role": "user", "content": f"User question: {user_question}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=messages,
        temperature=0
    )

    generated_query = response.choices[0].message['content'].strip()
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
            generated_query = call_model(user_question)
            print(f"\nGenerated SQL Query:\n{generated_query}\n")

if __name__ == "__main__":
    main()