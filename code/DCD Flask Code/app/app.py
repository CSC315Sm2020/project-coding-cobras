#! /usr/bin/python2

"""
IMPORTANT

To run this example in the CSC 315 VM you first need to make
the following one-time configuration changes:

# install psycopg2 python package
sudo apt-get update
sudo apt-get install python-psycopg2

# set the postgreSQL password for user 'csc315sm20'
sudo -u postgres psql
    ALTER USER csc315sm20 PASSWORD 'csc315sm20';
    \q

# install flask
sudo apt-get install python-pip
pip install flask
# logout, then login again to inherit new shell environment

"""

"""

Usage:
export FLASK_APP=app.py 
flask run
# then browse to http://127.0.0.1:5000/

Purpose:
Demonstrate Flask/Python to PostgreSQL using the psycopg
adapter. Connects to the 7dbs database from "Seven Databases
in Seven Days" in the CSC 315 VM.

This example uses Python 2 because Python 2 is the default in
Ubuntu 18.04 LTS on the CSC 315 VM.

For psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
import random
from config import config
from flask import Flask, render_template, request
from datetime import datetime

def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
    
def connectone(query):
    """ Connect to the PostgreSQL database server """
    
    
    print(query)
    
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchone()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
    
def connectnone(query):
    """ Connect to the PostgreSQL database server """
    
    
    print(query)
    
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        
        #commit changes to database
        conn.commit()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return 0
    
 
# app.py

app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('login.html')

# handle form data
@app.route('/form-handler', methods=['POST'])
def handle_data():

    #recives username/password from HTML form potential-match.html
    username = request.form['username']
    password = request.form['password']
    
    user = connect("SELECT * FROM USER_ACCOUNT WHERE fname=\'"+ username + "\' AND pwd= \'" + password + "'")
    astro = ["invalid"]
    pers = ["invalid"]
    user_id =[0]
    
    NUM = connectone("SELECT count(*) FROM USER_ACCOUNT GROUP BY TRUE")
    num = NUM[0]
    
    if (len(user) != 0):
        print("Valid user")  
        astro = connectone("SELECT sign_name FROM SIGN_REF WHERE sign_number = (SELECT astrological_sign FROM USER_ACCOUNT WHERE fname=\'"+ username + "\')")
        pers = connectone("SELECT mbti_name FROM MBTI_REF WHERE mbti_number = (SELECT mb_type FROM USER_ACCOUNT WHERE fname=\'"+ username + "\')")
        user_id = connectone("SELECT user_id FROM USER_ACCOUNT WHERE fname=\'"+ username + "\'")
        user_age = connectone("SELECT age FROM USER_ACCOUNT WHERE fname=\'"+ username + "\'")
        user_description = connectone("SELECT description FROM USER_ACCOUNT WHERE fname=\'"+ username + "\'")
    
        astro_sign = astro[0]
        pers_type = pers[0]
        userID = user_id[0]
        age = user_age[0]
        description = user_description[0]
        matches = []
        
    	#loops from 1 to 20
        for PMID in range(1, num+1):
            if (PMID != userID):
                
                GENDER_PREF = connectone("SELECT gender_pref FROM USER_ACCOUNT WHERE user_id=\'"+str(userID)+"\'")
                PM_GENDER = connectone("SELECT gender FROM USER_ACCOUNT WHERE user_id=\'"+str(PMID)+"\'")
                pm_age = connectone("SELECT age FROM USER_ACCOUNT WHERE user_id=\'"+str(PMID)+"\'")
                USER_AGE_MIN = connectone("SELECT age_min FROM USER_ACCOUNT WHERE user_id=\'"+str(userID)+"\'")
                USER_AGE_MAX = connectone("SELECT age_max FROM USER_ACCOUNT WHERE user_id=\'"+str(userID)+"\'")
                
                #cast string to int for comparison
                PM_AGE = int(pm_age[0])
                

                
                if ( (GENDER_PREF[0] != 'a' and PM_GENDER[0] != GENDER_PREF[0]) or PM_AGE > USER_AGE_MAX[0] or PM_AGE < USER_AGE_MIN[0]):
                    connectnone("UPDATE POTENTIAL_MATCH SET MATCH_RATING =0" + " WHERE user_id=\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'")
                    print("No match, move on") 
                    continue
                
                #Calculates ASTRO Rating
                PM_ASTRO = connectone("SELECT astrological_sign FROM USER_ACCOUNT WHERE user_id=\'"+str(PMID)+"\'")
                ASTRO_MATCH_RATING = connectone("SELECT "+astro_sign+" FROM ASTRO_COMPAT WHERE astrological_sign="+ str(PM_ASTRO[0]))
                
                #Calculates MBTI Rating
                PM_MBTI = connectone("SELECT mb_type FROM USER_ACCOUNT WHERE user_id=\'"+str(PMID)+"\'")
                MBTI_MATCH_RATING = connectone("SELECT "+pers_type+" FROM MBTI_COMPAT WHERE personality_type="+ str(PM_MBTI[0]))
                
                #adds two ratings together
                MATCH_RATING = MBTI_MATCH_RATING[0] + ASTRO_MATCH_RATING[0]
	        
	        #Trying to update the database
                connectnone("UPDATE POTENTIAL_MATCH SET MATCH_RATING =" + str(MATCH_RATING) + " WHERE user_id=\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'") 
                user_vote = connectone("SELECT votes FROM POTENTIAL_MATCH WHERE user_id =\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'") 
                pm_vote = connectone("SELECT votes FROM POTENTIAL_MATCH WHERE user_id =\'" + str(PMID) + "\' AND pm_id=\'" + str(userID)+"\'")
                    
                
                    
                if (user_vote[0] == True and pm_vote[0] == True):
                    match = connectone("SELECT fname, age, email FROM USER_ACCOUNT WHERE user_id=\'"+str(PMID)+"\'")
                    print("Match made!" + str(match[0]))
                    matches.append(match)


    if (len(user) == 0): 
    	matches = ['None']
    	astro_sign = "invalid"
    	pers_type = "invalid"
    	description = "invalid"
    	userID = 0
    	age = 0
    	
    return render_template('user-profile.html', username=username, password=password, astro_sign = astro_sign, pers_type = pers_type, matches=matches, description=description, age=age)


@app.route('/form-handler2', methods=['POST'])
def handle_data2():
    random.seed(datetime.now()) 
    username = request.form['username']
    
    user_id = connectone("SELECT user_id FROM USER_ACCOUNT WHERE fname=\'"+ username + "\'")
    userID = user_id[0]
    
    NUM = connectone("SELECT count(*) FROM USER_ACCOUNT GROUP BY TRUE")
    num = NUM[0]
    
    isPM = False
    PMID = 0
    rating = 0
    
    bucket_array = [False] * num
    bucket_array[userID-1] = True
    all_true = True
    
    while (not (isPM)):
        PMID = (random.randint(1,num))
        
        if (PMID == userID):
            continue
            
        all_true = True
        
        for ID in range(0,num):
            if (bucket_array[ID] == False):
                all_true = False
                break
                
        bucket_array[PMID-1] = True
        
        if (all_true == True):
            break
        
        user_vote = connectone("SELECT votes FROM POTENTIAL_MATCH WHERE user_id =\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'") 
        pm_rating = connectone("SELECT match_rating FROM POTENTIAL_MATCH WHERE user_id =\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'") 
        rating = pm_rating[0]
        
        if (rating==0):
            continue
        
        USER_VOTE = user_vote[0]
        
        if (USER_VOTE == None):
            isPM = True
        
    if (all_true == False):
        astro = connectone("SELECT sign_name FROM SIGN_REF WHERE sign_number = (SELECT astrological_sign FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\')")
        pers = connectone("SELECT mbti_name FROM MBTI_REF WHERE mbti_number = (SELECT mb_type FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\')")
        user_age = connectone("SELECT age FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\'")
        PM_NAME = connectone("SELECT fname FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\'")
        user_description = connectone("SELECT description FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\'")
    
        astro_sign = astro[0]
        pers_type = pers[0] 
        age = user_age[0]
        description = user_description[0]
        pm_name = PM_NAME[0]
        
    if (all_true == True):
       return render_template('no-matches.html')
    
    return render_template('potential-matches.html', PMID=PMID, username=username, pers_type=pers_type, pm_name=pm_name, astro_sign=astro_sign, description=description, age=age, rating=rating)

@app.route('/form-handler3', methods=['POST'])
def handle_data3():
    random.seed(datetime.now()) 
    username = request.form['username']
    vote = request.form['vote']
    PMID = request.form['PM']
    
    user_id = connectone("SELECT user_id FROM USER_ACCOUNT WHERE fname=\'"+ username + "\'")
    userID = user_id[0]
    
    if (vote!="Skip"):
        connectnone("UPDATE POTENTIAL_MATCH SET votes =" + str(vote) + " WHERE user_id=\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'") 
    
    
    NUM = connectone("SELECT count(*) FROM USER_ACCOUNT GROUP BY TRUE")
    num = NUM[0]
    
    isPM = False
    PMID = 0
    rating = 0
    
    bucket_array = [False] * num
    bucket_array[userID-1] = True
    all_true = False
    
    while (not (isPM)):
        PMID = (random.randint(1,num))
        
        if (PMID == userID):
            continue
            
        all_true = True
        
        for ID in range(0,num):
            if (bucket_array[ID] == False):
                all_true = False
                break
                
        bucket_array[PMID-1] = True
        
        if (all_true == True):
            break
        
        user_vote = connectone("SELECT votes FROM POTENTIAL_MATCH WHERE user_id =\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'") 
        pm_rating = connectone("SELECT match_rating FROM POTENTIAL_MATCH WHERE user_id =\'" + str(userID) + "\' AND pm_id=\'" + str(PMID)+"\'") 
        rating = pm_rating[0]
        
        if (rating==0):
            continue
        
        USER_VOTE = user_vote[0]
        
        if (USER_VOTE == None):
            isPM = True
        
    if (all_true == False):
        astro = connectone("SELECT sign_name FROM SIGN_REF WHERE sign_number = (SELECT astrological_sign FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\')")
        pers = connectone("SELECT mbti_name FROM MBTI_REF WHERE mbti_number = (SELECT mb_type FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\')")
        user_age = connectone("SELECT age FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\'")
        PM_NAME = connectone("SELECT fname FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\'")
        user_description = connectone("SELECT description FROM USER_ACCOUNT WHERE user_id=\'"+ str(PMID) + "\'")
    
        astro_sign = astro[0]
        pers_type = pers[0] 
        age = user_age[0]
        description = user_description[0]
        pm_name = PM_NAME[0]
        
    if (all_true == True):
       return render_template('no-matches.html')
    
    return render_template('potential-matches.html', PMID=PMID, username=username, pers_type=pers_type, pm_name=pm_name, astro_sign=astro_sign, description=description, age=age, rating=rating)


if __name__ == '__main__':
    app.run(debug = True)
