# fortune-api  
![https://github.com/danrog303/fortune-api/actions/workflows/ci.yml/badge.svg](https://github.com/danrog303/fortune-api/actions/workflows/ci.yml/badge.svg)
![https://shields.io/github/license/danrog303/fortune-api](https://shields.io/github/license/danrog303/fortune-api)
![Gitmoji](https://img.shields.io/badge/gitmoji-%20📝%20🏗️-FFDD67.svg)
> Django REST api for obtaining inspiring quotes and images based on the current date.   

## ✨ Features
1. Allows to define multiple quote pools
2. Allows to define multiple triggers for every pool (for example: you can display special quotes on Christmas)

## 🔧 How to run?
Application has been written in Python using Django REST Framework. Application will run correctly on Python 3.9 or higher.
```
$ git clone https://github.com/danrog303/fortune-api
$ cd fortune-api/app
$ python3 -m pip install -r requirements.txt
$ python3 manage.py makemigrations && python3 manage.py migrate
$ python3 manage.py runserver
```
Optionally, you can use **python3 manage.py prepopulate** command. This is a custom command that will populate the database with some lorem-ipsum-Albert-Einstein dummy data.

## 💻 How does it work?
### 📝 Glossary  
- __Fortune pool__:  
  a single pool storing text+image pairs, the pool could be for example "Albert Einstein quotes" or "cat jokes";  
- __Fortune image__:  
  the image that is displayed next to the quote (one image can be used by multiple pools and multiple entries simultaneously)  
- __Fortune trigger__:  
  the moment in time when a given group of fortune entries should be displayed (for example: "today is Christmas" or "it's nighttime")  
- __Fortune entry__:  
  some image and text to be displayed, paired with a trigger and related pool  

### 🔖 How to define those things?
Regular user cannot create new pools, images, triggers nor entries. Only administrators can manage data. Fortune triggers are defined in **fortune_triggers/triggers.py** file. Triggers are basically functions: for example, when there is nighttime, **trigger_night** function will return True - otherwise it will return False.  
Pools, images and entries are stored in the database: so to create new objects you can use Django built-in **/admin/** endpoint.

### 📚 How to use fortune-api?
First, you can use HTTP GET method on **/api/** endpoint. Such a query should display all public fortune pools. 
```python
# Example API usage in Python
import requests
response = requests.get("localhost:8000/api/")
print(response.json())
```
```python
# Example JSON response:
[
    {"name": "albert-einstein-quoutes", "description": "Quotes of Albert Einstein."},
    {"name": "cat-jokes", "description": "Images and jokes about cats."}
]
```

Then, to obtain your inspiring quote+image pair, you have to use HTTP GET method on **/api/pool/pool-name/** endpoint. Note that the server will return a 404 error if the specified pool does not exist.
```python
# Example API usage in Python
import requests
response = requests.get("localhost:8000/api/pool/albert-einstein-quotes/")
print(response.json())
```
```python
# Example JSON response:
{
    "text": "Quaerat eius consectetur sed eius dolorem quisquam sit. Consectetur est quaerat amet velit. Adipisci quaerat ut dolorem dolor ut. Dolor dolor ut quaerat dolorem eius magnam voluptatem. Quisquam velit magnam sed numquam modi. Tempora magnam neque neque velit sit amet.",
    "image": {
        "url": "http://127.0.0.1:8000/media/6817fd7b-a972-4d21-8295-f3df8d0eb4eb.jpg/"
    },
    "pool": {
        "last_refresh_date": "2022-06-18T18:37:50",
        "next_refresh_date": "2022-06-18T18:37:55"
    }
}
```

### ⚙️ What does really happen underneath?
When you connect to **/api/**, server will list all existing *public* fortune pools. It is also possible to define non-public pools: then they will not be listed, and to read them you will need to know their name.

When you connect to **/api/pool/pool-name/**, the server will find the pool with the specified name and then will find the correct trigger. When both trigger and pool will be found, the server will retrieve random fortune entry from the database (with corresponding pool and trigger). When multiple users connect to the database, they will receive the same fortune entry each time - retrieved fortune entry refreshes only after some time. Each pool separately defines the time after which a random fortune entry must be refreshed.
