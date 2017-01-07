# RESTful Todo Application
A RESTful web-based Todo application in Python and Flask

<!---
[![Build Status](https://travis-ci.org/vahidR/restful-todo.svg?branch=master)](https://travis-ci.org/vahidR/restful-todo)
--->

This code is a modification of the code at
[https://github.com/vahidR/restful-todo](https://github.com/vahidR/restful-todo).
It has been modified to support instruction regarding the use of REST APIs and
working with JSON by multiple users; see
[this](https://github.com/zarthur/CSCC-Fundamentals-Android-Notes/blob/master/week_15/readme.md)
for an example.

Additional user and basic auth code based on
[this tutorial](http://blog.miguelgrinberg.com/post/restful-authentication-with-flask)



## Install
```
$ python manage.py createall
```

## Running
```bash
$ python manage.py runserver
```

## Test
```bash
$ python manage.py test
```

## Remove
```bash
$ python manage.py dropall
```


## RESTful interactions

### POST a user
This is currently the **only** way to add a user.

*Request*

```
curl -H "Content-Type: application/json" -X POST -d '{"username":"username","password":"password"}' -i http://127.0.0.1:5000/todos/api/v1.0/user/create
```

*Response*

```
HTTP/1.1 201 CREATED
Date: Tue, 03 May 2016 00:15:51 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 24

{
  "username": "username"
}
```

### GET the List of todos
*Request*

```
curl -u username:password -H "Accept: application/json" -i http://localhost:5000/todos/api/v1.0/todos
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:35:58 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 265

{
  "todos": [
    {
      "body": "mow grass",
      "done": false,
      "uuid": "5494bb0a-e8c8-49b8-a584-ccdcc4f0e1f8",
      "priority": 1,
      "title": "grass"
    },
    {
      "body": "prepare dinner",
      "done": false,
      "uuid": "f012b899-3819-44fd-91c7-2f06fddffb99",
      "priority": 3,
      "title": "dinner"
    }
  ]
}
```

### GET an individual todo
*Request*

```
curl -u username:password -H "Accept: application/json" -i http://localhost:5000/todos/api/v1.0/todo/<UUID>
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:37:35 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 116

{
    "body": "mow grass",
    "done": false,
    "uuid": "5494bb0a-e8c8-49b8-a584-ccdcc4f0e1f8",
    "priority": 1,
    "title": "grass"
}
```

### POST a todo
*Request*
```
curl -u username:password -H "Content-Type: application/json" -X POST -d '{"title":"dinner", "body":"prepare dinner", "priority": 3}' -i http://localhost:5000/todos/api/v1.0/todo/create
```

*Response*
```
HTTP/1.1 201 CREATED
Date: Tue, 03 May 2016 09:31:32 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 96

{
  "body": "prepare dinner",
  "done": false,
  "uuid": "f012b899-3819-44fd-91c7-2f06fddffb99",
  "priority": 3,
  "title": "dinner"
}
```

### UPDATE a todo
*Request*

```
curl -u username:password -H "Content-Type: application/json" -X PUT -d '{"title":"dinner", "body":"eat dinner", "priority": 2}' -i http://localhost:5000/todos/api/v1.0/todo/update/<UUID>
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:40:41 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 118

{
    "body": "eat dinner",
    "done": false,
    "id": "f012b899-3819-44fd-91c7-2f06fddffb99",
    "priority": 2,
    "title": "dinner"
}
```

### DELETE a todo
*Request*

```
curl -u username:password -H "Accept: application/json" -X DELETE -i http://localhost:5000/todos/api/v1.0/todo/delete/<UUID>
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:44:43 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 31

{
  "result": "Todo deleted."
}
```