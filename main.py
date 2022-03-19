#Made by Shreya Bista

from flask import Flask, jsonify, render_template, request, session, redirect

# for database

from flask_mysqldb import MySQL

from flask_session import Session

# for unique tokens
import uuid


app = Flask(__name__)

# databse setting for mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbase_trekapp'

mysql = MySQL(app)

# session settings
# false means no time limit on login
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)


@app.route('/')
def home():
    logged_in_user = None

    if session.get('email'):
        logged_in_user = session['email']
    return render_template('index.html', result={'logged_in_user': logged_in_user})


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


# methods = is added only for post method
@app.route('/doLogin', methods=['POST'])
def doLogin():
    # 'email' is name="email" of login.html in <input of email field
    email = request.form['email']
    password = request.form['psw']

    # to give place to hit query of mysql->cursor
    cursor = mysql.connection.cursor()
    resp = cursor.execute(
        '''SELECT id,email ,full_name FROM users WHERE email=%s and password=%s;''', (email, password))

    # fetchall() is for select
    user = cursor.fetchone()
    cursor.close()
    # print(user)
    # if  email/password entered and email/password in database match response=1
    if resp == 1:
        session['email'] = email
        session['userId'] = user[0]
        logged_in_user = session.get('email')
        # session['userId'] = user[0]
        return render_template('home.html', result={'logged_in_user': logged_in_user})
    else:
        return render_template('login.html', result="Invalid Credentials")


@app.route('/doRegister', methods=['POST'])
def doRegister():
    full_name = request.form['full_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    address = request.form['address']

    password = request.form['psw']

    cursor = mysql.connection.cursor()
    resp = cursor.execute('''INSERT INTO `users` (`id`, `full_name`, `address`, `email`, `phone_number`, `password`) VALUES (NULL, %s, %s, %s, %s, %s);''',
                          (full_name, address, email, phone_number, password))

    # .commit() is needed to be done for all the sql quries where you add some data to table like insert and update but not select
    mysql.connection.commit()
    cursor.close()

    # return "Hello"

    if resp == 1:
        return render_template('login.html')
    else:
        return render_template('register.html', result="User not registered successfully")

# for trek destinations


@app.route('/treks')
def allTreks():

    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT td.id as 'SNO', td.title as 'Title',
    td.days AS 'Days' , td.difficulties as 'Difficulty'
     ,td.total_cost as 'Total cost', td.upvotes as 'Upvotes', 
     u.full_name as 'Full name',u.id as 'userId' FROM `trek_destinations`
    as td JOIN users as u ON td.user_id=u.id;''')
    treks = cursor.fetchall()

    cursor.close()
    logged_in_user = None
    if session.get('email'):
        logged_in_user = session['email']

    if session.get('userId'):
        userId = session.get('userId')
    return render_template('listing.html', result={"treks": treks, "logged_in_user": logged_in_user, "userId": userId})

# to render trek destination details


@app.route('/trek/<int:trekId>')
def getTrekbyId(trekId):

    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT td.id as 'SNO', td.title as 'Title',
    td.days AS 'Days' , td.difficulties as 'Difficulty'
     ,td.total_cost as 'Total cost', td.upvotes as 'Upvotes', 
     u.full_name as 'Full name' FROM `trek_destinations`
    as td JOIN users as u ON td.user_id=u.id where td.id=%s;''', (trekId, ))
    trek = cursor.fetchone()

    cursor.close()
# for iternaries start a new cursor
    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT * FROM `iternaries` WHERE `trek_destination_id`=%s;''', (trekId, ))
    iternaries = cursor.fetchall()

    cursor.close()

    return render_template('trekdetail.html', result={"trek": trek, "iternaries": iternaries})


@app.route('/logout')
def logout():
    session["email"] = None
    session["userId"] = None

    return redirect("/")


@app.route('/addTrek')
def addTrek():
    if session.get('email'):
        logged_in_user = session['email']

    return render_template('addtrek.html', result={'logged_in_user': logged_in_user})


@app.route('/doAddTrek', methods=['POST'])
def doAddTrek():
    logged_in_user = None

    if session.get('email'):
        logged_in_user = session['email']

    title = request.form['title']
    days = request.form['days']
    difficulty = request.form['difficulty']
    total_cost = request.form['total_cost']
    upvotes = 0

    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT id FROM `users` WHERE `email`=%s;''', (logged_in_user, ))
    user = cursor.fetchone()
    cursor.close()
    # pulling id from database
    userId = user[0]

    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO `trek_destinations` VALUES (NULL, %s, %s, %s, %s, %s,%s);''',
                   (title, days, difficulty, total_cost, upvotes, userId))

    mysql.connection.commit()
    cursor.close()

    return redirect('/treks')

# to edit treks


@app.route('/editTrek/<int:trekId>')
def editTrek(trekId):
    logged_in_user = None
    if session.get('email'):
        logged_in_user = session["email"]

    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT td.id as 'SNO', td.title as 'Title',
    td.days AS 'Days' , td.difficulties as 'Difficulty'
     ,td.total_cost as 'Total cost', td.upvotes as 'Upvotes', 
     u.full_name as 'Full name' FROM `trek_destinations`
    as td JOIN users as u ON td.user_id=u.id where td.id=%s;''', (trekId, ))
    trek = cursor.fetchone()
    cursor.close()

    return render_template('editTrek.html', result={'trek': trek, 'logged_in_user': logged_in_user})


