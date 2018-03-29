# SQL database logs analysis project README

<a href="https://www.udacity.com/">
    <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a>

**Udacity Full Stack Web Developer Nanodegree program**

Project 4. SQL database logs analysis

Brendon Smith

br3ndonland

## TOC
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Project description](#project-description)
- [Directory contents](#directory-contents)
- [Development environment](#development-environment)
- [Linux and PostgreSQL](#linux-and-postgresql)
- [A tale of three queries](#a-tale-of-three-queries)
- [Running the queries with the Python program](#running-the-queries-with-the-python-program)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Project description
[(Back to TOC)](#toc)

Databases can contain trillions of rows and columns, something that spreadsheet programs like Google Sheets and Microsoft Excel simply can't handle. Instead, Structured Query Language (SQL) is used to query (ask) the computer to retrieve information from binary databases, and return it to the user in plain text.

I completed this project as part of the Udacity Full Stack Web Developer Nanodegree program. Students were asked to write SQL queries to extract information from a database of news articles. Another general-purpose computing language called Python was used to group and control the queries.


## Directory contents
[(Back to TOC)](#toc)

### Required files

* *logs.py* - main program code
* *logs-output.txt* - example code output
* *README.md* - this file, a concise description of the project


### Other files

* *logs-methods.md* - detailed step-by-step explanation of how I wrote the code for the project
* *logs-udacity.md* - project description and rubric from Udacity


## Development environment
[(Back to TOC)](#toc)

I wrote the program in a Linux virtual machine with the following components:

* Oracle [VirtualBox](https://www.virtualbox.org/wiki/Downloads) Version 5.2.6 r120293 (Qt5.6.3)
    - Software that runs special containers called virtual machines, like Vagrant.
* [Vagrant](https://www.vagrantup.com/) 2.0.1 with Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-75-generic i686)
    - Software that provides the Linux operating system in a defined configuration, allowing it to run identically across many personal computers. Linux can then be run as a virtual machine with VirtualBox.
* [Udacity Virtual Machine configuration](https://github.com/udacity/fullstack-nanodegree-vm)
    - Repository from Udacity that configures Vagrant.
	- I installed and ran Vagrant from within the directory *fullstack-nanodegree-vm/vagrant*.
	- I also created a directory at *vagrant/logs*, and copied in *logs.py* after it was finished to run it.
* *PostgreSQL 9.5.10* - We used an implementation of SQL called PostgreSQL, included with the Linux distribution, to query the database.
* *psycopg2* - Python module that connects PostgreSQL databases with Python code.
* *Python 3* - Flexible and powerful computing language used to group and control the queries.
* *[News database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)* - We downloaded the database as a zip archive, unzipped it, and moved it into the *fullstack-nanodegree-vm/vagrant* directory.

Further details can be found in the "Prepare the software and data" section of *logs-udacity.md*.


## Linux and PostgreSQL
[(Back to TOC)](#toc)

On the Linux command line:

Change into the Vagrant directory (wherever you have it stored):

```bash
$ cd <path>/fullstack-nanodegree-vm/vagrant
```

Start Vagrant (only necessary after computer restart):

```bash
$ vagrant up
```

Log in to Ubuntu:

```bash
$ vagrant ssh
```

Change into the Vagrant directory:

```bash
vagrant@vagrant:~$ cd /vagrant
```

Connect to the database with PostgreSQL:

The first time:

```bash
vagrant@vagrant:/vagrant$ psql -d news -f newsdata.sql
```

Subsequent logins:

```bash
vagrant@vagrant:/vagrant$ psql -d news
```

```
psql (9.5.10)
Type "help" for help.

news=>
```

The queries can be entered directly at the `news=>` prompt.

To exit the `psql` prompt, simply type `\q` and hit enter:

```bash
news=> \q
vagrant@vagrant:/vagrant$
```


## A tale of three queries
[(Back to TOC)](#toc)

I implemented three SQL queries:


### 1. What are the most popular three articles of all time?

Returns a sorted list of the three most highly accessed articles, with the top article first.

```sql
select title, num from
    (select substr(path, 10), count(*) as num from log
    where path !='/' group by path)
as hits, articles where substr = slug order by num desc limit 3;
```

```
              title               | views
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
(3 rows)
```


### 2. Who are the most popular article authors of all time?

Returns a sorted list of the most popular article authors, with the most popular author at the top.

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


### 3. On which days did more than 1% of requests lead to errors?

Returns a list of days on which >1% of HTTP requests resulted in HTTP error codes.

```sql
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
```

```
        errdate         | http_requests | http_404 |       errpct
------------------------+---------------+----------+--------------------
 2016-07-17 00:00:00+00 |         55907 |     1265 | 2.2626862468027260
(1 row)
```


## Running the queries with the Python program
[(Back to TOC)](#toc)

Each query is included in a Python function in *logs.py*.

To run the queries contained within the Python program from the command line:

Change into the directory containing the Python file:

```bash
vagrant@vagrant:/vagrant$ cd logs
```

Run the Python program by directly invoking Python:

```bash
vagrant@vagrant:/vagrant/logs$ python3 logs.py
```

Python will return the results of the three queries in plain text, with Pythonic formatting modified from the original `psql` table format:

```
 Query 1: Most popular three articles
    Candidate is jerk, alleges rival  --  338647 views
    Bears love berries, alleges bear  --  253801 views
    Bad things gone, say good people  --  170098 views

 Query 2: Most popular authors
    Ursula La Multa  --  507594 views
    Rudolf von Treppenwitz  --  423457 views
    Anonymous Contributor  --  170098 views
    Markoff Chaney  --  84557 views

 Query 3: Days on which >1% HTTP requests returned 404 errors
    July 17, 2016  --  2.26% errors
```

[(Back to TOC)](#toc)