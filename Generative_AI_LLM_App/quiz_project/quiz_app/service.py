from openai import OpenAI
from .import config
import sqlite3

# API 키 설정
api_key = config.API_KEY
client = OpenAI(api_key=api_key)

def initialize_database():
    # SQLite 데이터베이스에 연결
    con = sqlite3.connect('question.db')
    cursor = con.cursor()

    # 테이블이 존재하지 않으면 생성
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                      (id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT)''')
    con.commit()
    con.close()

def generate_question(text):
    initialize_database()

    # SQLite 데이터베이스에 연결
    con = sqlite3.connect('question.db')
    cursor = con.cursor()

    # 프롬프트 생성
    messages = [
        {"role": "system", "content": "You are an assistant that generates multiple-choice questions."},
        {"role": "user", "content": f"Create a practice test with multiple choice questions on the following text:\n{text}\n\nEach question should be on a different line. Each question should have 4 possible answers. Under the possible answers, provide the correct answer."}
    ]

    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4",  # 또는 "gpt-3.5-turbo" 사용 가능
        messages=messages,
        max_tokens=3500,
        temperature=0.3
    )

    # 생성된 질문 추출
    questions = response.choices[0].message.content

    # 고유 키 생성
    base_key = ''.join(text.split()[:2])
    key = base_key

    index = 1
    
    while key_exists(cursor, key):
        key = f"{base_key}{index}"
        index += 1

    # 데이터베이스에 질문 삽입
    cursor.execute("INSERT INTO questions (key, value) VALUES (?, ?)", (key, questions))
    con.commit()
    con.close()
    
    return questions

def key_exists(cursor, key):
    cursor.execute("SELECT COUNT(*) FROM questions WHERE key = ?", (key,))
    count = cursor.fetchone()[0]
    return count > 0 

def print_all_questions():
    initialize_database()
    con = sqlite3.connect('question.db')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()
    con.close()

    return rows
