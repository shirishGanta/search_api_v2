\## Bonus 1: Design Notes



While building this search API, I considered a few different design approaches:



1\. \*\*In‑Memory Search (Chosen Approach)\*\*  

&nbsp;  - Fetch data from the external `/messages` API and filter it in memory.  

&nbsp;  - Simple, fast to implement, and ideal for small datasets.  

&nbsp;  - Works well for demonstration and low‑traffic use cases.



2\. \*\*Database‑Backed Search (SQLite FTS5)\*\*  

&nbsp;  - Store messages in a local SQLite database with full‑text search enabled.  

&nbsp;  - Allows indexing and faster queries for larger datasets.  

&nbsp;  - Easy to maintain and deploy with minimal overhead.



3\. \*\*Elasticsearch / OpenSearch\*\*  

&nbsp;  - Distributed search engine for large‑scale production systems.  

&nbsp;  - Provides fuzzy search, ranking, and near‑real‑time indexing.  

&nbsp;  - Best suited for millions of records and high‑traffic environments.



I chose the in‑memory approach for simplicity and quick deployment, since the goal is to demonstrate search and pagination logic.



\## Bonus 2: Data Insights



To reduce latency to around \*\*30 ms\*\*, the following optimizations can be applied:



\- \*\*Cache responses:\*\*  

&nbsp; Use Redis or an in‑memory cache to store frequent queries and avoid repeated API calls.



\- \*\*Asynchronous I/O:\*\*  

&nbsp; Convert the endpoint to `async def` and use `httpx` for non‑blocking requests.



\- \*\*Pre‑index data:\*\*  

&nbsp; Store messages in a database with text indexes (e.g., SQLite FTS5 or PostgreSQL GIN).



\- \*\*Deploy closer to the data source:\*\*  

&nbsp; Host the API in the same region as the external `/messages` service to minimize network latency.



\- \*\*Batch and reuse connections:\*\*  

&nbsp; Keep persistent HTTP sessions to reduce connection overhead.

