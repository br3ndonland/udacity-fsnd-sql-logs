#!/usr/bin/env python3

# Udacity database logs analysis project

# Import the psycopg2 module to work with PostgreSQL
import psycopg2

# Store the database name as an object for easy reference in functions
DBNAME = 'news'


# 1. Most popular three articles
def popular_articles():
    """Returns a sorted list of the three most highly accessed articles,
    with the top article first.
    """
    # Connect to database
    db = psycopg2.connect(database=DBNAME)
    # Create a cursor object to run queries and scan through results
    c = db.cursor()
    # Execute the SQL query using the cursor
    c.execute("""
        select title, num from
            (select substr(path, 10), count(*) as num from log
            where path !='/' group by path)
        as hits, articles where substr = slug order by num desc limit 3;
        """)
    # Fetch all results from the cursor object
    print('\n', 'Query 1: Most popular three articles')
    for table in c.fetchall():
        print(table[0], int(table[1]))
    # Close connection
    db.close()
    pass


# 2. Most popular authors
def popular_authors():
    """Returns a sorted list of the most popular article authors,
    with the most popular author at the top.
    """
    # Connect to database
    db = psycopg2.connect(database=DBNAME)
    # Create a cursor object to run queries and scan through results
    c = db.cursor()
    # Execute the SQL query using the cursor
    c.execute("""
        select name, sum(views) as total_views from
            (select name, author, title, views from
                (select substr(path, 10), count(*) as views from log
                    where path !='/' group by path)
                as hits, articles, authors
                where substr = slug and author = authors.id
                order by views desc)
            as threetables group by name order by total_views desc;
        """)
    # Fetch all results from the cursor object
    print('\n', 'Query 2: Most popular authors')
    for table in c.fetchall():
        print(table[0], int(table[1]))
    # Close connection
    db.close()
    pass


# 3. Days on which >1% of HTTP requests led to errors
def errors():
    """Returns a list of days on which >1% of HTTP requests resulted in
    HTTP error codes.
    """
    # Connect to database
    db = psycopg2.connect(database=DBNAME)
    # Create a cursor object to run queries and scan through results
    c = db.cursor()
    # Execute the SQL query using the cursor
    c.execute("""
        select requests.date, http_requests, http_404 from
            (select date_trunc('day', time) as date, count(*)
            as http_requests from log group by date)
            as requests,
            (select date_trunc('day', time) as date, count(*)
            as http_404 from log where status = '404 NOT FOUND' group by date)
            as errors
        where requests.date = errors.date
        and errors.http_404 > 0.01 * requests.http_requests
        order by requests.date desc;
        """)
    # Fetch all results from the cursor object
    print('\n', 'Query 3: Days on which >1% HTTP requests returned 404 errors')
    for table in c.fetchall():
        # Convert datetime to string and slice to retain only the date
        print('Date:', str(table[0])[:10])
        # Calculate error rate
        print('Percent errors:', float(table[2]) / float(table[1]) * 100)
    # Close connection
    db.close()
    pass
