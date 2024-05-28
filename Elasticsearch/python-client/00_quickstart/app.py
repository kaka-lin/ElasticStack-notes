import os

from elasticsearch import Elasticsearch, helpers


# Execute the query
def search_data(client, index_name, query):
    try:
        response = client.search(index=index_name, body=query)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Connect to Elasticsearch
    # HOST: os.environ["ELASTICSEARCH_HOSTS"]
    client = Elasticsearch("http://localhost:9200/")
    # print(client.info()) # Confirm that the connection was successful.

    # Create an index with mappings
    mappings = {
        "properties": {
            "foo": {"type": "text"},
            "bar": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256,
                    }
                },
            },
        }
    }
    client.indices.create(index="my_index", mappings=mappings)

    # Create a document (Add data to the index)
    doc = {
        "foo": "foo",
        "bar": "bar",
    }
    client.index(index="my_index", id="my_document_id", document=doc)

    # index multiple documents at once with the bulk helper function
    def generate_docs():
        for i in range(10):
            yield {
                "_index": "my_index",
                "_id": f"my_document_id_{i}",
                "foo": f"foo {i}",
                "bar": f"bar {i}",
            }
    helpers.bulk(client, generate_docs())

    # Get documents
    client.get(index="my_index", id="my_document_id")

    # Search documents
    # Define the query
    query = {
        "query": {
            "match": {
                "foo": "foo"
            }
        }
    }

    # Get the results
    result = search_data(client, "my_index", query)

    # Process the results
    if result:
        print(result)
    else:
        print("Data not found or an error occurred.")
