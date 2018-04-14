# README

<a href="https://www.udacity.com/">
    <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a>

Udacity Full Stack Web Developer Nanodegree program

Project 3. SQL database logs analysis

Brendon Smith

br3ndonland

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Project description](#project-description)
- [Repository contents](#repository-contents)
  - [Required files](#required-files)
  - [Other files](#other-files)
- [Instructions](#instructions)
  - [Install virtual machine](#install-virtual-machine)
  - [Add application files](#add-application-files)
  - [Run virtual machine](#run-virtual-machine)
  - [Run application](#run-application)
- [A tale of three queries](#a-tale-of-three-queries)
  - [1. Most popular articles](#1-most-popular-articles)
  - [2. Most popular authors](#2-most-popular-authors)
  - [3. HTTP request error rate](#3-http-request-error-rate)
- [Running the queries with the Python program](#running-the-queries-with-the-python-program)

## Project description

Databases can contain trillions of rows and columns, something that spreadsheet programs like Google Sheets and Microsoft Excel simply can't handle. Instead, Structured Query Language (SQL) is used to query (ask) the computer to retrieve information from binary databases, and return it to the user in plain text.

I completed this project as part of the Udacity Full Stack Web Developer Nanodegree program. Students were asked to write SQL queries to extract information from a database of news articles with over a million rows. The SQL queries contain advanced joins, selection, and calculation features. Another general-purpose computing language called Python was used to group and control the queries.

[(Back to TOC)](#table-of-contents)

## Repository contents

### Required files

- *[logs.py](logs.py)* - main program code
- *[logs-output.txt](logs-output.txt)* - example code output
- *[README.md](README.md)* - this file, a concise description of the project

### Other files

- *[logs-methods.md](logs-methods.md)* - computational narrative explaining I wrote the code for the project
- *[logs-udacity.md](logs-udacity.md)* - project description and rubric from Udacity

[(Back to TOC)](#table-of-contents)

## Instructions

### Install virtual machine

A virtual machine can be used to run the code from an operating system with a defined configuration. The virtual machine has all the dependencies needed to run the application.

I wrote the program in a Linux virtual machine with the following components:

- Oracle [VirtualBox](https://www.virtualbox.org/wiki/Downloads) Version 5.2.6 r120293 (Qt5.6.3)
  - Software that runs special containers called virtual machines, like Vagrant.
- [Vagrant](https://www.vagrantup.com/) 2.0.1 with Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-75-generic i686)
  - Software that provides the Linux operating system in a defined configuration, allowing it to run identically across many personal computers. Linux can then be run as a virtual machine with VirtualBox.
- [Udacity Virtual Machine configuration](https://github.com/udacity/fullstack-nanodegree-vm)
  - Repository from Udacity that configures Vagrant.
  - My personal fork of the configuration is also available on [GitHub](https://github.com/br3ndonland/fullstack-nanodegree-vm) if needed.

### Add application files

- Clone the [application repository](https://github.com/br3ndonland/udacity-fsnd-p3-sql) into the *vagrant/* virtual machine directory.
- Download the [news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and save in the *vagrant/* virtual machine directory (not directly within the cloned repository).

### Run virtual machine

- Change into the vagrant directory on the command line (wherever you have it stored):

  ```bash
  $ cd <path>/fullstack-nanodegree-vm/vagrant
  ```

- Start Vagrant (only necessary once per terminal session):

  ```bash
  $ vagrant up
  ```

- Log in to Ubuntu:

  ```bash
  $ vagrant ssh
  ```

### Run application

- After logging into the virtual machine, change into the application directory:

  ```bash
  $ vagrant@vagrant:~$ cd /vagrant/udacity-fsnd-p3-sql
  ```

- Change into the Vagrant directory:

  ```bash
  vagrant@vagrant:~$ cd /vagrant
  ```

- Connect to the database with PostgreSQL:
  - The first time:

    ```bash
    vagrant@vagrant:/vagrant$ psql -d news -f newsdata.sql
    ```

  - Subsequent logins:

    ```bash
    vagrant@vagrant:/vagrant$ psql -d news
    ```

- Enter SQL queries at the `=>` prompt. The queries can be more efficiently run from the Python program, as described [below](#running-the-queries-with-the-python-program).

  ```text
  psql (9.5.10)
  Type "help" for help.

  news=>
  ```

- To exit the `psql` prompt, simply type `\q` and hit enter:

  ```bash
  news=> \q
  vagrant@vagrant:/vagrant$
  ```

[(Back to TOC)](#table-of-contents)

## A tale of three queries

I implemented three SQL queries:

### 1. Most popular articles

*What are the most popular three articles of all time?*

Returns a sorted list of the three most highly accessed articles, with the top article first.

Query:

```sql
select title, num from
    (select substr(path, 10), count(*) as num from log
    where path !='/' group by path)
as hits, articles where substr = slug order by num desc limit 3;
```

Linux output:

```text
              title               | views
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
(3 rows)
```

### 2. Most popular authors

*Who are the most popular article authors of all time?*

Returns a sorted list of the most popular article authors, with the most popular author at the top.

Query:

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

Linux output:

```text
          name          | total_views
------------------------+-------------
 Ursula La Multa        |      507594
 Rudolf von Treppenwitz |      423457
 Anonymous Contributor  |      170098
 Markoff Chaney         |       84557
(4 rows)
```

### 3. HTTP request error rate

*On which days did more than 1% of requests lead to errors?*

Returns a list of days on which >1% of HTTP requests resulted in HTTP error codes.

Query:

```sql
select errdate, http_requests, http_404,
100.0 - http_404 / http_requests as errpct from
    (select date_trunc('day', time) as reqdate, count(*)
    as http_requests from log group by reqdate)
    as requests,
    (select date_trunc('day', time) as errdate, count(*)
    as http_404 from log where status = '404 NOT FOUND'
    group by errdate)
    as errors
where reqdate = errdate
and errors.http_404 > 0.01 - requests.http_requests
order by errdate desc;
```

Linux output:

```text
        errdate         | http_requests | http_404 |       errpct
------------------------+---------------+----------+--------------------
 2016-07-17 00:00:00+00 |         55907 |     1265 | 2.2626862468027260
(1 row)
```

[(Back to TOC)](#table-of-contents)

## Running the queries with the Python program

Each query is included in a Python function in *[logs.py](logs.py)*.

To run the queries contained within the Python program from the command line:

Change into the directory containing the Python file:

```bash
vagrant@vagrant:/vagrant$ cd logs
```

Run the Python program by directly invoking Python:

```bash
vagrant@vagrant:/vagrant/logs$ python3 logs.py
```

Python will return the results of the three queries in plain text output in the Linux terminal, with Pythonic formatting modified from the original `psql` table format:

```text
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

[(Back to TOC)](#table-of-contents)