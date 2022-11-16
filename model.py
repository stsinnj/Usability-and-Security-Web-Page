'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random

import no_sql_db
from hashlib import sha256
import bottle

database = no_sql_db.DB()
database.tables["users"].create_entry([1, "admin", sha256(("password").encode()).hexdigest()])
database.tables["users"].create_entry([1, "bob", "da7655b5bf67039c3e76a99d8e6fb6969370bbc0fa440cae699cf1a3e2f1e0a1"])
database.tables["users"].create_entry([1, "alice", "13dc8554575637802eec3c0117f41591a990e1a2d37160018c48c9125063838a"])
# database.tables["users"].create_entry([2, "",sha256(("password").encode()).hexdigest()])
database.add_table("chats","sender","receiver","content")
# database.tables["chats"].create_entry("")

# Initialise our views, all arguments are defaults for the template
page_view = view.View()
global chats
temp = []

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True
    
    # if username != "admin": # Wrong Username
    #     err_str = "Incorrect Username"
    #     login = False
    if not database.search_table("users","username",username)\
         or not database.search_table("users","password",password):
        err_str = "Incorrect Username or Password."
        login = False      
    
    if password == "" or username == "": # blank password or username
        return page_view("login")
    if bottle.request.get_cookie("user") == "alice":
        friend = "bob"    
    else:
        friend = "alice"
    print(bottle.request.get_cookie("user"))
    string = "<div class='"+'friends'+" ' id='"+friend+"'> "+ friend +"</div>"
    if login: 
        global current_user
        # welcome_user_model(username)
        current_user = username
        chats = ""
        return page_view("valid", chats= chats, friend = string)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------

def chat_history(new_message, sender):
    message = []
    message.append(sender)
    message.append(new_message)
    temp.append(message)
    chats=" "
    # print("current user:",current_user)
    # print(bottle.request.get_cookie("user"))
    # print(temp)


    for s,t in temp:
        if s == bottle.request.get_cookie("user"):
            string = "btalk"
        else:
            string = "atalk"
        chats  += '<div class='+string+'><span> '+ t +'</span></div>'
    
    if bottle.request.get_cookie("user") == "alice":
        
        friend = "bob"    
    else:
        friend = "alice"
    string = "<div class=friends id='"+friend+"'> "+ friend +"</div>"
    print(bottle.request.get_cookie("user"))
    print(string)
        

    return page_view("valid", chats= chats, friend = string)

#-----------------------------------------------------------------------------

# def welcome_user_model(user):

#     return page_view("header", User = user)




#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)