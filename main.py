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

message_history = [
    {"role": "system", "content": "You are a SQL query generator. Return only SQL queries or error messages."},
    {"role": "system", "content": SYSTEM_CONTEXT}
]

def call_model(user_question):
    """
    Call the OpenAI model to validate and generate the SQL query based on the user question.
    Maintains a chat history to provide context for better responses.
    """
    global message_history
    
    message_history.append({"role": "user", "content": user_question})
    
    message_history = message_history[-10:]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  
            messages=message_history,
            temperature=0
        )

        assistant_reply = response.choices[0].message['content'].strip()
        
        message_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return "An error occurred. Please try again."

def main():
    """
    Main function to run the SQL query generator interactively.
    """
    print("\nWelcome to the SQL Query Generator!")
    print("Ask SQL-related questions about the Employee table. Type 'exit' to exit.\n")
    while True:
        user_question = input("Please enter your question: ").strip()
        if user_question.lower() == 'exit':
            print("Exiting the SQL Query Generator. Goodbye!")
            break
        else:
            print("\nGenerating SQL query...\n")
            generated_query = call_model(user_question)
            print(f"Generated SQL Query:\n{generated_query}\n")

if __name__ == "__main__":
    main()