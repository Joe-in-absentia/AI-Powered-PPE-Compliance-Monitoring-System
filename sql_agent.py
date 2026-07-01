import os
import re
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_URI = os.getenv("DB_URI")

# Load the gemini model.
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
         google_api_key=GOOGLE_API_KEY,temperature=0)

# Database connection.
db = SQLDatabase.from_uri(DB_URI,include_tables=[
        "detection_metadata","violation_details"])

# Clean sql.
def clean_sql(text):
    text = text.strip()
    text = re.sub(r"```sql", "",text,flags=re.IGNORECASE)
    text = re.sub(r"```", "",text)
    return text.strip()

# Chatbot function.
def ask_sql_agent(question):
    try:
        # Question filter.
        allowed_keywords = ["violation","violations","ppe","helmet","glove","mask","goggle",
            "goggles","safety","detection","detect","image","video","webcam","camera","today",
                  "date","count","total","report","history","source"]

        question_lower = question.lower()

        if not any(
            word in question_lower
            for word in allowed_keywords):
            return (
                "I can only answer "
                "IntelliGuard PPE violation analytics questions.")

        schema = db.get_table_info()

        sql_prompt = f"""
You are IntelliGuard AI.
Generate PostgreSQL SQL query for PPE violation analytics.

DATABASE TABLES:
{schema}

RULES:
1. ONLY generate SELECT queries.
2. Never use INSERT, UPDATE, DELETE, DROP, ALTER.
3. Use ONLY:
   - detection_metadata
   - violation_details
4. For today's data use:
   timestamp::date = CURRENT_DATE
5. Return ONLY SQL.
6. No markdown.
7. No explanation.

USER QUESTION:
{question}

SQL:
"""
        response = llm.invoke(sql_prompt)
        sql_query = clean_sql(response.content)
        print("GENERATED SQL:",sql_query)

        # For sql security.
        forbidden_words = ["insert","update","delete","drop","alter","truncate"]

        if (
            not sql_query.lower().startswith("select")
            or any(word in sql_query.lower()
                for word in forbidden_words)):

            return (
                "I can only answer "
                "IntelliGuard PPE violation analytics questions.")

        # Execute sql.
        result = db.run(sql_query)
        print("DATABASE RESULT:",result)

        if not result:
            return "No violation records found."

        # Final answer.
        answer_prompt = f"""
You are IntelliGuard AI assistant.
Convert this database result into a simple dashboard response.

Question:
{question}
Database Result:
{result}

Rules:
- Give a short answer.
- Mention important numbers.
- Do not mention SQL.
- Do not mention database.

Answer:
"""
        final_answer = llm.invoke(answer_prompt)
        return final_answer.content

    except Exception as e:
        logging.exception("SQL Agent Error")
        return (f"Error processing query: {str(e)}")


# Test the llm model performance.
if __name__ == "__main__":

    question = "How many violations happened today?"
    answer = ask_sql_agent(question)
    print("\nFINAL ANSWER:")
    print(answer)