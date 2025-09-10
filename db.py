import sqlite3

def conectar():
    return sqlite3.connect("respostas.db", check_same_thread=False)

def inicializar_db():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS respostas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setor TEXT,
        colaborador TEXT,
        data TEXT,
        p1 TEXT, p2 TEXT,
        p3 TEXT, j3 TEXT,
        p4 TEXT, j4 TEXT,
        p5 TEXT, j5 TEXT,
        p6 TEXT, j6 TEXT,
        p7 TEXT, j7 TEXT,
        p8 TEXT, j8 TEXT,
        p9 TEXT, j9 TEXT,
        p10 TEXT, j10 TEXT,
        p11 TEXT, j11 TEXT,
        p12 TEXT,
        score INTEGER
    )
    """)
    conn.commit()
    return conn
