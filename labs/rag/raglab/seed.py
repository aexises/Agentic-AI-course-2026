from .ingestion import corpus,chunk_documents
from .models import embed
from . import db

def seed():
    db.initialize()
    count=0
    for record in corpus():
        chunks=chunk_documents([record])
        vectors=embed([c['text'] for c in chunks])
        db.replace_document(record,chunks,vectors)
        count+=len(chunks)
    print(f'Upserted {len(corpus())} documents and {count} chunks; unrelated records retained.')
    return count

if __name__=='__main__': seed()
