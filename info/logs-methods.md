# SQL database logs analysis project computational narrative

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo">
</a>

[Udacity Full Stack Developer Nanodegree program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

Brendon Smith ([br3ndonland](https://github.com/br3ndonland))

[![code license](https://img.shields.io/badge/code%20license-MIT-blue.svg?longCache=true&style=for-the-badge)](https://choosealicense.com/licenses/mit/)

## Table of Contents <!-- omit in toc -->

- [Setup](#setup)
- [Starting Python in `logs.py`](#starting-python-in-logspy)
- [Starting the virtual machine and exploring the data](#starting-the-virtual-machine-and-exploring-the-data)
- [A tale of three queries](#a-tale-of-three-queries)
  - [1. Most popular articles](#1-most-popular-articles)
  - [2. Most popular authors](#2-most-popular-authors)
  - [3. HTTP request error rate](#3-http-request-error-rate)

## Setup

- I read through the Udacity documentation and rubric (see _[logs-udacity.md](logs-udacity.md)_)
- I kept vagrant and the database in a separate directory because of the large size of the database file.

## Starting Python in `logs.py`

- Shebang: when reading through the "Functionality" section of the rubric, I saw that it recommended "a correct shebang line to indicate the Python version." I actually hadn't written a shebang line before, but looked it up on [Stack Overflow](https://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script) and drafted one.
- I created an outline in the python file `logs.py` with the steps I would be working on. Here's the initial outline:

  ```py
  #!/usr/bin/env python3

  # Udacity database logs analysis project

  # 1. Most popular three articles

  # 2. Most popular authors

  # 3. Days on which >1% of HTTP requests led to errors

  ```

_To function or not to function:_ Next, I decided to write each of the three queries as a Python function. I began building the functions based on the resources from _Lesson 03. Python DB-API_:

- `forumdb.py`
- _3.3. Writing Code with DB API_
- _3.16. Reference — Python DB-API_

```py
#!/usr/bin/env python3

# Udacity database logs analysis project

# Import the psycopg2 module to work with PostgreSQL
import psycopg2

# Store the database name as an object for easy reference in functions
DBNAME = "news"


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
    c.execute()
    # Fetch all results from the cursor object
    articles = c.fetchall()
    print(articles)
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
    c.execute()
    # Fetch all results from the cursor object
    authors = c.fetchall()
    print(authors)
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
    c.execute()
    # Fetch all results from the cursor object
    errors = c.fetchall()
    print(errors)
    # Close connection
    db.close()
    pass

```

Git commit at this point: "Initialize files and code outline"

[(Back to TOC)](#table-of-contents)

## Starting the virtual machine and exploring the data

- I already had vagrant installed from the instructions in _Lesson 2.17. Installing the Virtual Machine_.
- I unzipped *newsdata.sql- and moved it into the *vagrant- directory.
- I changed into the vagrant directory and started up vagrant (only necessary when restarting computer):

```sh
$ vagrant up
```

- I then logged in to Ubuntu as before

  ```sh
  $ vagrant ssh
  ```

- I connected to the database and loaded the data with PostgreSQL:

  ```sh
  $ cd /vagrant
  /vagrant$ psql -d news -f newsdata.sql
  ```

  As explained in the Udacity documentation for the project (see [logs-udacity.md](logs-udacity.md)):

  > Here's what this command does:
  >
  > - `psql` — the PostgreSQL command line program
  > - `-d news` — connect to the database named news which has been set up for you
  > - `-f newsdata.sql` — run the SQL statements in the file newsdata.sql
  >
  > Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

  This only needs to be done once. When reconnecting, after `vagrant up` and `vagrant ssh`, simply use

  ```sh
  $ cd /vagrant
  /vagrant$ psql -d news
  ```

  and to log out (the opposite of `vagrant ssh`), just type ctrl+d or

  ```sh
  $ logout
  ```

- I then began exploring the data by running commands in the vagrant Linux terminal. This helped me understand how to build the SQL queries.
- I started by viewing the tables:

  ```text
  /vagrant$ psql -d news
  psql (9.5.10)
  Type "help" for help.

  news=> \dt
            List of relations
   Schema |   Name   | Type  |  Owner
  --------+----------+-------+---------
   public | articles | table | vagrant
   public | authors  | table | vagrant
   public | log      | table | vagrant
  (3 rows)
  ```

- Next, I viewed the columns of each table.
  - `\d articles`
  - `\d authors`
  - `\d log`
- I then broke it down further and started looking at the content of the columns.
  - `select author from articles limit 10;` The `author` column in the `articles` table is a foreign key, "articles_author_fkey" that references the author `id` in the `authors` table.
  - `select slug from articles;` shows there are only 8 articles.
  - `select path from log limit 10;` `path` looks like `slug` from the `articles` table, but it is repeated every time the article is accessed. We need to group and count the paths to find out how many times each article was accessed.
- I tried out some of the SQL queries from the Udacity project instructions, like

  ```sql
  select title, name
  from articles, authors
  where articles.author = authors.id;
  ```

[(Back to TOC)](#table-of-contents)

## A tale of three queries

Helpful reference info when building the SQL queries:

- _2.18. Reference — Elements of SQL_
- _3.16. Reference — Python DB-API_
- _4.15. Reference — Deeper into SQL_

I broke each query down, as recommended in the [Udacity instructions](https://github.com/br3ndonland/udacity-fsnd03-p01-logs/blob/master/logs-udacity.md#q-these-queries-are-complicated-where-do-i-start), and repeatedly iterated until I got it.

[(Back to TOC)](#table-of-contents)

### 1. Most popular articles

_What are the most popular three articles of all time?_

#### Use the `log` table to count hits by `path`

I started by figuring out how to aggregate `path` and count hits in the `log` table. I based my first successful query on _1.11. Quiz: Count All the Species_.

```sql
news=> select path, count(*) as num from log group by path order by num desc;
```

This shows a list of 212 rows.

```text
                path                 |  num
-------------------------------------+--------
 /                                   | 479121
 /article/candidate-is-jerk          | 338647
 /article/bears-love-berries         | 253801
 /article/bad-things-gone            | 170098
 /article/goats-eat-googles          |  84906
 /article/trouble-for-troubled       |  84810
 /article/balloon-goons-doomed       |  84557
 /article/so-many-bears              |  84504
 /article/media-obsessed-with-bears  |  84383
 /spam-spam-spam-humbug              |    301
 /%20%20%20                          |    290
 /+++ATH0                            |    288
 /article/candidate-is-jerkx         |    161
 /article/candidate-is-jerkq         |    155
:
```

This was helpful. The top hit was the home page, which makes sense. The next top hits were the eight articles on the site.

I could see that there were a number of mistyped URLs. I decided not to group those with the correct URLs above, because users aren't technically accessing the page with a mistyped URL. The same users who mistyped the URL are probably correcting the URL and going to the page anyway, and thus still contributing to the total number of hits on the correct URL.

I limited the results to three, and offset by one (to take out the homepage "/" path) with `limit 3 offset 1;`, giving me only the articles of interest:

```sql
news=> select path, count(*) as num from log group by path order by num desc limit 3 offset 1;
```

The `offset 1` isn't totally ideal, because it's possible for one of the articles to be viewed more times than the homepage. I revised the code to exclude the homepage:

```sql
news=> select path, count(*) as num from log where path !='/' group by path order by num desc limit 3;
```

```text
            path             |  num
-----------------------------+--------
 /article/candidate-is-jerk  | 338647
 /article/bears-love-berries | 253801
 /article/bad-things-gone    | 170098
(3 rows)
```

#### Convert `path` in `log` to match `slug` in `articles`

Let's review the two tables we're trying to join:

```sql
news=> select id, slug, title from articles;
```

```text
 id |           slug            |               title
----+---------------------------+------------------------------------
 23 | bad-things-gone           | Bad things gone, say good people
 24 | balloon-goons-doomed      | Balloon goons doomed
 25 | bears-love-berries        | Bears love berries, alleges bear
 26 | candidate-is-jerk         | Candidate is jerk, alleges rival
 27 | goats-eat-googles         | Goats eat Google's lawn
 28 | media-obsessed-with-bears | Media obsessed with bears
 30 | trouble-for-troubled      | Trouble for troubled troublemakers
 29 | so-many-bears             | There are a lot of bears
(8 rows)
```

```sql
news=> select path, count(*) as num from log where path !='/' group by path order by num desc limit 3;
```

```text
            path             |  num
-----------------------------+--------
 /article/candidate-is-jerk  | 338647
 /article/bears-love-berries | 253801
 /article/bad-things-gone    | 170098
(3 rows)
```

Let's start by just trying a simple join between the two tables.

```sql
news=> select path, slug from log, articles limit 10;
```

```text
            path            |           slug
----------------------------+---------------------------
 /                          | bad-things-gone
 /                          | balloon-goons-doomed
 /                          | bears-love-berries
 /                          | candidate-is-jerk
 /                          | goats-eat-googles
 /                          | media-obsessed-with-bears
 /                          | trouble-for-troubled
 /                          | so-many-bears
 /article/candidate-is-jerk | bad-things-gone
 /article/candidate-is-jerk | balloon-goons-doomed
(10 rows)
```

Alright, so that's totally mismatched.

There is no foreign key here, but the `path` column is similar to the `slug` column in the articles table. I will need to slice the contents of each row in the `path` column to remove `/article/` from the list, to match with the `slug`, like `path[9:]` if it was Python.

This was a sticking point for me. I was stuck at this step for about a day. I had to browse my notes and documentation. I was thinking about using the `LIKE` operator to match based on certain conditions, but that doesn't really slice out the contents of each row in the `path` column.

I was looking through ["A Gentle Introduction to SQL Using SQLite Part II"](https://github.com/tthibo/SQL-Tutorial), that I was referred to during [computefest2018-pandas](https://github.com/Harvard-IACS/computefest2018-pandas). I got to the [`SUBSTRING` section](https://github.com/tthibo/SQL-Tutorial/blob/master/tutorial_files/part2.textile#substr), tried reformatting my query to select a substring in the `path` column of the `log` table, and... that was it!

```sql
news=> select substr(path, 10), count(*) as num from log where path !='/' group by path order by num desc limit 3;
```

```text
       substr       |  num
--------------------+--------
 candidate-is-jerk  | 338647
 bears-love-berries | 253801
 bad-things-gone    | 170098
(3 rows)
```

**Yes!**

#### Combine the hit count and the join of `log` and `articles` into a single SQL statement

Now time to write the full query! I started off just drafting it in plain English:

> I want to join the `log` table with the `articles` table, where the `substr` from `log` matches the `slug` from `articles`, and show the `title` column from `articles` with the `num` count column created by the aggregation in `log`.

Wow, alright. Let's break that down:

- where the `substr` from `log` matches the `slug` from `articles`:

  ```sql
  where log.substr = articles.slug
  ```

- show the `title` column from `articles` with the `num` count column created by the aggregation in `log`:

  ```sql
  select title, num
  ```

Now let's put that together.

My first query didn't work:

```sql
select title, num from articles,
  (select substr(path, 10), count(*) as num from log where path !='/' group by path order by num desc) as hits
where log.substr = articles.slug limit 3;
```

I had to break it down further. I started by working the successful query into a subquery, to select just the `num` column from the aggregation. This worked:

```sql
select num from (select substr(path, 10), count(*) as num from log where path !='/' group by path order by num desc limit 3) as hits;
```

```text
  num
--------
 338647
 253801
 170098
(3 rows)
```

Next, I continued iterating to get my first join of `log` and `articles`:

```sql
news=> select title, num from (select substr(path, 10), count(*) as num from log where path !='/' group by path order by num desc limit 3) as hits, articles limit 3;
```

```text
              title               |  num
----------------------------------+--------
 Bad things gone, say good people | 338647
 Bad things gone, say good people | 253801
 Bad things gone, say good people | 170098
(3 rows)
```

Now I needed to establish the join condition. After a few more iterations, I got it! I also changed "num" to "views" for easier interpretation here:

```sql
news=> select title, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles where substr = slug order by views desc limit 3;
```

```text
              title               | views
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
(3 rows)
```

This also showed me that the order of columns in the `SELECT` statement doesn't need to match the order the tables are mentioned in the `FROM` statement.

#### Add the first SQL query to the Python code

I plugged this into the Python code in `logs.py` to test it out. I reformatted the SQL query for Python with help from the [psycopg2](http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries) docs:

```py
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
        select title, views from
            (select substr(path, 10), count(*) as views from log
            where path !='/' group by path)
        as hits, articles where substr = slug order by views desc limit 3;
        """)
    # Fetch all results from the cursor object
    return c.fetchall()
    # Close connection
    db.close()
    pass

```

In order to run the Python code within Vagrant, I created a _vagrant/logs_ directory and copied in the `logs.py` file.

I then formatted the Linux command line argument to call the function, with a little help from [Stack Overflow](https://stackoverflow.com/questions/3987041/python-run-function-from-the-command-line#3987113) via a [DuckDuckGo](https://duckduckgo.com) search for "run python functions from command line":

```sh
vagrant@vagrant:/vagrant/logs$ python -c 'import logs; print(logs.popular_articles())'
```

```text
[('Candidate is jerk, alleges rival', 338647L), ('Bears love berries, alleges bear', 253801L), ('Bad things gone, say good people', 170098L)]
```

I will need to reformat the output into a plain-text table like PostgreSQL. I'm surprised that `psycopg2` doesn't return SQL tables as output by default. Isn't that what you would expect?

I tried a few different things. There is a `PrettyTable` module, but the Python distribution with Vagrant doesn't have it. I'll get back to this after finishing the second and third queries.

[(Back to TOC)](#table-of-contents)

### 2. Most popular authors

_Who are the most popular article authors of all time?_

The second query is like an extension of the first, with an additional join to the authors table, and an aggregation to group the articles by author.

#### Join the three tables

I started off viewing the `name` and `id` columns from the `authors` table, so I knew what to look for:

```sql
news=> select name, id from authors;
```

```text
          name          | id
------------------------+----
 Ursula La Multa        |  1
 Rudolf von Treppenwitz |  2
 Anonymous Contributor  |  3
 Markoff Chaney         |  4
(4 rows)
```

Next, I merged the `log` table and `articles` table as before, eliminating the `limit 3`, and including `author` id, to display all eight articles:

```sql
select title, author, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles where substr = slug order by views desc;
```

```text
               title                | author | views
------------------------------------+--------+--------
 Candidate is jerk, alleges rival   |      2 | 338647
 Bears love berries, alleges bear   |      1 | 253801
 Bad things gone, say good people   |      3 | 170098
 Goats eat Google's lawn            |      1 |  84906
 Trouble for troubled troublemakers |      2 |  84810
 Balloon goons doomed               |      4 |  84557
 There are a lot of bears           |      1 |  84504
 Media obsessed with bears          |      1 |  84383
(8 rows)
```

Now to join the three tables, displaying information from all three to verify:

```sql
select name, author, title, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles, authors where substr = slug and author = authors.id order by views desc;
```

```text
          name          | author |               title                | views
------------------------+--------+------------------------------------+--------
 Rudolf von Treppenwitz |      2 | Candidate is jerk, alleges rival   | 338647
 Ursula La Multa        |      1 | Bears love berries, alleges bear   | 253801
 Anonymous Contributor  |      3 | Bad things gone, say good people   | 170098
 Ursula La Multa        |      1 | Goats eat Google's lawn            |  84906
 Rudolf von Treppenwitz |      2 | Trouble for troubled troublemakers |  84810
 Markoff Chaney         |      4 | Balloon goons doomed               |  84557
 Ursula La Multa        |      1 | There are a lot of bears           |  84504
 Ursula La Multa        |      1 | Media obsessed with bears          |  84383
(8 rows)
```

The second query, up to this point, only took me a few iterations over maybe an hour. The next part took me several more hours.

#### Aggregate article views by author

_Aggregation aggravation:_ This step was more difficult. I tried creating views, but wasn't able to create a view and select from that view in the same SQL query (remember each of the three queries has to be a self-contained query).

I started moving in the right direction by nesting the entire subquery from the "Join the three tables" step above inside another query:

```sql
select name, views from
(select name, author, title, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles, authors where substr = slug and author = authors.id order by views desc) as threetables;
```

```text
          name          | views
------------------------+--------
 Rudolf von Treppenwitz | 338647
 Ursula La Multa        | 253801
 Anonymous Contributor  | 170098
 Ursula La Multa        |  84906
 Rudolf von Treppenwitz |  84810
 Markoff Chaney         |  84557
 Ursula La Multa        |  84504
 Ursula La Multa        |  84383
(8 rows)
```

This narrows down the table to the columns I want, but I still need the aggregation.

I was able to successfully complete the aggregation by adding two parts:

- `sum(views) as total_views` at the beginning, before the long nested subquery
- `group by name order by total_views desc`, after the long nested subquery, to tell `psql` how to compute the sum.

```sql
select name, sum(views) as total_views from
    (select name, author, title, views from
        (select substr(path, 10), count(*) as views from log
            where path !='/' group by path)
        as hits, articles, authors
        where substr = slug and author = authors.id
        order by views desc)
    as threetables group by name order by total_views desc;
```

```text
          name          | total_views
------------------------+-------------
 Ursula La Multa        |      507594
 Rudolf von Treppenwitz |      423457
 Anonymous Contributor  |      170098
 Markoff Chaney         |       84557
(4 rows)
```

**Success!**

#### Add the second SQL query to the Python code

```py
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
    return c.fetchall()
    # Close connection
    db.close()
    pass
```

I copied the updated code into the vagrant directory as before, then ran the code from the Linux command line:

```sh
vagrant@vagrant:/vagrant/logs$ python -c 'import logs; print(logs.popular_articles(), logs.popular_authors())'
```

```text
([('Candidate is jerk, alleges rival', 338647L), ('Bears love berries, alleges bear', 253801L), ('Bad things gone, say good people', 170098L)], [('Ursula La Multa', Decimal('507594')), ('Rudolf von Treppenwitz', Decimal('423457')), ('Anonymous Contributor', Decimal('170098')), ('Markoff Chaney', Decimal('84557'))])
```

Git commit at this point:

"Complete SQL queries one and two"

[(Back to TOC)](#table-of-contents)

### 3. HTTP request error rate

_On which days did more than one percent of requests lead to errors?_

I need to sum the total number of HTTP requests, and divide by the number of HTTP `404` error codes.

I started by reviewing the contents of the `log` table:

```text
\d log
```

```text
                                  Table "public.log"
 Column |           Type           |                    Modifiers
--------+--------------------------+--------------------------------------------------
 path   | text                     |
 ip     | inet                     |
 method | text                     |
 status | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
```

A quick view of the `status` column in the `log` table shows two status codes, `200 OK` and `404 NOT FOUND`:

```sql
news=> select status from log group by status;
```

```text
    status
---------------
 404 NOT FOUND
 200 OK
(2 rows)
```

Each HTTP request returns a `status` and `time`:

```sql
news=> select status, time from log limit 5;
```

```text
 status |          time
--------+------------------------
 200 OK | 2016-07-01 07:00:00+00
 200 OK | 2016-07-01 07:00:47+00
 200 OK | 2016-07-01 07:00:34+00
 200 OK | 2016-07-01 07:00:52+00
 200 OK | 2016-07-01 07:00:23+00
(5 rows)
```

#### Group requests by day

The `time` column contains more than just the date. I will have to slice out the time.

I took a look at the PostgreSQL documentation, and quickly found the entry for [`EXTRACT, date_part`](https://www.postgresql.org/docs/9.5/static/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT). After reading through and trying it out, I actually found that [`date_trunc`](https://www.postgresql.org/docs/9.5/static/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC) was more appropriate. It sets the time of day to zero, while keeping the date the same:

```sql
select date_trunc('day', time) as date, status from log limit 5;
```

```text
          date          | status
------------------------+--------
 2016-07-01 00:00:00+00 | 200 OK
 2016-07-01 00:00:00+00 | 200 OK
 2016-07-01 00:00:00+00 | 200 OK
 2016-07-01 00:00:00+00 | 200 OK
 2016-07-01 00:00:00+00 | 200 OK
(5 rows)
```

I tried slicing out the time completely with a substring command.

```sql
news=> select substr(date_trunc('day', time), 1, 10) as date from log limit 5;
```

I couldn't get it to work initially, but I will return to this later if needed.

I was able to group the entries by date, revealing that the table was logging HTTP requests in July 2016:

```sql
select date_trunc('day', time) as date from log group by date;
```

```text
          date
------------------------
 2016-07-01 00:00:00+00
 2016-07-02 00:00:00+00
 2016-07-03 00:00:00+00
 2016-07-04 00:00:00+00
 2016-07-05 00:00:00+00
 2016-07-06 00:00:00+00
 2016-07-07 00:00:00+00
 2016-07-08 00:00:00+00
 2016-07-09 00:00:00+00
 2016-07-10 00:00:00+00
 2016-07-04 00:00:00+00
 2016-07-05 00:00:00+00
 2016-07-06 00:00:00+00
 2016-07-07 00:00:00+00
 2016-07-08 00:00:00+00
 2016-07-09 00:00:00+00
 2016-07-10 00:00:00+00
 2016-07-11 00:00:00+00
 2016-07-12 00:00:00+00
 2016-07-13 00:00:00+00
 2016-07-14 00:00:00+00
 2016-07-15 00:00:00+00
 2016-07-16 00:00:00+00
 2016-07-17 00:00:00+00
 2016-07-18 00:00:00+00
 2016-07-19 00:00:00+00
 2016-07-20 00:00:00+00
 2016-07-21 00:00:00+00
 2016-07-22 00:00:00+00
 2016-07-23 00:00:00+00
 2016-07-24 00:00:00+00
 2016-07-25 00:00:00+00
 2016-07-26 00:00:00+00
```

#### Count the number of HTTP requests per day

One of my query attempts actually hung the virtual machine. I think it was including `from log` at the top level of the query.

I logged in with a separate terminal window and used the `top` command to troubleshoot.

```text
/vagrant$ psql -d news
psql (9.5.10)
Type "help" for help.
```

```sql
news=> select date, status, http_requests from log,
(select date_trunc('day', time) as date from log) as datemod,
(select count(*) as http_requests from log) as requests
 order by date limit 10;
```

In a separate terminal window:

```sh
$ vagrant ssh
vagrant@vagrant:~$ top
```

```text
top - 13:12:30 up 15:05,  2 users,  load average: 0.97, 0.50, 0.20
Tasks: 110 total,   2 running, 108 sleeping,   0 stopped,   0 zombie
%Cpu(s): 98.7 us,  1.3 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  1024012 total,   585268 free,    56496 used,   382248 buff/cache
KiB Swap:  1048572 total,  1048572 free,        0 used.   798024 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
 1508 postgres  20   0  202820  18888  12676 R 99.9  1.8   3:18.07 postgres
  852 message+  20   0    6044   3696   3320 S  0.3  0.4   0:02.86 dbus-daemon
 3947 vagrant   20   0   13172   4676   3976 S  0.3  0.5   0:00.04 sshd
    1 root      20   0    6744   5168   3820 S  0.0  0.5   0:01.87 systemd
    2 root      20   0       0      0      0 S  0.0  0.0   0:00.00 kthreadd
    3 root      20   0       0      0      0 S  0.0  0.0   0:00.11 ksoftirqd/0
    5 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 kworker/0:0H
    7 root      20   0       0      0      0 S  0.0  0.0   0:01.04 rcu_sched
    8 root      20   0       0      0      0 S  0.0  0.0   0:00.00 rcu_bh
    9 root      rt   0       0      0      0 S  0.0  0.0   0:00.00 migration/0
   10 root      rt   0       0      0      0 S  0.0  0.0   0:00.62 watchdog/0
   11 root      20   0       0      0      0 S  0.0  0.0   0:00.00 kdevtmpfs
   12 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 netns
   13 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 perf
   14 root      20   0       0      0      0 S  0.0  0.0   0:00.01 khungtaskd
   15 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 writeback
   16 root      25   5       0      0      0 S  0.0  0.0   0:00.00 ksmd
```

I actually couldn't kill the process.

```sh
vagrant@vagrant:~$ kill -9 1508
```

```text
-sh: kill: (1508) - Operation not permitted
```

Typing `logout` doesn't do anything, because I don't have a command prompt. Quitting my terminal program (iTerm2) reveals a process still running in VirtualBox. I sent an ACPI shutdown signal through the GUI (can also be done on command line with `VBoxManage controlvm Ubuntu acpipowerbutton`).

Okay, time to try again.

I started building the query, piece by piece.

This at least runs and establishes the count syntax:

```sql
select count(*) as http_requests from log group by time limit 5;
```

Now to build in the date truncation:

```sql
select date_trunc('day', time) as date, count(*) as http_requests from log group by date order by date desc;
```

```text
          date          | http_requests
------------------------+---------------
 2016-07-31 00:00:00+00 |         45845
 2016-07-30 00:00:00+00 |         55073
 2016-07-29 00:00:00+00 |         54951
 2016-07-28 00:00:00+00 |         54797
 2016-07-27 00:00:00+00 |         54489
 2016-07-26 00:00:00+00 |         54378
 2016-07-25 00:00:00+00 |         54613
 2016-07-24 00:00:00+00 |         55100
 2016-07-23 00:00:00+00 |         54894
 2016-07-22 00:00:00+00 |         55206
 2016-07-21 00:00:00+00 |         55241
 2016-07-20 00:00:00+00 |         54557
 2016-07-19 00:00:00+00 |         55341
 2016-07-18 00:00:00+00 |         55589
 2016-07-17 00:00:00+00 |         55907
 2016-07-16 00:00:00+00 |         54498
 2016-07-15 00:00:00+00 |         54962
 2016-07-14 00:00:00+00 |         55196
 2016-07-13 00:00:00+00 |         55180
 2016-07-12 00:00:00+00 |         54839
 2016-07-11 00:00:00+00 |         54497
 2016-07-10 00:00:00+00 |         54489
 2016-07-09 00:00:00+00 |         55236
 2016-07-08 00:00:00+00 |         55084
 2016-07-07 00:00:00+00 |         54740
 2016-07-06 00:00:00+00 |         54774
 2016-07-05 00:00:00+00 |         54585
 2016-07-04 00:00:00+00 |         54903
 2016-07-03 00:00:00+00 |         54866
 2016-07-02 00:00:00+00 |         55200
 2016-07-01 00:00:00+00 |         38705
(31 rows)
```

**Alright!**

#### Count the number of errors per day

I modified the total HTTP requests query to return the HTTP 404 errors:

```sql
select date_trunc('day', time) as date, count(*) as http_404 from log where status = '404 NOT FOUND' group by date order by date desc;
```

```text
          date          | http_404
------------------------+----------
 2016-07-31 00:00:00+00 |      329
 2016-07-30 00:00:00+00 |      397
 2016-07-29 00:00:00+00 |      382
 2016-07-28 00:00:00+00 |      393
 2016-07-27 00:00:00+00 |      367
 2016-07-26 00:00:00+00 |      396
 2016-07-25 00:00:00+00 |      391
 2016-07-24 00:00:00+00 |      431
 2016-07-23 00:00:00+00 |      373
 2016-07-22 00:00:00+00 |      406
 2016-07-21 00:00:00+00 |      418
 2016-07-20 00:00:00+00 |      383
 2016-07-19 00:00:00+00 |      433
 2016-07-18 00:00:00+00 |      374
 2016-07-17 00:00:00+00 |     1265
 2016-07-16 00:00:00+00 |      374
 2016-07-15 00:00:00+00 |      408
 2016-07-14 00:00:00+00 |      383
 2016-07-13 00:00:00+00 |      383
 2016-07-12 00:00:00+00 |      373
```

**Excellent!**

Note the single quotes around `status = '404 NOT FOUND'`. I tried double quotes first, but double quotes make PostgreSQL think `"404 NOT FOUND"` is a column name, and it returns an error.

The two steps above for counting total HTTP requests and errors separately took me ~2-3 hours over Sunday afternoon 20180128 and Monday morning 20180129.

#### Combine the counts of total HTTP requests and HTTP 404 errors into a single table

##### Review

Now I need to combine the two queries from above:

```sql
select date_trunc('day', time) as date, count(*) as http_requests from log group by date order by date desc;
```

```sql
select date_trunc('day', time) as date, count(*) as http_404 from log where status = '404 NOT FOUND' group by date order by date desc;
```

I need to join the two queries on date. This is a similar task to the [first query](#1-most-popular-articles), where I joined the `log` and `articles` table based on the `slug` in the URL:

```sql
news=> select title, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles where substr = slug order by views desc limit 3;
```

```text
              title               | views
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
(3 rows)

```

##### Planning

I continued by drafting the task in plain English:

- I want to see a table with three columns: the day, the total number of http requests, and the total number of error requests: `select day, http_requests, http_404`
- I want to match the http requests and error requests columns based on the date: `where http_requests.date = http_404.date`

It's not possible to combine both queries into a single `select` statement because `where` can be used only once. For example, the query below returns the three columns I want, but both columns display the error request count, because the entire statement is being filtered `where status = '404 NOT FOUND'`:

```sql
select date_trunc('day', time) as date, count(*) as http_requests, count(*) as http_404 from log where status = '404 NOT FOUND' group by date order by date desc limit 5;
```

```text
          date          | http_requests | http_404
------------------------+---------------+----------
 2016-07-31 00:00:00+00 |           329 |      329
 2016-07-30 00:00:00+00 |           397 |      397
 2016-07-29 00:00:00+00 |           382 |      382
 2016-07-28 00:00:00+00 |           393 |      393
 2016-07-27 00:00:00+00 |           367 |      367
(5 rows)
```

##### Execution

This task will require subqueries.

I had to repeatedly iterate at this step for about 3 hours. It wasn't too difficult to split the task out into subqueries, but I was throwing errors regarding the aggregation, like `ERROR: column "log.time" must appear in the GROUP BY clause or be used in an aggregate function`.
The two keys were:

1. Establishing the proper join condition `where requests.date = errors.date`
2. Making sure I specified the correct names (like `errors.date` instead of `http_404.date`).

Successful query:

```sql
select requests.date, http_requests, http_404 from
(select date_trunc('day', time) as date, count(*) as http_requests from log group by date) as requests,
(select date_trunc('day', time) as date, count(*) as http_404 from log where status = '404 NOT FOUND' group by date) as errors
where requests.date = errors.date
order by requests.date desc;
```

```text
          date          | http_requests | http_404
------------------------+---------------+----------
 2016-07-31 00:00:00+00 |         45845 |      329
 2016-07-30 00:00:00+00 |         55073 |      397
 2016-07-29 00:00:00+00 |         54951 |      382
 2016-07-28 00:00:00+00 |         54797 |      393
 2016-07-27 00:00:00+00 |         54489 |      367
 2016-07-26 00:00:00+00 |         54378 |      396
 2016-07-25 00:00:00+00 |         54613 |      391
 2016-07-24 00:00:00+00 |         55100 |      431
 2016-07-23 00:00:00+00 |         54894 |      373
 2016-07-22 00:00:00+00 |         55206 |      406
 2016-07-21 00:00:00+00 |         55241 |      418
 2016-07-20 00:00:00+00 |         54557 |      383
 2016-07-19 00:00:00+00 |         55341 |      433
 2016-07-18 00:00:00+00 |         55589 |      374
 2016-07-17 00:00:00+00 |         55907 |     1265
 2016-07-16 00:00:00+00 |         54498 |      374
 2016-07-15 00:00:00+00 |         54962 |      408
 2016-07-14 00:00:00+00 |         55196 |      383
 2016-07-13 00:00:00+00 |         55180 |      383
 2016-07-12 00:00:00+00 |         54839 |      373
 2016-07-11 00:00:00+00 |         54497 |      403
 2016-07-10 00:00:00+00 |         54489 |      371
 2016-07-09 00:00:00+00 |         55236 |      410
 2016-07-08 00:00:00+00 |         55084 |      418
 2016-07-07 00:00:00+00 |         54740 |      360
 2016-07-06 00:00:00+00 |         54774 |      420
 2016-07-05 00:00:00+00 |         54585 |      423
 2016-07-04 00:00:00+00 |         54903 |      380
 2016-07-03 00:00:00+00 |         54866 |      401
 2016-07-02 00:00:00+00 |         55200 |      389
 2016-07-01 00:00:00+00 |         38705 |      274
(31 rows)
```

**Awesome!**

#### Identify days on which more than one percent of requests were errors

Now I basically need to add in another calculation, probably something like `having http_404 > 0.01 - http_requests`. I tried `having` but it was easier to just add `and` to the `where` restriction instead.

```sql
select requests.date, http_requests, http_404 from
(select date_trunc('day', time) as date, count(*) as http_requests from log group by date) as requests,
(select date_trunc('day', time) as date, count(*) as http_404 from log where status = '404 NOT FOUND' group by date) as errors
where requests.date = errors.date
and errors.http_404 > 0.01 - requests.http_requests
order by requests.date desc;
```

```text
          date          | http_requests | http_404
------------------------+---------------+----------
 2016-07-17 00:00:00+00 |         55907 |     1265
(1 row)
```

**YES!** The query shows one day, July 17, on which more than 1% of queries led to errors.

#### Display the error percentage

I tried going a bit further to show the error percentage as a column.

I figured it would be something like:

```sql
select errors.http_404 / requests.http_requests - 100 as error_percentage
```

It was difficult, because the `http_requests` and `http_404` columns are being created in this query.

Maybe I need another subquery.

This runs and displays the `error_percentage` column, but doesn't correctly calculate the percentage:

```sql
select requests_and_errors.date, http_requests, http_404, (http_404 / http_requests *100) as error_percentage from
  (select requests.date, http_requests, http_404 from
  (select date_trunc('day', time) as date, count(*) as http_requests from log group by date) as requests,
  (select date_trunc('day', time) as date, count(*) as http_404 from log where status = '404 NOT FOUND' group by date) as errors
  where requests.date = errors.date
  order by requests.date desc) as requests_and_errors;
```

I tried nesting the query even further, unsuccessfully:

```sql
select requests_and_errors.date, http_requests, http_404, error_percentage from
  (select http_404 / http_requests - 100 as error_percentage from requests_and_errors) as percentage
    (select requests.date, http_requests, http_404 from
      (select date_trunc('day', time) as date, count(*) as http_requests from log group by date) as requests,
      (select date_trunc('day', time) as date, count(*) as http_404 from log where status = '404 NOT FOUND' group by date) as errors
      where requests.date = errors.date
      order by requests.date desc)
    as requests_and_errors,
group by requests_and_errors.date desc;
```

It gets difficult to keep track of this many subqueries.

Git commit at this point:
"Complete SQL query three up to sticking point"

Instead of subqueries, I tried to calculate the error percentage from information in the original `logs` table:

```sql
select date_trunc('day', time) as date, count(status = '404 NOT FOUND') from log group by date;
```

The `count` returned is just the total number of requests though.

#### Add the third SQL query to the Python code

Eventually, I just decided to calculate the percentage in Python. I already need to format the output anyway, because `psycopg2` does not output plain text SQL tables like `psql`. I found it strange that `psycopg2` doesn't format the Python output like the plain-text tables from PostgreSQL. The whole point of `psycopg2` is to work with `psql`, so why doesn't it return the same output?

I worked on [cleaning up the output](https://stackoverflow.com/questions/10598002/how-do-i-get-tables-in-postgres-using-psycopg2):

```py
    # Fetch all results from the cursor object
    print("Query 1")
    for table in c.fetchall():
        print(table)
    # Close connection
    db.close()
    pass
```

```sh
vagrant@vagrant:/vagrant/logs$ python -c 'import logs; logs.popular_articles(), logs.popular_authors(), logs.errors()'
```

```text
Query 1
('Candidate is jerk, alleges rival', 338647L)
('Bears love berries, alleges bear', 253801L)
('Bad things gone, say good people', 170098L)
Query 2
('Ursula La Multa', Decimal('507594'))
('Rudolf von Treppenwitz', Decimal('423457'))
('Anonymous Contributor', Decimal('170098'))
('Markoff Chaney', Decimal('84557'))
Query 3
(datetime.datetime(2016, 7, 17, 0, 0, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=0, name=None)), 55907L, 1265L)
```

Still not great, especially for query 3.

I was finally able to remove the timestamp from the date by converting it to a string, and slicing for characters 0-10, with `print("Date:", str(table[0])[:10])`. I also improved the output formatting by including a header line.

```py
    # Fetch all results from the cursor object
    print('\n', 'Query 3: Days on which >1% HTTP requests returned 404 errors')
    for table in c.fetchall():
        # Convert datetime to string and slice to retain only the date
        print('Date:', str(table[0])[:10])
        # Calculate error rate
        print('Percent errors:', float(table[2]) / float(table[1]) - 100)
```

Next, I simply changed the Linux command (just by guessing) from `python` to `python3`, to specify. The output was formatted correctly. Maybe my shebang line isn't working, though it's written correctly, or maybe this distribution of Linux ignores the shebang line.

Here's the final Linux command:

```sh
vagrant@vagrant:/vagrant/logs$ python3 -c 'import logs; logs.popular_articles(), logs.popular_authors(), logs.errors()'
```

```text
 Query 1: Most popular three articles
Candidate is jerk, alleges rival 338647
Bears love berries, alleges bear 253801
Bad things gone, say good people 170098

 Query 2: Most popular authors
Ursula La Multa 507594
Rudolf von Treppenwitz 423457
Anonymous Contributor 170098
Markoff Chaney 84557

 Query 3: Days on which >1% HTTP requests returned 404 errors
Date: 2016-07-17
Percent errors: 2.2626862468027262
```

**Done!**

[(Back to TOC)](#table-of-contents)
