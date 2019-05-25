# SQL database logs analysis

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo">
</a>

[Udacity Full Stack Developer Nanodegree program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

Brendon Smith ([br3ndonland](https://github.com/br3ndonland))

[![code license](https://img.shields.io/badge/code%20license-MIT-blue.svg?longCache=true&style=for-the-badge)](https://choosealicense.com/licenses/mit/)

## Table of Contents <!-- omit in toc -->

- [Project description](#project-description)
- [Repository contents](#repository-contents)
  - [Required files](#required-files)
  - [Other files](#other-files)
- [A tale of three queries](#a-tale-of-three-queries)
  - [1. Most popular articles](#1-most-popular-articles)
  - [2. Most popular authors](#2-most-popular-authors)
  - [3. HTTP request error rate](#3-http-request-error-rate)
- [Instructions](#instructions)
  - [Major dependencies](#major-dependencies)
  - [Pipenv virtual environment](#pipenv-virtual-environment)
  - [Docker](#docker)
  - [Vagrant virtual machine](#vagrant-virtual-machine)
  - [Add files](#add-files)
  - [Run queries](#run-queries)

## Project description

Databases can contain trillions of rows and columns, something that spreadsheet programs like Google Sheets and Microsoft Excel simply can't handle. Structured Query Language (SQL) is used to query (ask) the computer to retrieve information from databases.

I completed this project as part of the Udacity Full Stack Developer Nanodegree program. Students were asked to write SQL queries to extract information from a database of news articles with over a million rows. The SQL queries contain advanced joins, selection, and calculation features. Another general-purpose computing language called Python was used to group and control the queries.

[(Back to TOC)](#table-of-contents)

## Repository contents

### Required files

- _[logs.py](logs.py)_ - main program code
- _[logs-output.txt](logs-output.txt)_ - example code output
- _[README.md](README.md)_ - this file, a concise description of the project

### Other files

- _[logs-methods.md](info/logs-methods.md)_ - computational narrative explaining how I wrote the code for the project
- _[logs-review.md](info/logs-review.md)_ - Udacity code review
- _[logs-udacity.md](info/logs-udacity.md)_ - project description, installation instructions, and rubric from Udacity

[(Back to TOC)](#table-of-contents)

## A tale of three queries

I implemented three SQL queries:

### 1. Most popular articles

_What are the most popular three articles of all time?_

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

_Who are the most popular article authors of all time?_

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

_On which days did more than 1% of requests lead to errors?_

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

## Instructions

The application can be run by setting up either a virtual environment or a virtual machine. Instructions for each option are provided below. More comprehensive instructions are available in [logs-udacity.md](info/logs-udacity.md).

### Major dependencies

- Python 3
- `psycopg2`
- [PostgreSQL](https://www.postgresql.org/)

### Pipenv virtual environment

- **[Pipenv](https://pipenv.readthedocs.io/en/latest/)** was used to manage the development virtual environment for this project.

  - Install Pipenv with a system package manager like [Homebrew](https://brew.sh/), or with the Python package manager `pip`.
  - Use Pipenv to install the virtual environment from the _Pipfile_ with `pipenv install --dev`.

    - The `--dev` flag was used to accommodate the Black autoformatter, which is considered a pre-release package (see [code style](#python-code-style) below).
    - When generating the initial _Pipfile_ containing the Black dev package, the `--pre` flag added a line to the _Pipfile_ to allow pre-release packages. (TOML format):

      ```toml
      [pipenv]
      allow_prereleases = true
      ```

    - Further information can be found in the [Pipenv docs](https://pipenv.readthedocs.io/en/latest/basics/#specifying-versions-of-a-package).

  - Activate the virtual environment with `pipenv shell`.

- VSCode can be configured to recognize the Pipenv virtual environment. See [Using Python environments in VS Code](https://code.visualstudio.com/docs/python/environments).
  - _Command Palette -> Python: Select Interpreter_. Select virtual environment.
  - _Command Palette -> Python: Create Terminal_. Creates a terminal and automatically activates the virtual environment. If the virtual environment is set as the interpreter for the workspace, new terminal windows will automatically start in the virtual environment.

Proceed to [run queries](#run-queries).

### Docker

#### Docker background

- **[Docker](https://www.docker.com/)** is a technology for running lightweight virtual machines called **containers**.
  - An **image** is the executable set of files read by Docker.
  - A **container** is a running image.
  - The **[Dockerfile](https://docs.docker.com/engine/reference/builder/)** tells Docker how to build the container.
- VSCode has built-in Docker features. See [Working with Docker in VSCode](https://code.visualstudio.com/docs/azure/docker) and the [VSCode tutorial on deploying Python with Docker](https://code.visualstudio.com/docs/python/tutorial-deploy-containers).
- To install Docker tools locally:
  - Ubuntu Linux: follow the [instructions for Ubuntu Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/), making sure to follow the [postinstallation steps](https://docs.docker.com/install/linux/linux-postinstall/) to activate the Docker daemon.
  - macOS and Windows: install [Docker Desktop](https://www.docker.com/products/docker-desktop) (available via [Homebrew](https://brew.sh) with `brew cask install docker`).
- To build this Docker image and run the container:

  ```sh
  cd path/to/repo
  docker build . -t graphql-python-starter:latest
  docker run -d -p 80:1040 graphql-python-starter:latest
  ```

  - `-t` web tells Docker to name the image `graphql-python-starter`. Adding `.` builds from the current directory.
  - `-d` runs the container in detached mode. Docker will display the container hash and return the terminal prompt.
  - `-p 80:1040` maps the http port 80 from your local machine to port 1040 in the container.
  - A tag can be specified with `name:tag`, otherwise, the tag `latest` will be used.

- <details><summary>Expand this details element for more <a href="https://docs.docker.com/engine/reference/commandline/cli/">useful Docker commands</a>.</summary>

  ```sh
  # List images
  docker image ls

  # List containers
  docker container ls

  # Inspect a container (web in this example) and return the IP Address
  docker inspect web | grep IPAddress

  # Stop a container
  docker container stop # container hash

  # Remove a downloaded image
  docker image rm # image hash or name

  # Remove a container
  docker container rm # container hash

  # Prune stopped containers (wipes them and resets their state)
  docker container prune

  # Connect to running container (sort of like SSH)
  docker ps # get ID/hash of container you want to connect to
  docker exec -it [ID] /bin/bash
  # Or, connect as root:
  docker exec -u 0 -it [ID] /bin/bash

  # Copy file to/from container:
  docker cp [container_name]:/path/to/file destination.file
  ```

  </summary>

#### Pipenv and Docker

- There are a few [adjustments](https://stackoverflow.com/a/49705601) needed to enable Pipenv and Docker to work together.
- Pipenv must first be installed with `pip`.
- Python dependencies are then installed from _Pipfile.lock_.

  - Docker containers don't need virtual environments, so the `--system` flag is used to install packages into the container's global Python installation. Thus, it is not necessary to enter the virtual environment with `pipenv shell` before starting the application.
  - The `--deploy` flag causes the build to fail if the _Pipfile.lock_ is out of date.
  - The `--ignore-pipfile` flag tells Pipenv to use the _Pipfile.lock_ for installation instead of the _Pipfile_.

  ```dockerfile
  # Pull an image: alpine images are tightly controlled and small in size
  FROM python:3.7-alpine
  LABEL app=graphql-python-starter
  WORKDIR /app
  # Copy the directory to /app in the container
  COPY . /app
  # Install Pipenv
  RUN python -m pip install pipenv
  # Install packages from Pipfile.lock, configured for Docker deployments
  RUN pipenv install --system --deploy --ignore-pipfile
  # Run the application
  CMD ["python", "app.py"]
  ```

### Vagrant virtual machine

A virtual machine can be used to run the code from an operating system with a defined configuration. The virtual machine has all the dependencies needed to run the application.

#### Configure virtual machine

I wrote the program in a Linux virtual machine with the following components:

- Oracle [VirtualBox](https://www.virtualbox.org) Version 5.2.10 r122088 (Qt5.6.3)
  - Software that runs special containers called virtual machines, like Vagrant.
  - Updates to the program need to be [downloaded directly](https://www.virtualbox.org/wiki/Downloads).
- [Vagrant](https://www.vagrantup.com/) 2.0.4 with Ubuntu 16.04.4 LTS (GNU/Linux 4.4.0-75-generic x86_64)
  - Software that provides the Linux operating system in a defined configuration, allowing it to run identically across many personal computers. Linux can then be run as a virtual machine with VirtualBox.
  - Updates to the program need to be [downloaded directly](https://www.vagrantup.com/downloads.html).
- [Udacity virtual machine configuration](https://github.com/udacity/fullstack-nanodegree-vm)
  - Repository from Udacity that configures Vagrant.
  - Some of the necessary Python modules in the Udacity virtual machine configuration are only included for Python 2, and not Python 3. If needed, install the modules with `pip`.

#### Run virtual machine

- Clone the application repository into the _vagrant/_ virtual machine directory.
- Start the virtual machine and log into vagrant:

  - Change into the vagrant directory on the command line (wherever you have it stored):

    ```sh
    cd <path>/fullstack-nanodegree-vm/vagrant
    ```

  - Start Vagrant (only necessary once per terminal session):

    ```sh
    vagrant up
    ```

  - Log in to Ubuntu:

    ```sh
    vagrant ssh
    ```

  - After logging into the virtual machine, change into the application directory:

    ```sh
    vagrant@vagrant:~$ cd /vagrant/udacity-fsnd-p3-sql
    ```

### Add files

- Clone the [application repository](https://github.com/br3ndonland/udacity-fsnd-p3-sql) into the directory.
- Create a _data/_ directory within the application directory.
- Download the [news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and save in the _data/_ directory.

### Run queries

The queries can be run directly by `psql`, or from within the Python program.

#### Run queries from psql

- Connect to the database with PostgreSQL:

  - The first time:

    ```sh
    vagrant@vagrant:/vagrant$ psql -d news -f data/newsdata.sql
    ```

- Activate PostgreSQL:

  ```sh
  vagrant@vagrant:/vagrant$ psql -d news
  ```

- Enter SQL queries at the `=>` prompt.

  ```text
  psql (9.5.10)
  Type "help" for help.

  news=>
  ```

- To exit the `psql` prompt, simply type `\q` and hit enter:

  ```sh
  news=> \q
  vagrant@vagrant:/vagrant$
  ```

[(Back to TOC)](#table-of-contents)

#### Run queries with the Python program

Each query is included in a Python function in _[logs.py](logs.py)_.

To run the queries contained within the Python program from the command line:

Change into the directory containing the Python file:

```sh
vagrant@vagrant:/vagrant$ cd logs
```

Run the Python program by directly invoking Python:

```sh
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
