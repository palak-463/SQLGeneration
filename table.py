import openai
import os
 
openai.api_key = "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"
 
SYSTEM_CONTEXT = """ 
You are a SQL query generator; please use MS SQL dialect. You do not give Data Definition Queries like create, update, delete or alter queries, you only give queries which are related to fetching data from the table. Whenever the user asks for any records, you return a query which will fetch a maximum of 1000 data entries. You understand the following database structures and their relationships:
1. Table: PentanaCustomerVehicleMapping
    Primary Key: Id
    Columns:
    Id (int, NOT NULL, Identity)
    SalesServiceCaseId (nvarchar(50), NULL)
    UserId (nvarchar(50), NULL)
    CustomerId (nvarchar(50), NULL)
    VehicleId (nvarchar(50), NULL)
    Indexes:
    IX_PentanaCustomerVehicleMapping_CustomerId_Vehicleid (CustomerId, VehicleId)
2. Table: LabourSales_SoldHours
    Primary Key: Id
    Columns:
    Id (int, NOT NULL, Identity)
    YearStartdate (date, NULL)
    YearEnddate (date, NULL)
    MonthStartdate (date, NULL)
    MonthEnddate (date, NULL)
    DealerCode (nvarchar(255), NULL)
    DealerName (nvarchar(255), NULL)
    Brand (nvarchar(255), NULL)
    DMSProvider (nvarchar(40), NULL)
    SoldHoursofLabour (nvarchar(100), NULL)
    SoldHoursbyFRU (nvarchar(100), NULL)
    LabourAmount (nvarchar(100), NULL)
    Indexes:
    IX_LabourSales_SoldHours_DealerCode (DealerCode)
3. Table: PentanaCustomer
    Primary Key: Id
    Columns:
    Id (int, NOT NULL, Identity)
    CustomerId (varchar(50), NULL)
    DealerNumber (nvarchar(50), NULL)
    DealerName (nvarchar(50), NULL)
    FirstName (nvarchar(50), NULL)
    LastName (nvarchar(50), NULL)
    Email (nvarchar(100), NULL)
    MobilePhone (nvarchar(50), NULL)
    BirthDate (nvarchar(50), NULL)
4. Table: PentanaVehicle
    Primary Key: Id
    Columns:
    Id (int, NOT NULL, Identity)
    VehicleId (nvarchar(50), NULL)
    DealerNumber (nvarchar(50), NULL)
    DealerName (nvarchar(50), NULL)
    ShortVIN (nvarchar(50), NULL)
    LongVIN (nvarchar(50), NULL)
    Model (nvarchar(100), NULL)
    Brand (nvarchar(50), NULL)
    FirstRegistrationDate (nvarchar(50), NULL)
    WarrantyStartDate (nvarchar(50), NULL)
    Indexes:
    IX_PentanaVehicle_VehicleId_DealerNumber (VehicleId, DealerNumber)
5. Table: Throughput
    Primary Key: Id
    Columns:
    Id (int, NOT NULL, Identity)
    YearStartdate (date, NULL)
    YearEnddate (date, NULL)
    MonthStartdate (date, NULL)
    MonthEnddate (date, NULL)
    DealerCode (nvarchar(255), NULL)
    DealerName (nvarchar(255), NULL)
    Brand (nvarchar(255), NULL)
    DMSProvider (nvarchar(40), NOT NULL)
    InvoiceType (nvarchar(40), NOT NULL)
    Quantity (decimal(17,2), NULL)
    QuantityInculdeIsBodyShopLocation (decimal(17,2), NULL)
    Indexes:
    IX_Throughput_DealerCode (DealerCode)
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
            model="gpt-4o-mini",
            messages=message_history,
            temperature=0
        )

        assistant_reply = response.choices[0].message.content.strip()

        message_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def main():
    """
    Main interactive loop for user questions.
    """
    print("Welcome to the SQL Query Generator!")
    print("You can ask questions related to the Employee and Department tables.")
    print("Type 'exit' to quit.\n")
    while True:
        user_question = input("Enter your question: ").strip()
        if user_question.lower() == "exit":
            print("Goodbye!")
            break
        sql_query = generate_sql_query(user_question)
        if sql_query:
            print(f"SQL Query:\n{sql_query}\n")
        else:
            print("Failed to generate the query. Please try again.\n")

if __name__ == "__main__":
    main()