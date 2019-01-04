
Optimal Resource Assignment by Genetic Algorithm
_________________________________________________

The goal of this project is to assign resources to tasks by considering the preferences of resources and the preferences of high authorities that manage the tasks. 



Built With
___________

Python


Prerequisites
______________


0. Downloading Python

Python and a Python IDE should be installed. 


1. List of Python module requirements:

- pip install pyodbc #for database connection
- pip install Tkinter #for creating the user interface
- pip install tkFont #for specifying fonts while creating user interface 
- pip install numpy
- pip install --upgrade google-api-python-client oauth2client #for reading Google Spreadsheets 
- pip install xlsxwriter #for downloading Excel files
- pip install pil 


Running the Program
_______________________


In order to run the program, source course should be downloaded and run in a Python IDE. 


How to use the program?
_______________________


1- Run gui_noDB.py.

2- A user interface will appear which will direct the user.

ps: gui_noDB.py is actually created for the cases when there is no database is connected to system. This extension is requested
by our project advisor.

gui_DB is the one which works with database.


Explanation of .py files
_________________________


Assignment_DB.py is the file that makes does the assignment process, and it is connected to the UI which works with the Azure Database.

Assignment_noDB.py is the file that makes does the assignment process, but it is connected to UI which works with no database, but only the data
comes from two Google Spreadsheets.

excel_read.py reads the necessary fields from Google Spreadsheets which is represented by URL.

sqlconn.py is for writing necessary data about assignment to the database.

Course.py, Instructor.py, TeachingAssistant.py, Preference.py are the object classes which are used in the Assignment.py

ps: the comments made for each function in Assignment_noDB.py is also valid for Assignment_DB.py


 
