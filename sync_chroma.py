import psycopg2
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

client = chromadb.Client(Settings())

collection = client.get_or_create_collection(
    name="mfc_tickets",
    embedding_function=DefaultEmbeddingFunction()
)

conn = psycopg2.connect(
    dbname='mfc_db',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

cur = conn.cursor()
cur.execute("SELECT id, text FROM ticket")
rows = cur.fetchall()

ids = [str(row[0]) for row in rows]
docs = [row[1] for row in rows]

print(f"Всего документов: {len(docs)}")

collection.delete(ids=ids)

batch_size = 100
for i in range(0, len(docs), batch_size):
    batch_docs = docs[i:i + batch_size]
    batch_ids = ids[i:i + batch_size]
    collection.add(documents=batch_docs, ids=batch_ids)
    print(f"Добавлено {len(batch_docs)} документов")

cur.close()
conn.close()

print("Синхронизация завершена.")
