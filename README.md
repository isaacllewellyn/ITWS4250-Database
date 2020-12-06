# ITWS4250-Database
####Isaac Llewellyn && Shepard Gordon 

To import data:

 Make sure importer.py "connection_string" is set along with the mongodb connection to whatever mongodb you have runnning.
 
 Then, run "python importer.py".



# Final Project Technical Information

The `code` directory the code for our application. It uses python. Requirements to be installed are located within the "requirements.txt" file.




## Database Setup

The database you use for your final project will be defined in `db-setup.sql`. Any of your code may create other database users, and grant them privileges, as you feel is necessary, but your initial access will be limited to the database and user created by the script.

Run it as a superuser: `psql -U postgres postgres < db-setup.sql`.

If your application also requires a non-relational database system, be sure to thoroughly document which system as well as the necessary configuration and setup steps in your `readme.md` file.

## Loading Data

Running `retrieve_data.py` will download the datasets needed and place them in a newly created `datasets` directory within the `code` directory. (Any existing `datasets` directory will be destroyed in the process.)

## Running the Application

The entry point to your application is a single script (`main.py`). It can be run properly from the command line with no additional arguments.

### Organization

Your database code should be separated from your application code, ideally in a separate file (e.g., `load_data/importer.py`). For this project, you can put all of your database-related code that one file if you'd like, but you're free to create additional python files in support of both your application and database code as you feel is appropriate.

Your code should be readable, through the appropriate choice of method, field, and variable names, and the appropriate use of comments. Personally, I prefer "self-documenting" code to excessive comments. Something like this:

```python
user_county_input = input("Enter a county name")
```

is generally preferable to 

```python
# Allow the user to choose a county
usr_ipt = input("Enter a county name")
```



### Queries

Your application should facilitate exploration of the data. Remember that the goal is to demonstrate (and hopefully practice and solidify) your understanding of the concepts discussed in class. In practice, it will be difficult to do that if your application doesn't meet at least the following:

- Five separate queries
- At least two queries that select at least some data from both of your datasets
- At least two queries that showcase syntax beyond the basic `SELECT-FROM-WHERE` clauses (e.g., Grouping, Subqueries, etc.)
- At least two queries that accept input entered by the user (as opposed to just allowing selection from a list of options)

Note that some queries are likely to fulfill more than one of the above requirements simultaneously and that merely filling these requirements might not be sufficient for full marks.

### User Interface

This is not a UI/UX class. A simple text-based command line interface is completely acceptable. If you choose to do more (e.g., a web application) that's fine, but the UI isn't one of the graded components. If you do use something like a web application, your application script still needs to be the entry point for starting that application: ideally it will output a URL that can be opened in the browser (and that information should also be present in the readme).

While the database-related code will be reviewed for the security problems we discuss in class, you may assume for the purposes of this assignment that the UI will not be attacked: don't stress about making it resilient.

## Dependencies

There's a `requirements.txt` file in the `code` directory. It will be run on a fresh python 3.8 virtual environment before running your application.
