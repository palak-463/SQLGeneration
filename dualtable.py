from langchain.prompts import PromptTemplate
import openai
import re
import os

os.environ['OPENAI_API_KEY'] = "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"

SYSTEM_CONTEXT = """
You are a SQL query generator. You understand the following database structures and their relationships:
Table: Employee
    - EmployeeID VARCHAR(50) PRIMARY KEY
    - Name VARCHAR(255)
    - DepartmentID VARCHAR(50) FOREIGN KEY REFERENCES Department(DepartmentID)
    - Designation VARCHAR(255)
    - Salary INT
    - ManagerID VARCHAR(50) FOREIGN KEY REFERENCES Employee(EmployeeID)
Table: Department
    - DepartmentID VARCHAR(50) PRIMARY KEY
    - DepartmentName VARCHAR(255)
    - Location VARCHAR(255)
Sample data in the Employee table:
- John Doe (E12345) works in the Engineering department (D001) as Software Engineer, salary 80000, reports to Jane Smith (E67890)
- Alice Johnson (E67890) works in HR (D002) as HR Manager, salary 90000, reports to David Lee (E54321)
- Bob Brown (E54321) works in Sales (D003) as Sales Executive, salary 60000, reports to Mike Tyson (E98765)
- Mike Tyson (E98765) works in Sales (D003) as Sales Manager, salary 95000, reports to None
Sample data in the Department table:
- D001: Engineering, Location: Building A
- D002: Human Resources, Location: Building B
- D003: Sales, Location: Building C
Relationships:
- Each employee belongs to one department.
- Employees can have managers who are also employees.
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

def generate_sql_query(system_context, user_question, api_key):
    
    openai.api_key = api_key
    full_prompt = PROMPT_TEMPLATE.format(
        system_context=system_context,
        user_question=user_question
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a SQL query generator. Return only SQL queries without any explanation."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message['content'].strip()

def is_valid_query(query):
    valid_keywords = [
        "employee", "department", "salary", "manager", "name",
        "designation", "employeeid", "departmentid", "location"
    ]
    if any(re.search(r"\b" + keyword + r"\b", query.lower()) for keyword in valid_keywords):
        return True
    return False

def display_tables():
    print("Employee Table Structure")
    print("""
    | EmployeeID | Name         | DepartmentID | Designation       | Salary | ManagerID |
    |------------|--------------|--------------|-------------------|--------|-----------|
    | E12345     | John Doe     | D001         | Software Engineer | 80000  | E67890    |
    | E67890     | Alice Johnson| D002         | HR Manager        | 90000  | E54321    |
    | E54321     | Bob Brown    | D003         | Sales Executive   | 60000  | E98765    |
    | E98765     | Mike Tyson   | D003         | Sales Manager     | 95000  | NULL      |
    """)
    print("Department Table Structure")
    print("""
    | DepartmentID | DepartmentName   | Location   |
    |--------------|------------------|------------|
    | D001         | Engineering      | Building A |
    | D002         | Human Resources  | Building B |
    | D003         | Sales            | Building C |
    """)

def main():
    prompt = create_rag_system()
    display_tables()
    example_questions = [
        "List the names of employees along with their respective department names.",
        "Find the average salary for each department.",
        "Retrieve all employees who report to managers in the 'Engineering' department.",
        "List each department and the number of employees working in it.",
        "Find employees who earn more than their managers.",
        "Show the names of employees along with their manager's name and department.",
        "Identify departments that have no employees assigned.",
        "List employees who are managers, along with the number of people they manage.",
        "Find the highest-paid employee in each department.",
        "Retrieve the names of employees along with the locations of their departments."
    ]
    api_key = os.environ['OPENAI_API_KEY']
    print("\nGenerating SQL Queries for Example Questions\n")
    for idx, question in enumerate(example_questions, 1):
        print(f"Q{idx}: {question}")
        user_question = question  
        if is_valid_query(question):
            try:
                query = generate_sql_query(SYSTEM_CONTEXT, user_question, api_key)
                print(f"SQL Query:\n{query}\n")
            except Exception as e:
                print(f"An error occurred while generating the query: {e}\n")
        else:
            print("Invalid question. Skipping.\n")

if __name__ == "__main__":
    main()