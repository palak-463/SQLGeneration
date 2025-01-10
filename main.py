from langchain.prompts import PromptTemplate
import openai
import re
import os

os.environ['OPENAI_API_KEY']="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"

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

def create_rag_system():
    prompt = PromptTemplate(
        input_variables=["system_context", "user_question"],
        template=PROMPT_TEMPLATE
    )
    return prompt

def generate_sql_query(user_question):
    api_key = openai.api_key
    full_prompt = PROMPT_TEMPLATE.format(
        system_context=SYSTEM_CONTEXT,
        user_question=user_question
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a SQL query generator. Return only SQL queries without any explanation."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def is_valid_query(query):
    valid_keywords = ["employee", "department", "salary", "manager", "name", "designation", "employeeid"]
    if any(re.search(r"\b" + keyword + r"\b", query.lower()) for keyword in valid_keywords):
        return True
    return False

def main():
    prompt = create_rag_system()
    api_key = os.environ['OPENAI_API_KEY']
    while True:
        user_question = input("\nPlease ask a SQL query related to the Employee table (press 'e' to exit): ")
        if user_question.lower() == 'e':
            print("Exiting...")
            break
        if is_valid_query(user_question):
            query = generate_sql_query(prompt, user_question, api_key)
            print(f"\nGenerated Query: {query}")
        else:
            print("\nSorry, I can only generate queries related to the employee table. Please try again.")

if __name__ == "__main__":
    main()