# Airflow ETL Pipeline (Crypto API)

## Overview

This project demonstrates a basic ETL pipeline using:

- Apache Airflow
- Python
- PostgreSQL
- Docker

The pipeline extracts data from an external API, transforms it using Python, and loads it into PostgreSQL.

---

## Architecture

API → Airflow → Python ETL → PostgreSQL

---

## Tech Stack

- Airflow (orchestration)
- Python (data extraction & transformation)
- PostgreSQL (storage)
- Docker (environment)

---

## How to Run

```bash
docker compose up --build