## project name 
  Epic Mail

## project overview
  Epic mail is an online system that improves and makes communcation easliy where a user 
  Create a user account.Sign in the system.Get all received emails.
  Get all the unread emails and get all emails sent by a the other user.
  Get a specific user’s email.
  Send email to individuals.Delete an email in a user’s inbox

## Getting started
 These instructions will get you acopy of the project up and running on your local machine for development and testing purposes

## Prerequisties
Inorder  to run this application you need the following;
you need to have [python3](https://www.python.org/downloads/)  installed on your machine.

You need to have [flask](http://flask.pocoo.org/docs/1.0/installation/) installed on your 
machine.

The application is bulit with a python flamework called [Flask](http://flask.pocoo.org/).
Go on and install pylint to help you run the tests of the application
Pylint is allows someone to write code following a specific style guide

 to install it run
`pip install pylint`

## Installing 

To clone this appplication ;

`https://github.com/jennizalwango/EPIC_MAIL.git`


Then change into the directory

 `cd <app directory>`

 Extract and open this application in a text editor eg 
 `VScode`
 `Submile`
 `Atom`
  
##You have to install a virutualenvirnoment, 
 `pip3 install virtualenv`.


##Create the virtual envirnoment
 `virtualenv myenv`.

##Activate your virtualenv to start working.
For Windows:
 ` (virtualenv name)\scripts\activate`

	  and 

For Linux:
 ` source(virtualenv name)/bin/activate`

 Good then install the app dependencies,these are found in the `requirements.txt`

 `pip install -r requiremnets.txt`

This will help you get all the app dependencies used in the application development

Execute the application by running a given command 

 `python run.py`

After running that command the server will start running http://127.0.0.1.5000/ which is the default URL 

### To run the tests:
  `python -m pytest`  or
  `python -m unittest`  and this will show you the coverage of the tests locally


## Functionality
-Create an account and sign in to the system

-Get all received emails.

-Get all the unread emails

-Get all emails sent by a the other user

-Get a specific user’s email

-Send email to individuals.

-Delete an email in a user’s inbox


## Supported Endpoints
| Method | Endpoint | Description | Body  |
|--------|----------|-------------|-------|
| POST   |/auth/signup/ |Create User|{"first_name":"jenny", "last_name":"zawal","password":"jenny123","email":"jenny23@gmail.com", "is_admin": true}|
| POST   |/auth/login/ |Log in User|{"email": "jenny123@gmail.com", "password":"jenny123"}|
| POST   |/messages/ |Create  or send a message|{"subject": "hackthon", "message":"we will hold an hackthon", "status":"sent"}|
| GET    |/messages/unread|/status/|Get all unread message|
| GET    |/messages/|Get all received message|
| GET    |/messages/sent/status/|Get all sent messages|
| GET    |/messages/<message-id>/|get a specific email message|
| DELETE |/messages/<message-id>/|Delete a specific message|