# Logs analysis project methods and notes

**Udacity Full Stack Web Developer Nanodegree program**

Part 03. Backend

Project 01. Logs analysis

Brendon Smith

br3ndonland

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Setup](#setup)
- [Starting Python in *logs.py*](#starting-python-in-logspy)
- [Starting the virtual machine and exploring the data](#starting-the-virtual-machine-and-exploring-the-data)
- [SQL queries](#sql-queries)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Setup

* I read through the Udacity documentation and rubric (see *logs-udacity.md*)
* Files:
	- *logs-methods.md* (this file) to log my progress
	- *logs-udacity.md* to store the project information and rubric from Udacity
	- *logs.py* for the main program code
	- *output.txt* to store sample output from the program
	- *README.md* for a concise description of the project
* I kept vagrant and the database in a separate directory because of the large size of the database file.


## Starting Python in *logs.py*
[(back to top)](#top)

* Shebang: when reading through the "Functionality" section of the rubric, I saw that it recommended "a correct shebang line to indicate the Python version." I actually hadn't written a shebang line before, but looked it up on [Stack Overflow](https://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script) and drafted one.
* I created an outline in the python file *logs.py* with the steps I would be working on. Here's the initial outline:
	```python
	#!/usr/bin/env python3

	# Udacity database logs analysis project

	# 1. Most popular three articles

	# 2. Most popular authors

	# 3. Days on which >1% of HTTP requests led to errors

	```
* To function or not to function: Next, I decided to write each of the three queries as a Python function. I began building the functions based on the resources from *Lesson 03. Python DB-API*:
	- *forumdb.py*
	- *3.3. Writing Code with DB API*
	- *3.16. Reference — Python DB-API*
	```python
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
* Git commit at this point: "Initialize files and code outline"


## Starting the virtual machine and exploring the data
[(back to top)](#top)

* I already had vagrant installed from the instructions in *Lesson 2.17. Installing the Virtual Machine*.
* I unzipped *newsdata.sql* and moved it into the *vagrant* directory.
* I changed into the vagrant directory and started up vagrant (only necessary when restarting computer):
	```bash
	$ vagrant up
	```
* I then logged in to Ubuntu as before
	```bash
	$ vagrant ssh
	```
* I connected to the database and loaded the data with PostgreSQL:
	```bash
	$ cd /vagrant
	/vagrant$ psql -d news -f newsdata.sql
	```
	As explained in the Udacity documentation for the project (see *logs-udacity.md*):
	> Here's what this command does:
	> 
	> * `psql` — the PostgreSQL command line program
	> * `-d news` — connect to the database named news which has been set up for you
	> * `-f newsdata.sql` — run the SQL statements in the file newsdata.sql
	> 
	> Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
	
	This only needs to be done once. When reconnecting, after `vagrant up` and `vagrant ssh`, simply use 
	```bash
	$ cd /vagrant
	/vagrant$ psql -d news
	```
	and to log out (the opposite of `vagrant ssh`), just type ctrl+d or
	```bash
	$ logout
	```
* I then began exploring the data by running commands in the vagrant Linux terminal. This helped me understand how to build the SQL queries.
* I started by viewing the tables:
	```
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
* Next, I viewed the columns of each table.
	- `\d articles`
	- `\d authors`
	- `\d log`
* I then broke it down further and started looking at the content of the columns.
	- `select author from articles limit 10;` The `author` column in the `articles` table is a foreign key, "articles_author_fkey" that references the author `id` in the `authors` table.
	- `select slug from articles;` shows there are only 8 articles.
	- `select path from log limit 10;` `path` looks like `slug` from the `articles` table, but it is repeated every time the article is accessed. We need to group and count the paths to find out how many times each article was accessed.
* I tried out some of the SQL queries from the Udacity project instructions (see *logs-udacity.md*), like
	```sql
	select title, name
	from articles, authors
	where articles.author = authors.id;
	```


## SQL queries
[(back to top)](#top)

Helpful reference info when building the SQL queries:

* *2.18. Reference — Elements of SQL*
* *3.16. Reference — Python DB-API*
* *4.15. Reference — Deeper into SQL*

I broke each query down, as recommended in the Udacity instructions, and repeatedly iterated until I got it.


### 1. What are the most popular three articles of all time?

#### Use the `log` table to count hits by `path`

I started by figuring out how to aggregate `path` and count hits in the `log` table. I based my first successful query on *1.11. Quiz: Count All the Species*.

```sql
news=> select path, count(*) as num from log group by path order by num desc;
```

This shows a list of 212 rows.

```
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

```
            path             |  num
-----------------------------+--------
 /article/candidate-is-jerk  | 338647
 /article/bears-love-berries | 253801
 /article/bad-things-gone    | 170098
(3 rows)
```


#### Join the log table with the articles table

Now to merge the log with the articles table. 

```sql
news=> select id, slug, title from articles;
```

```
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

```
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

```
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

```
       substr       |  num
--------------------+--------
 candidate-is-jerk  | 338647
 bears-love-berries | 253801
 bad-things-gone    | 170098
(3 rows)
```


#### Combine the hit count and join into a single SQL statement

Now time to write the join! I started off just drafting it in plain English.

I want to join the `log` table with the `articles` table, where the `substr` from `log` matches the `slug` from `articles`, and show the `title` column from `articles` with the `num` count column created by the aggregation in `log`.

Wow, alright. Let's break that down:

* where the `substr` from `log` matches the `slug` from `articles`:
	```sql
	where log.substr = articles.slug
	```
* show the `title` column from `articles` with the `num` count column created by the aggregation in `log`:
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

```
  num
--------
 338647
 253801
 170098
(3 rows)
```

Next, I continued iterating to get my first successful join of `log` and `articles`:

```sql
news=> select title, num from (select substr(path, 10), count(*) as num from log where path !='/' group by path order by num desc limit 3) as hits, articles limit 3;
```

```
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

```
              title               | views
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
(3 rows)

```

This also showed me that the order of columns in the `SELECT` statement doesn't need to match the order the tables are mentioned in the `FROM` statement.


#### Add the first SQL query to the Python code

I plugged this into the Python code in *logs.py* to test it out. I reformatted the SQL query for Python with help from the [psycopg2](http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries) docs:

```python
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

In order to run the Python code within Vagrant, I created a */vagrant/logs* directory and copied in the *logs.py* file.

I then formatted the Linux command line argument to call the function, with a little help from [Stack Overflow](https://stackoverflow.com/questions/3987041/python-run-function-from-the-command-line#3987113) via a [DuckDuckGo](https://duckduckgo.com) search for "run python functions from command line":

```bash
vagrant@vagrant:/vagrant/logs$ python -c 'import logs; print(logs.popular_articles())'
```

```
[('Candidate is jerk, alleges rival', 338647L), ('Bears love berries, alleges bear', 253801L), ('Bad things gone, say good people', 170098L)]
```

I will need to reformat the output into a plain-text table like PostgreSQL. I tried a few different things. There is a `PrettyTable` module, but the Python distribution with Vagrant doesn't have it. I'll get back to this after finishing the second and third queries.


### 2. Who are the most popular article authors of all time?

The second query is like an extension of the first, with an additional join to the authors table, and an aggregation to group the articles by author.


#### Join the three tables

I started off viewing the `name` and `id` columns from the `authors` table, so I knew what to look for:

```sql
news=> select name, id from authors;
```

```
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

```
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

select count(views) as authorviews from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles where substr = slug group by author order by views desc;

select title, author, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles where substr = slug order by author desc;

Now to join the three tables, displaying information from all three to verify:

```sql
select name, author, title, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles, authors where substr = slug and author = authors.id order by views desc;
```

```
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

*Aggregation aggravation*

This step was more difficult. I tried creating views, but wasn't able to create a view and select from that view in the same SQL query (remember each of the three queries has to be a self-contained query).

I started moving in the right direction by nesting the entire subquery from the "Join the three tables" step above inside another query:

```sql
select name, views from 
(select name, author, title, views from (select substr(path, 10), count(*) as views from log where path !='/' group by path) as hits, articles, authors where substr = slug and author = authors.id order by views desc) as threetables;
```

```
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

* `sum(views) as total_views` at the beginning, before the long nested subquery
* `group by name order by total_views desc`, after the long nested subquery, to tell `psql` how to compute the sum.

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

```
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

```python
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

```bash
vagrant@vagrant:/vagrant/logs$ python -c 'import logs; print(logs.popular_articles(), logs.popular_authors())'
```

```
([('Candidate is jerk, alleges rival', 338647L), ('Bears love berries, alleges bear', 253801L), ('Bad things gone, say good people', 170098L)], [('Ursula La Multa', Decimal('507594')), ('Rudolf von Treppenwitz', Decimal('423457')), ('Anonymous Contributor', Decimal('170098')), ('Markoff Chaney', Decimal('84557'))])
```

Git commit at this point: 

"Complete queries one and two"


### 3. On which days did more than 1% of requests lead to errors?

I will need to sum the total number of HTTP requests, and divide by the number of HTTP error codes like 404.


[(back to top)](#top)