@app.route('/doUpdateTrek', methods=['POST'])
def doUpdateTrek():
    logged_in_user = None

    if session.get('email'):
        logged_in_user = session['email']

    title = request.form['title']
    days = request.form['days']
    difficulty = request.form['difficulty']
    total_cost = request.form['total_cost']
    trekId = request.form['trekId']

    cursor = mysql.connection.cursor()
    cursor.execute('''UPDATE `trek_destinations` SET `title`=%s,`days`=%s,`difficulties`=%s,`total_cost`=%s WHERE`id`=%s;''',
                   (title, days, difficulty, total_cost, trekId))

    mysql.connection.commit()
    cursor.close()

    return redirect('/treks')
# to delete the trek


@app.route('/doDeleteTrek/<int:trekId>')
def doDelete(trekId):
    cursor = mysql.connection.cursor()
    cursor.execute(
        '''DELETE from `trek_destinations` WHERE `id`=%s;''', (trekId,))
    mysql.connection.commit()
    cursor.close()

    return redirect('/treks')


@app.route('/addIternary')
def addIternary():
    logged_in_user = None
    if session.get('email'):
        logged_in_user = session["email"]
    cursor = mysql.connection.cursor()
    # pulling id from session without going to database
    userId = None
    if session.get('userId'):
        userId = session.get('userId')

    cursor.execute(
        '''SELECT id,title from `trek_destinations` where user_id=%s ;''', (userId,))
    treks = cursor.fetchall()

    cursor.close()

    return render_template('addIternary.html', result={'treks': treks, 'logged_in_user': logged_in_user})


@app.route('/doAddIternary', methods=['POST'])
def doAddIternary():
    logged_in_user = None

    if session.get('email'):
        logged_in_user = session['email']

    title = request.form['title']
    day = request.form['day']
    start_place = request.form['start_place']
    end_place = request.form['end_place']
    description = request.form['description']
    duration = request.form['duration']
    cost = request.form['cost']
    trek_destination_id = request.form['trek_destination_id']

    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO `iternaries` VALUES (NULL,%s, %s, %s, %s, %s,%s,%s,%s)''',
                   (title, day, start_place, end_place, description, duration, cost, trek_destination_id))

    mysql.connection.commit()
    cursor.close()

    return redirect('/treks')


@app.route('/iternary/<int:trekId>')
def getIternaryByTrekId(trekId):

    # for iternaries start a new cursor
    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT * FROM `iternaries` WHERE `trek_destination_id`=%s;''', (trekId, ))
    iternaries = cursor.fetchall()

    cursor.close()

    return render_template('iternary.html', result={"trekId": trekId, "iternaries": iternaries})

# afno trek destinations matra dekhauney


@app.route('/myTreks/<string:param>')
def getTreksbyUser(param):
    userId = None
    if session.get('email'):
        logged_in_user = session['email']

    if session.get('userId'):
        userId = session.get('userId')
    cursor = mysql.connection.cursor()
    if param == "user":
        cursor.execute(
            '''SELECT * FROM `trek_destinations` WHERE `user_id`=%s;''', (userId, ))
    else:
        cursor.execute(
            '''SELECT * FROM `trek_destinations`;''')

    treks = cursor.fetchall()

    cursor.close()
    return render_template('mytreks.html', result={"treks": treks, "userId": userId})


# for searching

