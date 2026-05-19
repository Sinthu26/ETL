# CanadaLens ETL Pipeline

Ever try to find a job through the Canadian Job Bank and it looks so cluttered? 
CanadaLens is the solution. It is an ETL pipeline that tracks the Canadian tech 
job market. It works by extracting job postings from the Canada Job Bank, cleaning 
and transforming the data, and loading it into a structured SQLite database for analysis.

## How it works

All the data on the job market is extracted and filtered — for example, if there is 
no salary, a 0 is used as a placeholder, and rows without job titles are dropped entirely. 
The cleaned data then gets loaded into a SQLite database so it is easy to access and query. 
This pipeline runs automatically every Monday via GitHub Actions. The loader is idempotent, 
meaning if the pipeline runs twice in one day, no duplicate rows are ever inserted into the database.

## Tech Stack

- Python
- Pandas
- SQLite3
- Requests
- GitHub Actions

## How to run it

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the pipeline:

```bash
python pipeline.py
```

## What it produces

It produces a clean SQLite database containing over 27,000 job postings across 
Ontario, British Columbia, Alberta, and Québec. You can query the database to 
answer questions like which cities are hiring most, what the average salary is 
by province, or which job titles appear most frequently.