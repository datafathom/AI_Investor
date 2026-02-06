import psycopg2
import os
from dotenv import load_dotenv

def verify_phase_1_db():
    load_dotenv()
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT')
        )
        cur = conn.cursor()

        # 1. Check pgvector extension
        cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector'")
        extension = cur.fetchone()
        print(f"Vector Extension: {'INSTALLED' if extension else 'MISSING'}")

        # 2. Check agent_memories table
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'agent_memories'")
        table = cur.fetchone()
        print(f"Table agent_memories: {'EXISTS' if table else 'MISSING'}")

        if table:
            # 3. Check schema
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'agent_memories'
            """)
            columns = cur.fetchall()
            print("Schema columns:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")

            # 4. Check HNSW index
            cur.execute("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'agent_memories' AND indexdef LIKE '%hnsw%'
            """)
            index = cur.fetchone()
            print(f"HNSW Index: {'FOUND' if index else 'NOT FOUND'}")
            if index:
                print(f"  Index Definition: {index[1]}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    verify_phase_1_db()
