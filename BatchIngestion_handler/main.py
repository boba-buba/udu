from batch_ingestion_client_py import (
    BatchIngestor,
    Entity,
    ValueInLanguage,
)

ingestor = BatchIngestor(
    base_url='http://147.231.55.155',
    username="admin",
    password="2pigsontheroof",
)

print(ingestor.base_url())

#curl -X POST -H "Content-Type: application/json" cookies.txt -d '{"entities":[{"type": "item","labels": {"en": {"language": "en","value": "Simple"}}}]}'  http://147.231.55.155/w/rest.php/BatchIngestion/v0/batchcreate
