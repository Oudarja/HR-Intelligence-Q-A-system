from auto_schema_extractor import extract_mysql_schema
from embedder import embed_schema

if __name__ == "__main__":
    extract_mysql_schema()
    embed_schema()
