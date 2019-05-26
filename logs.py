"""
SQL database logs analysis project
Udacity Full Stack Developer Nanodegree program
Brendon Smith https://github.com/br3ndonland/udacity-fsnd-sql-logs
"""

import psycopg2


def get_query_results(query):
    """Helper function for code shared among the three SQL queries.
    ---
    - Connect to database
    - Create a cursor object to run queries and scan results
    - Execute SQL query using cursor
    - Fetch all results from cursor object
    - Save as results object
    - Close connection
    """
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def popular_articles():
    """1. Most popular three articles
    ---
    - Save SQL query as object
    - Execute SQL query using helper function
    - Print results, with top article first
    """
    query = """
        select title, num from
            (select substr(path, 10), count(*) as num from log
            where path !='/' group by path)
        as hits, articles where substr = slug order by num desc limit 3;
        """
    result = get_query_results(query)
    print("\nQuery 1: Most popular three articles")
    for title, num in result:
        print(f"    {title}  --  {num} views")


def popular_authors():
    """2. Most popular authors
    ---
    - Save SQL query as object
    - Execute SQL query using helper function
    - Print a sorted list of the most popular article authors
    """
    query = """
        select name, sum(views) as total_views from
            (select name, author, title, views from
                (select substr(path, 10), count(*) as views from log
                    where path !='/' group by path)
                as hits, articles, authors
                where substr = slug and author = authors.id
                order by views desc)
            as threetables group by name order by total_views desc;
        """
    result = get_query_results(query)
    print("\nQuery 2: Most popular authors")
    for name, total_views in result:
        print(f"    {name}  --  {total_views} views")


def errors():
    """3. Days on which >1% of HTTP requests led to errors
    ---
    - Save SQL query as object
    - Execute SQL query using helper function
    - Print days on which 1% or more HTTP requests returned errors
    """
    query = """
        select errdate, http_requests, http_404,
        100.0 * http_404 / http_requests as errpct from
            (select date_trunc('day', time) as reqdate, count(*)
            as http_requests from log group by reqdate)
            as requests,
            (select date_trunc('day', time) as errdate, count(*)
            as http_404 from log where status = '404 NOT FOUND'
            group by errdate)
            as errors
        where reqdate = errdate
        and errors.http_404 > 0.01 * requests.http_requests
        order by errdate desc;
        """
    result = get_query_results(query)
    print("\nQuery 3: Days on which >1% HTTP requests returned 404 errors")
    for errdate, http_requests, http_404, errpct in result:
        print(f"    {errdate:%B %d, %Y}  --  {errpct:.2f}% errors")


if __name__ == "__main__":
    popular_articles()
    popular_authors()
    errors()
