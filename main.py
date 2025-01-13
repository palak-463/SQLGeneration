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
Generate SQL queries based on user questions about this table structure.
Always return only the SQL query without any explanations.
"""

PROMPT_TEMPLATE = """
{system_context}
User question: {user_question}
1. Validate if the question is related to the employee table (structure provided above).
2. If the question is valid, generate the SQL query for it.
3. If the question is not valid, respond with "Invalid question. Please ask about the Employee table or related fields."
"""

def call_model(user_question):
    """Call the OpenAI model to generate the SQL query based on the user question."""
    full_prompt = PROMPT_TEMPLATE.format(
        system_context=SYSTEM_CONTEXT,
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
    generated_query = response.choices[0].message.content.strip()
    return generated_query

#def display_table():
    #"""Displays the sample employee table."""
    #print("\nSample Employee Table:\n")
    #print(f"{'Employee Name':<20} {'Employee ID':<10} {'Department':<15} {'Designation':<20} {'Salary':<10} {'Manager':<20}")
    #print("-" * 95)
    #sample_data = [
        #("John Doe", "E12345", "Engineering", "Software Engineer", 80000, "Jane Smith"),
        #("Alice Johnson", "E67890", "HR", "HR Manager", 70000, "David Lee"),
        #("Bob Brown", "E54321", "Sales", "Sales Executive", 60000, "Mike Tyson"),
    #]
    #for row in sample_data:
        #print(f"{row[0]:<20} {row[1]:<10} {row[2]:<15} {row[3]:<20} {row[4]:<10} {row[5]:<20}")
    #print("\n")

def is_valid_query(question):
    """Checks if the query contains valid keywords for the Employee table."""
    valid_keywords = ["employee", "department", "salary", "manager", "name", "designation", "employee id"]
    return any(re.search(r"\b" + keyword + r"\b", question.lower()) for keyword in valid_keywords)

def main():
    """Main function to run the SQL query generator."""
    print("\nWelcome to the SQL Query Generator!")
    print("Ask SQL-related questions about the Employee table. Type 'table' to view the sample table or 'exit' to exit.\n")
    
    while True:
        user_question = input("Please enter your question: ").strip()
        
        if user_question.lower() == 'exit':
            print("Exiting the SQL Query Generator. Goodbye!")
            break
        #elif user_question.lower() == 'table':
            #display_table()
        elif is_valid_query(user_question):
            generated_query = call_model(user_question)
            print(f"\nGenerated SQL Query:\n{generated_query}\n")
        else:
            print("\nInvalid question. Please ask about the Employee table or related fields.\n")

if __name__ == "__main__":
    main()