@app.route('/search/treks')
def search():
    keyword = request.args.get("keyword")
    cursor = mysql.connection.cursor()
    searchString = "%" + keyword + "%"
    cursor.execute(
        '''SELECT * FROM `trek_destinations`
    WHERE `title` Like %s;''', (searchString,))
    treks = cursor.fetchall()
    cursor.close()

    logged_in_user = None
    if session.get('email'):
        logged_in_user = session['email']

    if session.get('userId'):
        userId = session.get('userId')
    result = {'treks': treks, 'logged_in_user': logged_in_user}

    return render_template('mytreks.html', result={"treks": treks, "userId": userId})


# """
# API INTERFACES DEFINED FROM HERE
# """

@app.route('/api/doRegister', methods=['POST'])
def doRegisterAPI():
    print(request.json)

    full_name = request.json['full_name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']

    password = request.json['psw']

    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO `users` (`id`, `full_name`, `address`, `email`, `phone_number`, `password`) VALUES (NULL, %s, %s, %s, %s, %s);''',
                   (full_name, address, email, phone_number, password))

    # .commit() is needed to be done for all the sql quries where you add some data to table like insert and update but not select
    mysql.connection.commit()
    cursor.close()

    return jsonify({"result": "Registered User Successfully"})


@app.route('/api/doLogin', methods=['POST'])
def doLoginApi():
    # 'email' is name="email" of login.html in <input of email field
    email = request.json['email']
    password = request.json['psw']

    # to give place to hit query of mysql->cursor
    cursor = mysql.connection.cursor()
    resp = cursor.execute(
        '''SELECT id,email ,full_name FROM users WHERE email=%s and password=%s;''', (email, password))

    # fetchall() is for select
    user = cursor.fetchone()
    cursor.close()

    # print(user)
    # if  email/password entered and email/password in database match response=1

    # token=""

    if resp == 1:
        session['email'] = email
        session['userId'] = user[0]
        logged_in_user = session.get('email')

        token = str(uuid.uuid4())

        # put that token to database
        cursor = mysql.connection.cursor()
        resp = cursor.execute(
            '''UPDATE users set token=%s WHERE email=%s ;''', (token, email))
        mysql.connection.commit()

        # fetchall() is for select
        user = cursor.fetchone()
        cursor.close()

        return jsonify({"message": "Successful Login", "loggedIn": True, "token": token})

    else:

        return jsonify({"result": "Login Failed ,Please check your username and password", "loggedIn": False})


# REST APIS are defined from here

def _validate_token(token):
    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT id FROM users WHERE token=%s;''', (token,))

    # fetchall() is for select
    user = cursor.fetchone()
    cursor.close()
    userId = 0

    if user is not None:
        userId = user[0]
    return userId


@app.route('/rest/treks')
def allAPITreks():

    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT td.id as 'SNO', td.title as 'Title',
    td.days AS 'Days' , td.difficulties as 'Difficulty'
     ,td.total_cost as 'Total cost', td.upvotes as 'Upvotes', 
     u.full_name as 'Full name' FROM `trek_destinations`
    as td JOIN users as u ON td.user_id=u.id;''')
    treks = cursor.fetchall()

    cursor.close()
    logged_in_user = None
    if session.get('email'):
        logged_in_user = session['email']
    result = {'treks': treks, 'logged_in_user': logged_in_user}

    return jsonify(result)


@app.route('/rest/treks', methods=['POST'])
def doAddTrekApi():
    logged_in_user = None

    if session.get('email'):
        logged_in_user = session['email']

    title = request.json['title']
    days = request.json['days']
    difficulty = request.json['difficulty']
    total_cost = request.json['total_cost']
    token = request.json['token'] or None

    userId = _validate_token(token)
    if userId == 0:
        return jsonify({"message": "Please enter a valid token"})

    upvotes = 0

    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO `trek_destinations` VALUES (NULL, %s, %s, %s, %s, %s,%s);''',
                   (title, days, difficulty, total_cost, upvotes, userId,))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Trek has been added Successfully"})


@app.route('/rest/treks', methods=['PUT'])
def doUpdateTrekApi():
    title = request.json['title']
    days = request.json['days']
    difficulty = request.json['difficulty']
    total_cost = request.json['total_cost']
    trekId = request.json['trekId']

    token = request.json['token'] or None
    userId = _validate_token(token)
    if userId == 0:
        return jsonify({"message": "Please enter a valid token"})

    cursor = mysql.connection.cursor()
    resp = cursor.execute('''UPDATE `trek_destinations` SET `title`=%s,`days`=%s,`difficulties`=%s,`total_cost`=%s WHERE`id`=%s and `user_id`=%s ;''',
                          (title, days, difficulty, total_cost, trekId, userId))
    if resp == 0:
        return jsonify({"message": "you cannot update someone else's trek"})

    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Trek has been updated Successfully"})


