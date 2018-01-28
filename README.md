# Logs analysis project README

<p align="left">
    <a href="https://www.udacity.com/">
        <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
    </a>
</p>

**Udacity Full Stack Web Developer Nanodegree program**

Part 03. Backend

Project 01. Logs analysis

Brendon Smith

br3ndonland

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Project description](#project-description)
- [Directory contents](#directory-contents)
- [Development environment](#development-environment)
- [Running the program: A tale of three queries](#running-the-program-a-tale-of-three-queries)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Project description
[(back to top)](#top)

When working with large databases, it is most efficient to store them in binary format (zeros and ones). Databases can contain trillions of rows and columns, something that spreadsheet programs like Google Sheets and Microsoft Excel simply can't handle. Instead, Structured Query Language (SQL) is used to query (ask) the computer to retrieve information about the database, and display it to the user in plain text.

I completed this project as part of the Udacity Full Stack Web Developer Nanodegree program. Students were asked to write SQL queries to extract information from a database of news articles. Another general-purpose computing language called Python was used to group and control the queries.


## Directory contents

### Required files

* *logs.py* - main program code
* *logs-output.txt* - example code output
* *README.md* - this file, a concise description of the project


### Other files

* *logs-methods.md* - detailed step-by-step explanation of how I wrote the code for the project
* *logs-udacity.md* - project description and rubric from Udacity


## Development environment
[(back to top)](#top)

I wrote the program in a Linux virtual machine with the following components:

* *Oracle [VirtualBox](https://www.virtualbox.org/wiki/Downloads) Version 5.2.6 r120293 (Qt5.6.3)* - software that runs special containers called  virtual machines, like Vagrant.
* *[Vagrant](https://www.vagrantup.com/) 2.0.1 with Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-75-generic i686)* -  software that provides the Linux operating system in a precisely defined configuration, allowing it to run identically across many personal computers. Linux can then be run as a virtual machine with VirtualBox.
* *[Udacity Virtual Machine configuration specs](https://github.com/udacity/fullstack-nanodegree-vm)* - repository from Udacity that configures Vagrant. I installed and ran Vagrant from within the directory *fullstack-nanodegree-vm/vagrant*.
* *PostgreSQL 9.5.10* - We used an implementation of SQL called PostgreSQL, included with the Linux distribution, to query the database.
* *psycopg2* - connects SQL databases with Python code
* *Python 3* - general-purpose and flexible computing language used to group and control the queries.

Further details can be found in the "Prepare the software and data" section of *logs-udacity.md*.


## Running the program: A tale of three queries
[(back to top)](#top)

I had to implement three SQL queries. Each query is included in a Python function in *logs.py*.


### 1. What are the most popular three articles of all time?


### 2. Who are the most popular article authors of all time?


### 3. On which days did more than 1% of requests lead to errors?

### Run the queries

On the Linux command line, type:
```bash
cd <this directory>
python logs.py
```

Linux will return the results of the three queries in plain text.