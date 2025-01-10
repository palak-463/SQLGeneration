from langchain_core.prompts import PromptTemplate  
import openai  
import os
import re

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

api_key = os.environ['OPENAI_API_KEY']
 
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
 
def main():
    prompt = create_rag_system()
    example_questions = [
        "Generate a query to list all employees reporting to 'Jane Smith', including their departments and designations.",
        "Generate a query to calculate the average salary of employees in the Engineering department.",
        "Generate a query to find the highest and lowest salaries of employees in the company.",
        "Generate a query to show all employees with salaries greater than 75000, including their managers.",
        "Generate a query to display all employees working in the HR department along with their designations and departments.",
        "Generate a query to retrieve employees with salary between 60000 and 70000, sorted by salary.",
        "Generate a query to find the department with the highest number of employees.",
        "Generate a query to show the total number of employees in the 'Sales' department.",
        "Generate a query to list employees with salary below 65000, including their managers.",
        "Generate a query to retrieve all employees whose names start with the letter 'A'.",
        "Generate a query to list employees with their salary and department who report to 'Mike Tyson'.",
        "Generate a query to find the average salary for each department.",
        "Generate a query to retrieve all employees in the 'Sales' department, showing their designations.",
        "Generate a query to count how many employees have 'John' anywhere in their name.",
        "Generate a query to list employees whose designation includes the word 'Manager'.",
        "Generate a query to find the total number of employees whose EmployeeID starts with 'E6'."
    ]
    for question in example_questions:
        query = generate_sql_query(prompt, question, api_key)
        print(f"\nQuestion: {question}")
        print(f"Generated Query: {query}")
 
if __name__ == "__main__":
    main()