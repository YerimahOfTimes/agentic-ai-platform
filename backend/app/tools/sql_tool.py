import sqlite3
from app.llm import llm


from app.core.config import DB_PATH


def run_sql_query(query: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()
        conn.commit()
        conn.close()

        if not rows:
            return "Query executed successfully."

        return "\n".join([str(row) for row in rows])

    except Exception as e:
        return f"SQL Error: {str(e)}"


def natural_language_to_sql(question: str):
    prompt = f"""
You convert user questions into SQLite SQL.

Database schema:
employees(id INTEGER, name TEXT, role TEXT, salary INTEGER)

Rules:
- Return ONLY SQL
- No explanation
- Only use SELECT queries
- Do not use DELETE, UPDATE, INSERT, DROP, ALTER

Question:
{question}
"""

    sql = llm.invoke(prompt).content.strip()

    dangerous = ["delete", "update", "insert", "drop", "alter", "truncate"]

    if any(word in sql.lower() for word in dangerous):
        return "SELECT 'Unsafe SQL blocked';"

    return sql


def run_natural_sql(question: str):
    sql = natural_language_to_sql(question)
    return run_sql_query(sql)
