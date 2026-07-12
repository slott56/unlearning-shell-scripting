##########################
Unlearning Shell Scripting
##########################

The examples from the Unlearning Shell Scripting book

Installation
=============

There are several steps to getting this ready for experimentation.

If you don't have **uv** installed, see Astral...

1.  Clone or download this https://github.com/slott56/unlearning-shell-scripting repository.

2.  Change to the downloaded directory.

    ..  code-block:: bash

        cd unlearning-shell-scripting

3.  Install required packages to run the demo applications.

    ..  code-block:: bash

        uv sync --all

General Operation
=================

In order to play with the examples, it's helpful
to have a file named ``activate_source.csv``.
This file contains the raw data to be bulk-loaded
into the database.

It's also helpful, of course, to have a database.
In this case, it will be ``unlearning_sql.db``.

To build the file, and the database, execute
the following two steps:

..  code-block:: bash

    python src/fake_data.py
    python src/sql_db_preparation.py

The ``fake_data.py`` program builds the ``activate_source.data`` file.
The ``sql_db_preparation.py`` program loads the database with some (but not all) of the fake data.
This omission of data permits some of the data validation rules to spot
bad data in the input.

Makefile
=========

The ``Makefile`` has targets to help create files and databases.

..  code-block:: bash

    make sql_load

The ``sql_load`` target will build the fake data and populate the database if needed.
It will run the SQL-based loader application.

..  code-block:: bash

    make python_load


The ``python_load`` target will build the fake data and populate the database if needed.
It will run the Python-based loader application.

Diagrams
========

The diagrams were built with PlantUML. See https://plantuml.com for more information.
This is not required to run the demonstration applications.
It's handy for creating entity-relationship diagrams.
