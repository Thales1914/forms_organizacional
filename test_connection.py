import psycopg2

URL = "postgresql://postgres.rrpdsbebwygaiptjzbvv:rhomeg%40123456712@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"

try:
    conn = psycopg2.connect(URL)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    versao = cursor.fetchone()
    print("✅ Conexão bem-sucedida!")
    print("Versão do PostgreSQL:", versao[0])
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Erro de conexão:", e)
