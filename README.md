<!---
[![Build Status](https://travis-ci.org/vahidR/restful-todo.svg?branch=master)](https://travis-ci.org/vahidR/restful-todo)
--->

This code is a modification of the code at
[https://github.com/vahidR/restful-todo](https://github.com/vahidR/restful-todo).
It has been modified to support instruction regarding accessing REST APIs and
working with JSON; see
[this](https://github.com/zarthur/CSCC-Fundamentals-Android-Notes/blob/master/week_15/readme.md)
for an example.

Additional user and basic auth code based on
[this tutorial]([this tutorial](http://blog.miguelgrinberg.com/post/restful-authentication-with-flask)


RESTful Todo Application
=========================
A RESTful web-based Todo application in Python and Flask 

Install
========
```
$ python manage.py createall
```

Running
========
```bash
$ python manage.py runserver
```

Test
=====
```bash
$ python manage.py test
```

Remove
========
```bash
$ python manage.py dropall
```


RESTful interactions
====================
**POST a user**
```
curl -H "Content-Type: application/json" -X POST -d '{"username":"username","password":"password"}' -i http://127.0.0.1:5000/todos/api/v1.0/users
```

**GET the List of todos**
```
curl -u test:test -H "Accept: application/json" -i http://localhost:5000/todos/api/v1.0/todos
```

**GET an individual todo**
```
curl -u test:test -H "Accept: application/json" -i http://localhost:5000/todos/api/v1.0/todo/<ID>
```

**POST a todo**
```
curl -u test:test -H "Content-Type: application/json" -X POST -d '{"title":"Lunch", "body":"Having lunch"}' -i http://localhost:5000/todos/api/v1.0/todo/create
```

**UPDATE a todo**
```
curl -u test:test -H "Content-Type: application/json" -X PUT -d '{"title":"Dinner", "body":"Having Dinner"}' -i http://localhost:5000/todos/api/v1.0/todo/update/<ID>
```

**DELETE a todo**
```
curl -u test:test -H "Accept: application/json" -X DELETE http://localhost:5000/todos/api/v1.0/todo/delete/<ID>
```
