[![Build Status](https://travis-ci.org/jennizalwango/epicmail2.svg?branch=ft-delete)](https://travis-ci.org/jennizalwango/epicmail2)
[![Coverage Status](https://coveralls.io/repos/github/jennizalwango/epicmail2/badge.svg?branch=ft-delete)](https://coveralls.io/github/jennizalwango/epicmail2?branch=ft-delete)
[![Maintainability](https://api.codeclimate.com/v1/badges/b188f0d76827a1124f58/maintainability)](https://codeclimate.com/github/jennizalwango/epicmail2/maintainability)

## project name 
  epic mail

## project overview
  Epic mail is an online system that improves and makes communcation easliy where a user 
  Create a user account.Sign in the system.Get all received emails.
  Get all the unread emails and get all emails sent by a the other user.
  Get a specific user’s email.
  Send email to individuals.Delete an email in a user’s inbox

## Prerequisties
Inorder  to run this application you need the following;
you need to have [python3](https://www.python.org/downloads/)  installed on your machine.

You need to have [flask](http://flask.pocoo.org/docs/1.0/installation/) installed on your machine.

## Installing 

##You have to install a virutualenvirnoment, 
 `pip3 install virtualenv`.


##Create the virtual envirnoment
 `virtualenv myenv`.


##Activate your virtualenv to start working.
 `source myenv/bin/activate`.

Install the app dependencies,these are found in the `requirements.txt`

The application is bulit with a python flamework called [Flask](http://flask.pocoo.org/).
Go on and install pylint to help you run the tests of the application

### To run the tests:
  `python -m pytest`  or
  `python -m unittest`  and this will show you the coverage of the tests locally

Install all application requirements from the requirements files found in the root folder
 `pip install -r requirements`
All done! Now,start your server by running  `python run.py`.


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
