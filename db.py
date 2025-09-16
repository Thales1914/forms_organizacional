import psycopg2
import streamlit as st

def conectar():
    url = st.secrets["supabase"]["url"]
    return psycopg2.connect(url)

def inicializar_db():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id SERIAL PRIMARY KEY,
            setor TEXT,
            colaborador TEXT,
            data DATE,
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
            score NUMERIC(5,2)
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inicializar banco: {e}")
        return False
