import os
from dotenv import load_dotenv
from pinecone import Pinecone
import logging

load_dotenv()
logger  = logging.getLogger('respackage.status.logger')

def status_check():
    # Initialize Pinecone client
    pine_key = os.getenv("PINECONE_API_KEY")
    if not pine_key:
        print("ERROR: PINECONE_API_KEY not set in .env file")
        return

    try:
        pc = Pinecone(api_key=pine_key)
        logger.info('pinecone connection established')
    except Exception as error:
        print(f"ERROR: Failed to initialize Pinecone client: {error}")
        return

    # list_indexes() yields IndexModel objects, whereas describe_index()
    # accepts an index name (a string). Passing the model caused the
    # PineconeApiValueError during request serialization.
    for index_name in pc.list_indexes().names():
        index_info = pc.describe_index(name=index_name)
        print(f"Index: {index_info.name}")
        print(f"  Dimension: {index_info.dimension}")
        print(f"  Metric: {index_info.metric}")
        print(f"  Spec: {index_info.spec}")
        print(f"  Status: {index_info.status}")
        
