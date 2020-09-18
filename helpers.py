import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def lookup(search):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(search)}&key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        search = response.json()
        allBooks = [] #UPDATED
        eachBook = [] #UPDATED
        for value in search.values():
            if type(value) == list:
                for i in value:
                    identity = i['id']
                    eachBook += [identity] 
                    for a, ve in i.items():
                        if type(ve) == dict and a == 'volumeInfo':
                            for row, re in ve.items():
                                if row == 'title':
                                    name = re
                                    eachBook += [name] #UPDATED
                                    
                                if row == 'description':
                                    description = re
                                    eachBook += [description] #UPDATED
                    
                                if row == 'authors':
                                    authors = re[0]
                                    if len(re) > 1:
                                        for names in range(1, len(re)):
                                            authors += ", " +re[names]
                                    authors += "."
                                    eachBook += [authors] #UPDATED
                                    
                                if row == 'pageCount':
                                    pagecount = str(re)
                                    eachBook += [pagecount]#UPDATED
                                    
                                if row == 'industryIdentifiers':
                                    for i in re:
                                        if i['type'] =='ISBN_13':
                                            indentifier = i['identifier']
                                            eachBook += [indentifier]

                            allBooks += [eachBook]#UPDATED
                            eachBook = [] #UPDATED


        return allBooks #UPDATED
    except (KeyError, TypeError, ValueError):
        return None

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function