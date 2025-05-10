import psycopg2
import chromadb
from config import Config
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

def update_chromadb():
    client = chromadb.Client(Settings())
    collection = client.get_or_create_collection(
        name="mfc_tickets",
        embedding_function=DefaultEmbeddingFunction()
    )
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
        
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM ticket")
    rows = cur.fetchall()
    ids = [str(row[0]) for row in rows]
    docs = [row[1] for row in rows]

    if ids:
        collection.delete(ids=ids)
        
    batch_size = 100
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        collection.add(documents=batch_docs, ids=batch_ids)

    cur.close()
    conn.close()
    return {"status": "success", "message": f"Updated {len(docs)} documents"}


def get_situation_from_chromadb_by_id(ticket_id):
    client = chromadb.Client(Settings())
    collection = client.get_or_create_collection(
        name="mfc_tickets",
        embedding_function=DefaultEmbeddingFunction()
    )
        
    result = collection.get(ids=[str(ticket_id)])
    if result and result['documents']:
        return {
            "status": "success",
            "document": result['documents'][0]
        }
    return {"status": "not_found"}