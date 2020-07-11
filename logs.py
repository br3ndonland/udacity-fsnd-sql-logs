"""
SQL database logs analysis project
Udacity Full Stack Developer Nanodegree program
Brendon Smith https://github.com/br3ndonland/udacity-fsnd-sql-logs
"""
import os
import records


def query_result(query, is_file=False):
    """Helper function used to execute SQL queries.
    ---
    - Connect to database
    - Read SQL query
    - Execute SQL query with Records
    - Save result as object and return
    """
    if os.environ.get("DATABASE_URL"):
        db_uri = os.environ.get("DATABASE_URL")
    else:
        db_uri = "postgresql://vagrant@localhost/news"
    db = records.Database(db_uri)
    return db.query_file(query) if is_file is True else db.query(query)


def popular_articles():
    """1. Most popular three articles
    ---
    - Input path to SQL query
    - Execute SQL query using helper function
    - Print results, with top article first
    """
    query = "sql/1-most-popular-articles.sql"
    result = query_result(query, is_file=True)
    print("\nQuery 1: Most popular three articles")
    for title, num in result:
        print(f"    {title}  --  {num} views")


def popular_authors():
    """2. Most popular authors
    ---
    - Input path to SQL query
    - Execute SQL query using helper function
    - Print a sorted list of the most popular article authors
    """
    query = "sql/2-most-popular-authors.sql"
    result = query_result(query, is_file=True)
    print("\nQuery 2: Most popular authors")
    for name, total_views in result:
        print(f"    {name}  --  {total_views} views")


def errors():
    """3. Days on which >1% of HTTP requests led to errors
    ---
    - Input path to SQL query
    - Execute SQL query using helper function
    - Print days on which 1% or more HTTP requests returned errors
    """
    query = "sql/3-http-request-error-rate.sql"
    result = query_result(query, is_file=True)
    print("\nQuery 3: Days on which >1% HTTP requests returned 404 errors")
    for errdate, http_requests, http_404, errpct in result:
        print(f"    {errdate:%B %d, %Y}  --  {errpct:.2f}% errors")


if __name__ == "__main__":
    popular_articles()
    popular_authors()
    errors()
