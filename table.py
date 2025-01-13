import openai
import os

openai.api_key = "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"

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
"""

PROMPT_TEMPLATE = """
{system_context}
User question: {user_question}
Return only the SQL query that answers this question.
"""

message_history = [
    {"role": "system", "content": "You are a SQL query generator. Return only SQL queries without any explanation."},
    {"role": "system", "content": SYSTEM_CONTEXT}
]

def generate_sql_query(user_question):
    """
    Generate an SQL query based on the user's question, considering memory of recent interactions.
    """
    global message_history
    
    message_history.append({"role": "user", "content": user_question})
   
    message_history = message_history[-10:]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_history,
            temperature=0
        )

        assistant_reply = response.choices[0].message.content.strip()

        message_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def display_tables():
    """
    Display the structure of the Employee and Department tables for the user.
    """
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
    display_tables()
    """
    Main interactive loop for user questions.
    """
    print("Welcome to the SQL Query Generator!")
    print("You can ask questions related to the Employee and Department database.")
    print("Type 'exit' to quit.\n")
    while True:
        user_question = input("Enter your question: ").strip()
        if user_question.lower() == "exit":
            print("Goodbye! Have a great day!")
            break
        print("\nGenerating SQL query...\n")
        sql_query = generate_sql_query(user_question)
        if sql_query:
            print(f"SQL Query:\n{sql_query}\n")
        else:
            print("Failed to generate the query. Please try again.\n")

if __name__ == "__main__":
    main()