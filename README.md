# RESTful Contacts Application
A RESTful web-based Contacts application in Python and Flask

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

### GET the List of Contacts
*Request*

```
curl -u username:password -H "Accept: application/json" -i http://localhost:5000/contacts/api/v1.0/contacts
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:35:58 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 265

{
  "contacts": [
    {
      "name": "bob",
      "email": "bob@bob.com",
      "address": "123 Main St",
      "favorite": false,
      "uuid": "5494bb0a-e8c8-49b8-a584-ccdcc4f0e1f8"
    },
    {
      "name": "sue",
      "email": "sue@sue.com",
      "address": "456 High St",
      "favorite": true,
      "uuid": "f012b899-3819-44fd-91c7-2f06fddffb99"
    }
  ]
}
```

### GET an individual contact
*Request*

```
curl -u username:password -H "Accept: application/json" -i http://localhost:5000/contacts/api/v1.0/contact/<UUID>
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:37:35 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 116

{
  "name": "bob",
  "email": "bob@bob.com",
  "address": "123 Main St",
  "favorite": false,
  "uuid": "5494bb0a-e8c8-49b8-a584-ccdcc4f0e1f8"
}
```

### POST a contact
*Request*
```
curl -u username:password -H "Content-Type: application/json" -X POST -d '{"name":"sue", "email":"sue@sue.com", "address": "456 High St", "favorite": true}' -i http://localhost:5000/contacts/api/v1.0/contact/create
```

*Response*
```
HTTP/1.1 201 CREATED
Date: Tue, 03 May 2016 09:31:32 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 96

{
  "name": "sue",
  "email": "sue@sue.com",
  "address": "456 High St",
  "favorite": true,
  "uuid": "f012b899-3819-44fd-91c7-2f06fddffb99"
}
```

### UPDATE a contact
*Request*

```
curl -u username:password -H "Content-Type: application/json" -X PUT -d '{"email": "sue@email.com"}' -i http://localhost:5000/contacts/api/v1.0/contact/update/<UUID>
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:40:41 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 118

{
  "name": "sue",
  "email": "sue@email.com",
  "address": "456 High St",
  "favorite": true,
  "uuid": "f012b899-3819-44fd-91c7-2f06fddffb99"
}
```

### DELETE a contact
*Request*

```
curl -u username:password -H "Accept: application/json" -X DELETE -i http://localhost:5000/contacts/api/v1.0/contact/delete/<UUID>
```

*Response*

```
HTTP/1.1 200 OK
Date: Tue, 03 May 2016 09:44:43 GMT
Server: Werkzeug/0.11.4 Python/3.4.3+
Content-Type: application/json
Content-Length: 31

{
  "result": "Contact deleted."
}
```