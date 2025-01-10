from langchain.prompts import PromptTemplate
import openai
import re
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
Sample data in the table:
- John Doe (E12345) works in Engineering as Software Engineer, salary 80000, reports to Jane Smith
- Alice Johnson (E67890) works in HR as HR Manager, salary 70000, reports to David Lee
- Bob Brown (E54321) works in Sales as Sales Executive, salary 60000, reports to Mike Tyson
Generate SQL queries based on user questions about this data.
Always return only the SQL query without any explanations.
"""

PROMPT_TEMPLATE = """
{system_context}
User question: {user_question}
Return only the SQL query that answers this question.
"""

def display_table():
    """Displays the sample employee table."""
    print("\nSample Employee Table:\n")
    print(f"{'Employee Name':<20} {'Employee ID':<10} {'Department':<15} {'Designation':<20} {'Salary':<10} {'Manager':<20}")
    print("-" * 95)
    sample_data = [
        ("John Doe", "E12345", "Engineering", "Software Engineer", 80000, "Jane Smith"),
        ("Alice Johnson", "E67890", "HR", "HR Manager", 70000, "David Lee"),
        ("Bob Brown", "E54321", "Sales", "Sales Executive", 60000, "Mike Tyson"),
    ]
    for row in sample_data:
        print(f"{row[0]:<20} {row[1]:<10} {row[2]:<15} {row[3]:<20} {row[4]:<10} {row[5]:<20}")
    print("\n")

def generate_sql_query(user_question):
    """Generates SQL query using OpenAI ChatCompletion API."""
    full_prompt = PROMPT_TEMPLATE.format(
        system_context=SYSTEM_CONTEXT,
        user_question=user_question
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a SQL query generator. Return only SQL queries without any explanation."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def is_valid_query(query):
    """Checks if the query contains valid keywords for the Employee table."""
    valid_keywords = ["employee", "department", "salary", "manager", "name", "designation", "employeeid"]
    return any(re.search(r"\b" + keyword + r"\b", query.lower()) for keyword in valid_keywords)

def main():
    """Main function to run the SQL query generator."""
    print("\nWelcome to the SQL Query Generator! ")
    print("Ask SQL-related questions about the Employee table. Type 'table' to view the sample table or 'e' to exit.\n")
    while True:
        user_question = input("Please enter your question: ")
        if user_question.lower() == 'e':
            print("Exiting the SQL Query Generator. Goodbye! ")
            break
        elif user_question.lower() == 'table':
            display_table()
        elif is_valid_query(user_question):
            query = generate_sql_query(user_question)
            print(f"\nGenerated SQL Query:\n{query}\n")
        else:
            print("\n Invalid question. Please ask about the Employee table or related fields.\n")

if __name__ == "__main__":
    main()