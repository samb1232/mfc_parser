import psycopg2
from sentence_transformers import SentenceTransformer
import chromadb

POSTGRES_CONFIG = {
    'dbname': 'mfc_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}


COLLECTION_NAME = "mfc_knowledge_base"


def fetch_records():
    """
    Подключается к базе данных и забирает все записи (id, текст ситуации).
    """
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM ticket;")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def sync_to_chromadb(records):
    """
    Принимает записи из базы, создаёт эмбеддинги и отправляет их в ChromaDB.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.Client()

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(name=COLLECTION_NAME)

    for rec_id, text in records:
        embedding = model.encode(text).tolist()
        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(rec_id)]
        )

    print(f"✅ Синхронизация завершена: {len(records)} записей загружено в ChromaDB.")

def main():
    records = fetch_records()
    sync_to_chromadb(records)

if __name__ == "__main__":
    main()
