# Logs analysis project documentation

<p align="left">
    <a href="https://www.udacity.com/">
        <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
    </a>
</p>

**Udacity Full Stack Web Developer Nanodegree program**

Part 03. Backend

Project 01

Brendon Smith

br3ndonland

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Readme](#readme)
- [Project description](#project-description)
- [Review](#review)
- [Prepare the software and data](#prepare-the-software-and-data)
- [Your assignment: Build it!](#your-assignment-build-it)
- [Frequently asked questions](#frequently-asked-questions)
- [Logs Analysis Rubric](#logs-analysis-rubric)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Readme

This is the documentation for the project from Udacity. I converted it from HTML to Markdown by viewing the website HTML with Developer Tools, copying the HTML, pasting the HTML into [Turndown](https://domchristie.github.io/turndown/) for conversion from HTML to Markdown, then copying and pasting into this file.


## Project description
[(back to top)](#top)

You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.


### Why this project?

In this project, you will stretch your SQL database skills. You will get practice interacting with a live database both from the command line and from your code. You will explore a large database with over a million rows. And you will build and refine complex queries and use them to draw business conclusions from data.


#### Report generation

Building an informative summary from logs is a real task that comes up very often in software engineering. For instance, at Udacity we collect logs to help us measure student progress and the success of our courses. The reporting tools we use to analyze those logs involve hundreds of lines of SQL.


#### Database as shared resource

In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

This shows one of the valuable roles of a database server in a real-world application: it's a point where different pieces of software (a web app and a reporting tool, for instance) can share data.

Just one of many queries Udacity uses for logs analysis:

```sql
SELECT event_day AS period,
	SUM(current_paid_students) AS "Paid Students",
	SUM(current_trial_students) AS "Free Students"
FROM analytics_tables.paid_enrollment
WHERE ("course_key" = {NANODEGREE})
AND current_trial_students > 0
GROUP BY period
ORDER BY period ASC;
```


## Review
[(back to top)](#top)

Completing this project will exercise your database skills. Here are some portions of the Relational Databases course that you might want to review:

* [Joining tables](https://classroom.udacity.com/courses/ud197/lessons/3415228765/concepts/33932188550923)
* [The `select` ...`where` statement](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/33885287000923)
* [Select clauses](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/33885287080923)
* [Writing code with DB-API](https://classroom.udacity.com/courses/ud197/lessons/3483858580/concepts/35153985360923)
* [Views](https://classroom.udacity.com/courses/ud197/lessons/3490418600/concepts/35140186650923)


### The PostgreSQL documentation

In this project, you'll be using a PostgreSQL database. If you'd like to know a lot more about the kinds of queries that you can use in this dialect of SQL, check out the PostgreSQL documentation. It's a lot of detail, but it spells out _all the many things_ the database can do.

Here are some parts that may be particularly useful to refer to:

*	[The select statement](https://www.postgresql.org/docs/9.5/static/sql-select.html)
*	[SQL string functions](https://www.postgresql.org/docs/9.5/static/functions-string.html)
*	[Aggregate functions](https://www.postgresql.org/docs/9.5/static/functions-aggregate.html)


## Prepare the software and data
[(back to top)](#top)

### The virtual machine

To start on this project, you'll need database software (provided by a Linux virtual machine) and the data to analyze.

This project makes use of the same Linux-based virtual machine (VM) as the preceding lessons.

If you skipped those lessons and came right to this project, that's OK! However, you will need to go back to the instructions to install the virtual machine. This will give you the PostgreSQL database and support software needed for this project. If you have used an older version of this VM, you may need to install it into a new directory.

If you need to bring the virtual machine back online (with `vagrant up`), do so now. Then log into it with `vagrant ssh`.

*Installation instructions includec below for reference.*


#### Intro

In the next part of this course, you'll use a virtual machine (VM) to run an SQL database server and a web app that uses it. The VM is a Linux server system that runs on top of your own computer. You can share files easily between your computer and the VM; and you'll be running a web service inside the VM which you'll be able to access from your regular browser.

We're using tools called [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) to install and manage the VM. You'll need to install these to do some of the exercises. The instructions on this page will help you do this.


#### Conceptual overview

[This video](https://www.youtube.com/watch?v=djnqoEO2rLc) offers a conceptual overview of virtual machines and Vagrant. You don't need to watch it to proceed, but you may find it informative.


#### Use a terminal

You'll be doing these exercises using a Unix-style terminal on your computer. If you are using a **Mac or Linux** system, your regular terminal program will do just fine. On **Windows**, we recommend using the **Git Bash** terminal that comes with the Git software. If you don't already have Git installed, download Git from [git-scm.com](https://git-scm.com/downloads).

For a refresher on using the Unix shell, look back at [our Shell Workshop](https://www.udacity.com/course/ud206).

If you'd like to learn more about Git, take a look at [our course about Git](https://www.udacity.com/course/ud123).


#### Install VirtualBox

VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) Install the _platform package_ for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.


#### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

**Windows users:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

![vagrant --version](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/584881ee_screen-shot-2016-12-07-at-13.40.43/screen-shot-2016-12-07-at-13.40.43.png)

_If Vagrant is successfully installed, you will be able to run_ `vagrant --version`  
_in your terminal to see the version number._  
_The shell prompt in your terminal may differ. Here, the_ `$` _sign is the shell prompt._


#### Download the VM configuration

There are a couple of different ways you can download the VM configuration.

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called **FSND-Virtual-Machine**. It may be located inside your **Downloads** folder.

Alternately, you can use Github to fork and clone the [repository](https://github.com/udacity/fullstack-nanodegree-vm).

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory:


![vagrant-directory](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58487f12_screen-shot-2016-12-07-at-13.28.31/screen-shot-2016-12-07-at-13.28.31.png)

_Navigating to the FSND-Virtual-Machine directory and listing the files in it._  
_This picture was taken on a Mac, but the commands will look the same on Git Bash on Windows._


#### Start the virtual machine

From your terminal, inside the **vagrant** subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

![vagrant-up-start](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488603_screen-shot-2016-12-07-at-13.57.50/screen-shot-2016-12-07-at-13.57.50.png)

_Starting the Ubuntu Linux installation with `vagrant up`._  
_This screenshot shows just the beginning of many, many pages of output in a lot of colors._

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

![linux-vm-login](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58488962_screen-shot-2016-12-07-at-14.12.29/screen-shot-2016-12-07-at-14.12.29.png)

_Logging into the Linux VM with `vagrant ssh`._


#### Logged in!

If you are now looking at a shell prompt that starts with the word `vagrant` (as in the above screenshot), congratulations — you've gotten logged into your Linux VM.

If not, take a look at the **Troubleshooting** section below.


#### The files for this course

Inside the VM, change directory to `/vagrant` and look around with `ls`.

The files you see here are the same as the ones in the `vagrant` subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM.

Files in the VM's `/vagrant` directory are shared with the `vagrant` folder on your computer. But other data inside the VM is not. For instance, the PostgreSQL database itself lives only inside the VM.


#### Running the database

The PostgreSQL database server will automatically be started inside the VM. You can use the `psql` command-line tool to access it and run SQL statements:

![linux-vm-PostgreSQL](https://d17h27t6h515a5.cloudfront.net/topher/2016/December/58489186_screen-shot-2016-12-07-at-14.46.25/screen-shot-2016-12-07-at-14.46.25.png)

_Running `psql`, the PostgreSQL command interface, inside the VM._


#### Logging out and in

If you type `exit` (or `Ctrl-D`) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type `vagrant ssh` again.

If you reboot your computer, you will need to run `vagrant up` to restart the VM.


#### Troubleshooting

##### I'm not sure if it worked.

If you can type `vagrant ssh` and log into your VM, then it worked! It's normal for the `vagrant up` process to display a lot of text in many colors, including sometimes scary-looking messages in red, green, and purple. If you get your shell prompt back at the end, and you can log in, it should be OK.


##### `vagrant up` is taking a long time. Why?

Because it's downloading a whole Linux operating system from the Internet.


##### I'm on Windows, and when I run `vagrant ssh`, I don't get a shell prompt.

Some versions of Windows and Vagrant have a problem communicating the right settings for the terminal. There is a workaround: Instead of `vagrant ssh`, run the command `winpty vagrant ssh` instead.


##### I'm on Windows and getting an error about virtualization.

Sometimes other virtualization programs such as Docker or Hyper-V can interfere with VirtualBox. Try shutting these other programs down first.

In addition, some Windows PCs have settings in the BIOS or UEFI (firmware) or in the operating system that disable the use of virtualization. To change this, you may need to reboot your computer and access the firmware settings. [A web search](https://www.google.com/search?q=enable%20virtualization%20windows%2010) can help you find the settings for your computer and operating system. Unfortunately there are so many different versions of Windows and PCs that we can't offer a simple guide to doing this.


##### Why are we using a VM? It seems complicated.

It is complicated. In this case, the point of it is to be able to offer the same software (Linux and PostgreSQL) regardless of what kind of computer you're running on.


##### I got some other error message.

If you're getting a specific textual error message, try looking it up on your favorite search engine. If that doesn't help, take a screenshot and post it to the discussion forums, along with as much detail as you can provide about the process you went through to get there.


##### If all else fails, try an older version.

Udacity mentors have noticed that some newer versions of Vagrant don't work on all operating systems. Version 1.9.2 is reported to be stabler on some systems, and version 1.9.1 is the supported version on Ubuntu 17.04. You can download older versions of Vagrant from [the Vagrant releases index](https://releases.hashicorp.com/vagrant/).


#### Supporting Materials

[FSND-Virtual-Machine](http://video.udacity-data.com.s3.amazonaws.com/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)


### Download the data

Next, [download the data here.](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database. Review how to use the `psql` command in *Lesson 3.7. Hello PostgreSQL*.

To load the data, `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.  
Here's what this command does:

* `psql` — the PostgreSQL command line program
* `-d news` — connect to the database named news which has been set up for you
* `-f newsdata.sql` — run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

*Getting an error?*

If this command gives an error message, such as —  
`psql: FATAL: database "news" does not exist`  
`psql: could not connect to server: Connection refused`  
— this means the database server is not running or is not set up correctly. This can happen if you have an _older version_ of the VM configuration from before this project was added. To continue, [download the virtual machine configuration](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) into a fresh new directory and start it from there.


### Explore the data

Once you have the data loaded into your database, connect to your database using `psql -d news` and explore the tables using the `\dt` and `\d table` commands and `select` statements.

* `\dt` — display tables — lists the tables that are available in the database.
* `\d table` — (replace _table_ with the name of a table) — shows the database schema for that particular table.

Get a sense for what sort of information is in each column of these tables.

The database includes three tables:

* The `authors` table includes information about the authors of articles.
* The `articles` table includes the articles themselves.
* The `log` table includes one entry for each time a user has accessed the site.

As you explore the data, you may find it useful to take notes! Don't try to memorize all the columns. Instead, write down a description of the column names and what kind of values are found in those columns.


#### Connecting from your code

The database that you're working with in this project is running PostgreSQL, like the `forum` database that you worked with in the course. So in your code, you'll want to use the `psycopg2` Python module to connect to it, for instance:

```python
db = psycopg2.connect("dbname=news")
```

Your task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the `psycopg2` module to connect to the database.


## Your assignment: Build it!
[(back to top)](#top)

### So what are we reporting, anyway?

Here are the questions the reporting tool should answer. The example answers given aren't the right ones, though!


#### 1. What are the most popular three articles of all time?

Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

**Example:**

* "Princess Shellfish Marries Prince Handsome" — 1201 views
* "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
* "Political Scandal Ends In Political Scandal" — 553 views


#### 2. Who are the most popular article authors of all time?

That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

**Example:**

*   Ursula La Multa — 2304 views
*   Rudolf von Treppenwitz — 1985 views
*   Markoff Chaney — 1723 views
*   Anonymous Contributor — 1023 views

#### 3. On which days did more than 1% of requests lead to errors?

The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to [this lesson](https://classroom.udacity.com/courses/ud303/lessons/6ff26dd7-51d6-49b3-9f90-41377bff4564/concepts/75becdb9-da2a-4fbf-9a30-5f3ccd1aa1d6) for more information about the idea of HTTP status codes.)

**Example:**

* July 29, 2016 — 2.5% errors


### Good coding practices

#### SQL style

Each one of these questions can be answered with a single database query. Your code should get the database to do the heavy lifting by using joins, aggregations, and the `where` clause to extract just the information you need, doing minimal "post-processing" in the Python code itself.

In building this tool, you may find it useful to add views to the database. You are allowed and encouraged to do this! However, if you create views, make sure to put the **create view** commands you used into your lab's README file so your reviewer will know how to recreate them.

#### Python code quality

Your code should be written with good Python style. The [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) is an excellent standard to follow. You can do a quick check using the `pep8` command-line tool.


## Frequently asked questions
[(back to top)](#top)

### Q: I modified my database. Can I undo it?

If you'd like to revert the `news` database to its original form, you can do that by dropping each of the tables, then re-importing the data from the `newsdata.sql` file.

In `psql`:

```sql
drop table log;
drop table articles;
drop table authors;
```

Then in the shell, re-import the data:

```sql
psql -d news -f newsdata.sql
```


### Q: These queries are complicated. Where do I start?

One of the best ways to build complex queries is by starting with smaller pieces, and testing each of them in small steps. Here's a worked example —

Suppose we wanted to print out each article's *title and author name.*

Looking at the schema for `articles` (with `\d articles`) we can see there's an author and title column. But the author column doesn't have names in it — just numbers. To see this in your database, run:

```sql
select author from articles;
```

But the `authors` table has a `name` column, and a numeric `id` column. To see this, run:

```sql
select * from authors;
```

Those numeric id values match up with the `articles.author` column. And that means we can connect the two tables with a join:

```sql
select title, name
from articles join authors
on articles.author = authors.id;
```

or:

```sql
select title, name
from articles, authors
where articles.author = authors.id;
```

Try these queries on your `news` database! Look for other relationships that can work with `join`.


## Logs Analysis Rubric
[(back to top)](#top)

### Functionality

Functionality

Running the code displays the correct answers to each of the questions in the lab description.

Compatibility: Database

The code works with the (unchanged) database schema from the lab description.  
It is OK to add views to the database, but don't modify or rename the existing tables.

Compatibility: Language

The code may be written in Python 2 or Python 3 but must be consistent. It should start with a correct shebang line to indicate the Python version.

Well-formatted text output

The code presents its output in clearly formatted plain text. Imagine that you are looking at this text in an email message, not on a web page.

Database queries

The code connects to and queries an SQL database. It does not use answers hardcoded into the application code.


### Code quality

No errors

The project code runs without any error messages or warnings from the language interpreter.

Application code style

The code conforms to the PEP8 style recommendations.  
You can install the `pep8` tool to test this, with `pip install pep8` or `pip3 install pep8` (Python 3).

In order for this requirement to pass, running the `pep8` tool on your code should produce *zero* warnings.

SQL code quality

When the application fetches data from multiple tables, it uses a single query with a join, rather than multiple queries. Each of the questions must be answered using one SQL query.


### README file

README file describes work

The README file includes instructions for how to run the program, as well as a description of the program's design.

Imagine a person who knows Python and SQL well, but has not done this project. If that person read the README would they know how to run this code?

README file includes view definitions, if any

If the code relies on views created in the database, the README file includes the `create view` statements for these views.  
(If the code does not depend on views, ignore this requirement.)

[(back to top)](#top)