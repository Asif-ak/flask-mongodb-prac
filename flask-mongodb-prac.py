from flask import Flask,request,jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME']='testsaylani'
app.config['MONGO_URI']='mongodb://testuser:testuser@ds223578.mlab.com:23578/testsaylani'

mongo=PyMongo(app)


@app.route('/')
def hello_world():
    return 'Hello Flask App!'

@app.route('/add',methods=['GET','POST'])
def Add():
    if request.method=="POST":
        user=request.form['user']
        email=request.form['email']
        password=request.form['pass']
        record=mongo.db.Students.insert({'user':user,'email':email,'pass':password})
        return "SAVED"
    else:
        return '''
        <form method="post">
        <h2>Add New Student</h2>
        <input type="text" name="user">
        <input type="email" name="email">
        <input type="password" name="pass">
        <input type="submit" value="Save">
        </form>
        '''
@app.route('/view',methods=['GET','POST'])
def ViewOne():
    if request.method=="POST":
        search=request.form['user']
        students=[]
        records=mongo.db.Students.find({'user':search})
        for student in records:
            students.append({'user':student['user'],'email':student['email'],'pass':student['pass']})
        return jsonify({'AllData':students})
    else:
        return '''
                <form method="post">
                <h2>Search Student</h2>
                <input type="text" name="user">
                <input type="submit" value="Search">
                </form>
                '''


@app.route('/viewall', methods=['GET'])
def ViewAll():
    students = []
    records = mongo.db.Students.find()
    for student in records:
        students.append({'user': student['user'], 'email': student['email'], 'pass': student['pass']})
    return jsonify({'AllData': students})


@app.route('/remove', methods=['GET','POST'])
def RemoveSelected():
    if request.method=="POST":
        search=request.form['user']
        remove=mongo.db.Students.delete_one({'user':search})
        return "Removed: "+ search
    else:
        return '''
        <form method="post">
        <h2>Delete Student</h2>
        <input type="text" name="user">
        <input type="submit" value="Delete">
        </form>
        '''

@app.route('/update', methods=['GET','POST'])
def Update():
    if request.method=="POST":
        search=request.form['email']
        user = request.form['user']
        password = request.form['pass']
        update=mongo.db.Students.find_one_and_update({'email':search},{"$set":{'user':user,'pass':password}},upsert=False) #upsert true will include document if NOT found so false

        return "Updated: "+search
    else:
        return '''
        <form method="post">
        <h2>Update Student</h2>
        <input type="email" name="email">
        <br/>
        <input type="text" name="user">
        <input type="password" name="pass">
        <input type="submit" value="Update">
        </form>
        '''


app.run(debug=True)
