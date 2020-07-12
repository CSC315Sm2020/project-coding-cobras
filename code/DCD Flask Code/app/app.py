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
from config import config
from flask import Flask, render_template, request
 
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
    
 
# app.py

app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    return render_template('login.html')

#db_cursor = db_conn.cursor()

# handle form data
@app.route('/form-handler', methods=['POST'])
def handle_data():

    username = request.form['username']
    password = request.form['password']
    astro = connectone("SELECT sign_name FROM SIGN_REF WHERE sign_number = (SELECT astrological_sign FROM USER_ACCOUNT WHERE fname=\'"+ username + "\')")
    pers = connectone("SELECT mbti_name FROM MBTI_REF WHERE mbti_number = (SELECT mb_type FROM USER_ACCOUNT WHERE fname=\'"+ username + "\')")
    user_id = connectone("SELECT user_id FROM USER_ACCOUNT WHERE fname=\'"+ username + "\'")
    user = connect("SELECT * FROM USER_ACCOUNT WHERE fname=\'"+ username + "\' AND pwd= \'" + password + "'")
    
    astro_sign = astro[0]
    pers_type = pers[0]
    userID = user_id[0]
    
    
    
    for PMID in range(20):
        if (PMID != userID):
            PM_ASTRO = connectone("SELECT astrological_sign FROM USER_ACCOUNT WHERE user_id=\'"+str(PMID)+"\'")
	    print("pm_astro"+PM_ASTRO[0])
#MATCH_RATING = connectone("SELECT "+astro_sign+" FROM ASTRO_COMPAT WHERE astrological_sign=\'"+PM_ASTRO+"\'")
#print("PM: " + PM_ASTRO + "\n USER_ASTRO" + astro_sign + "\n RATING:" + MATCH_RATING + "\n\n")
#"UPDATE POTENTIAL_MATCH SET match_rating = (SELECT astrological_sign FROM ASTRO_COMPAT WHERE " + PMID + "=" + astro_sign"
    
    
    if (len(user) == 0): 
    	user = ['Not a valid user']
    	
    	
    
    
    return render_template('user-matches.html', username=username, password=password, astro_sign = astro_sign, pers_type = pers_type, user=user)

if __name__ == '__main__':
    app.run(debug = True)
