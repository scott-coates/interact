def purge_data(graph_client):
  graph_client.query("""MATCH (n)
      OPTIONAL MATCH (n)-[r]-()
      DELETE n,r""")
