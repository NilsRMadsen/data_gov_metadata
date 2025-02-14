# Data.gov Metadata Visualization
## Nils Madsen

### Description
This project implements a local version of the Modern Data Stack, in order to visualize and explore metadata about the hundreds of thousands of datasets available on Data.gov (https://data.gov/). This metadata is a little more interesting from a data engineering and modeling standpoint than the published datasets themselves, as most of those are standalone and pre-aggregated, without any cross-referencing relational structure.

Using this metadata, we can answer questions like:
- Which government organizations have published the most datasets?
- What are the most popular dataset tags?
- How has the number of datasets grown over time?

### Components
All components of this project are completely free and open source:

1. The Data.gov CKAN metadata API (https://data.gov/developers/apis/)
2. The Python requests library (https://requests.readthedocs.io/en/latest/) for extracting the data
3. DuckDB (https://duckdb.org/docs/) as a local OLAP data warehouse
4. dbt Core (https://docs.getdbt.com/docs/core/installation-overview) for transforming and modeling the data
5. Dagster (https://docs.dagster.io/) for orchestration, end-to-end lineage tracing, and monitoring
6. Apache Superset (https://superset.apache.org/docs/intro) for visualizing the data

This project follows an ELT pattern, first extracting and loading the raw data directly into DuckDB, then using dbt to transform the data within the data warehouse.

Other convenient, but not required, tools for interacting with this project include:
1. DBeaver (https://dbeaver.io/) as a SQL editor for DuckDB

### A Quick Note on Ingestion
There are open-source tools available for ingestion, e.g. Airbyte and dltHub. I have chosen not to use them for this project because I felt they would overcomplicate and obscure what is otherwise a relatively simple ingestion pipeline. Therefore, I have elected to build a custom ingestion module with the requests library.