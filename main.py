from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer, models
import ssl
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
es_endpoint = os.environ["es_endpoint"]
es_cert_path = os.environ["es_cert_path"]

# SSL context for Elasticsearch connection
context = ssl.create_default_context(cafile=es_cert_path)

# Connect to the Elasticsearch server
es = Elasticsearch([es_endpoint], ssl_context=context)

# Define a function to get the model
def get_model(model_name='airesearch/wangchanberta-base-att-spm-uncased', max_seq_length=768, condition=True):
    if condition:
        word_embedding_model = models.Transformer(model_name, max_seq_length=max_seq_length)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode='cls')
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    return model

# Initialize the model
en_encoder = get_model(model_name="BAAI/bge-large-en-v1.5", max_seq_length=1024)

# Create index with mapping for embeddings
index_name = "test-index-2"
create_index_body = {
    "settings": {
        "index": {
        "analysis": {
            "analyzer": {
            "analyzer_shingle": {
                "tokenizer": "icu_tokenizer",
                "filter": [
                "filter_shingle"
                ]
            }
            },
            "filter": {
            "filter_shingle": {
                "type": "shingle",
                "max_shingle_size": 3,
                "min_shingle_size": 2,
                "output_unigrams": "true"
            }
            }
        }
        }
    },  
    "mappings": {
        "properties": {
            "en_character": {"type": "text"},
            "en_character_description": {"type": "text", "analyzer": "analyzer_shingle"},
            "vector_en": {
                "type": "dense_vector",
                "dims": 1024,
                "index": True,
                "similarity": "cosine"
            }
        }
    }
}
if not es.indices.exists(index=index_name):
    print(f"Index '{index_name}' does not exist. Creating a new one")
else:
    response = es.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted successfully.")
es.indices.create(index=index_name, body=create_index_body)
    

# Define the documents
docs = [
    {
        'author': 'John Doe',
        'title': 'Introduction to Elasticsearch',
        'text': 'Elasticsearch is great for searching and analyzing text.',
        'timestamp': datetime.now(),
    },
    {
        'author': 'Jane Smith',
        'title': 'Advanced Elasticsearch Queries',
        'text': 'Understanding queries is crucial for using Elasticsearch effectively.',
        'timestamp': datetime.now(),
    }
]

# Index the documents with semantic embeddings and raw text
for i, doc in enumerate(docs, start=1):
    # Generate embeddings
    embedding = en_encoder.encode(doc['text'])

    # Index document with both raw text and embeddings
    res = es.index(index=index_name, id=i, body={
        'author': doc['author'],
        'title': doc['title'],
        'en_character': doc['text'],
        'timestamp': doc['timestamp'],
        'vector_en': embedding.tolist()  # Store embedding
    })
    print(f"Document {i} indexing result: {res['result']}")



search_term = "Elasticsearch?"  # Intentionally misspelled for demonstration


# # Get all data
# resp = es.search(index=index_name, query={"match_all":{}})
# for hit in resp['hits']['hits']:
#     print(hit['_source']['th_character'])

print("\nFuzzy search\n")
# Fuzzy search
fuzzy_query = {
    "query": {
        "fuzzy": {
            "en_character": {
                "value": search_term,
                "fuzziness": "AUTO"  # You can adjust the fuzziness level
            }
        }
    }
}

res = es.search(index=index_name, body=fuzzy_query)
print(f"Got {res['hits']['total']['value']} Hits:")
for hit in res['hits']['hits']:
    print(f"Document: {hit['_source']['en_character']}")

print("\nSemantic search\n")
# Semantic search
semantic_query_en = {
    "field": "vector_en",
    "query_vector": en_encoder.encode(search_term),
    "k": 4,
    "num_candidates": 20
}


semantic_resp_en = es.search(index=index_name, knn=semantic_query_en)
for hit in semantic_resp_en['hits']['hits']:
    print(hit['_score'])
    print(hit['_source']['en_character'])