# to delete the trek
@app.route('/rest/treks', methods=['DELETE'])
def doDeleteTrekApi():

    trekId = request.json["trekId"]

    token = request.json['token'] or None
    userId = _validate_token(token)
    if userId == 0:
        return jsonify({"message": "Please enter a valid token"})

    cursor = mysql.connection.cursor()
    resp = cursor.execute(
        '''DELETE from `trek_destinations` WHERE `id`=%s and `user_id`=%s ;''', (trekId, userId))
    if resp == 0:
        return jsonify({"message": "you cannot delete someone else's trek"})

    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Trek has been deleted Successfully"})


# method for search=trek
# @app.route('/api/treks/search/<string:keyword>',)
# def search(keyword):

# another method for ?keyword=trek
@app.route('/api/search/treks')
def searchApi():
    keyword = request.args.get("keyword")
    cursor = mysql.connection.cursor()
    searchString = "%" + keyword + "%"
    cursor.execute(
        '''SELECT * FROM `trek_destinations`
    WHERE `title` Like %s;''', (searchString,))
    treks = cursor.fetchall()
    cursor.close()

    logged_in_user = None
    if session.get('email'):
        logged_in_user = session['email']
    result = {'treks': treks, 'logged_in_user': logged_in_user}

    return jsonify(result)


app.run(debug=True)

# this hidden code consists of API endpoints that are not REST
"""       
@app.route('/api/treks')
def allAPITreks():

    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT td.id as 'SNO', td.title as 'Title',
    td.days AS 'Days' , td.difficulties as 'Difficulty'
     ,td.total_cost as 'Total cost', td.upvotes as 'Upvotes', 
     u.full_name as 'Full name' FROM `trek_destinations`
    as td JOIN users as u ON td.user_id=u.id;''')
    treks = cursor.fetchall()

    cursor.close()
    logged_in_user = None
    if session.get('email'):
        logged_in_user = session['email']
    result={'treks':treks,'logged_in_user': logged_in_user}

    return jsonify(result)

@app.route('/api/doAddTrek', methods=['POST'])
def doAddTrekApi():
    logged_in_user = None

    if session.get('email'):
        logged_in_user = session['email']

    title = request.json['title']
    days = request.json['days']
    difficulty = request.json['difficulty']
    total_cost = request.json['total_cost']
    token=request.json['token'] or None
    
    userId=_validate_token(token)
    if userId == 0:
        return jsonify({"message":"Please enter a valid token" })

    upvotes = 0

    

    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO `trek_destinations` VALUES (NULL, %s, %s, %s, %s, %s,%s);''',
                          (title, days, difficulty, total_cost, upvotes,userId,))



    
    mysql.connection.commit()
    cursor.close()

    
    return jsonify({"message":"Trek has been added Successfully"})


@app.route('/api/doUpdateTrek', methods=['PUT'])
def doUpdateTrekApi():
    title = request.json['title']
    days = request.json['days']
    difficulty = request.json['difficulty']
    total_cost = request.json['total_cost']
    trekId=request.json['trekId']

    token=request.json['token'] or None
    userId=_validate_token(token)
    if userId == 0:
        return jsonify({"message":"Please enter a valid token" })
   
    cursor = mysql.connection.cursor()
    resp=cursor.execute('''UPDATE `trek_destinations` SET `title`=%s,`days`=%s,`difficulties`=%s,`total_cost`=%s WHERE`id`=%s and `user_id`=%s ;''',
                          (title, days, difficulty, total_cost,trekId,userId))
    if resp==0:
        return jsonify({"message":"you cannot update someone else's trek"})

    
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message":"Trek has been updated Successfully"})


##to delete the trek
@app.route('/api/doDeleteTrek',methods=['DELETE'])
def doDeleteTrekApi():

    trekId=request.json["trekId"]

    token=request.json['token'] or None
    userId=_validate_token(token)
    if userId == 0:
        return jsonify({"message":"Please enter a valid token" })
   
    cursor = mysql.connection.cursor()
    resp=cursor.execute('''DELETE from `trek_destinations` WHERE `id`=%s and `user_id`=%s ;''',(trekId,userId))
    if resp==0:
        return jsonify({"message":"you cannot delete someone else's trek"})
   

    
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message":"Trek has been deleted Successfully"})
    
    """
