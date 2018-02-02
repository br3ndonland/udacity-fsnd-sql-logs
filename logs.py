#!/usr/bin/env python3

# Udacity database logs analysis project

# Import the psycopg2 module to work with PostgreSQL
import psycopg2

# Store the database name as an object for easy reference in functions
DBNAME = 'news'


# Create a helper function to re-use code shared among the three SQL queries
def get_query_results(query):
    """Helper function for code shared among the three SQL queries."""
    # Connect to database
    db = psycopg2.connect(database=DBNAME)
    # Create a cursor object to run queries and scan through results
    c = db.cursor()
    # Execute the SQL query using the cursor
    c.execute(query)
    # Fetch all results from the cursor object, and save as a results object
    result = c.fetchall()
    # Close connection
    db.close()
    return result


# 1. Most popular three articles
def popular_articles():
    """Returns a sorted list of the three most highly accessed articles,
    with the top article first.
    """
    # Save SQL query as object
    query = ("""
        select title, num from
            (select substr(path, 10), count(*) as num from log
            where path !='/' group by path)
        as hits, articles where substr = slug order by num desc limit 3;
        """)
    # Execute SQL query using the helper function
    result = get_query_results(query)
    # Print results
    print('\n', 'Query 1: Most popular three articles')
    for title, num in result:
        print('    {}  --  {} views'.format(title, num))
    pass


# 2. Most popular authors
def popular_authors():
    """Returns a sorted list of the most popular article authors,
    with the most popular author at the top.
    """
    # Save SQL query as object
    query = ("""
        select name, sum(views) as total_views from
            (select name, author, title, views from
                (select substr(path, 10), count(*) as views from log
                    where path !='/' group by path)
                as hits, articles, authors
                where substr = slug and author = authors.id
                order by views desc)
            as threetables group by name order by total_views desc;
        """)
    # Execute SQL query using the helper function
    result = get_query_results(query)
    # Print results
    print('\n', 'Query 2: Most popular authors')
    for name, total_views in result:
        print('    {}  --  {} views'.format(name, total_views))
    pass


# 3. Days on which >1% of HTTP requests led to errors
def errors():
    """Returns a list of days on which >1% of HTTP requests resulted in
    HTTP error codes.
    """
    # Save SQL query as object
    query = ("""
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
        """)
    # Execute SQL query using the helper function
    result = get_query_results(query)
    # Print results
    print('\n', 'Query 3: Days on which >1% HTTP requests returned 404 errors')
    for errdate, http_requests, http_404, errpct in result:
        print("    {:%B %d, %Y}  --  {:.2f}% errors".format(errdate, errpct))
    pass


if __name__ == "__main__":
    popular_articles()
    popular_authors()
    errors()
