from multiprocessing import connection
import pickle
from flask import Flask,render_template,redirect,session,url_for,request
from flask_mysqldb import MySQL
import MySQLdb
import sklearn


app= Flask(__name__)
app.secret_key="12345"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="AKther123%"
app.config["MYSQL_DB"]="hinadb"

db=MySQL(app)

@app.route('/',methods=['Get','POST'])
def index():
    return render_template("login.html")


@app.route('/profile',methods=['Get','POST'])
def login():
    if request.method == 'POST':
        print('request.form',request.form)
        if 'email' in request.form and 'password' in request.form:
            email=request.form['email']
            password=request.form['password']

            #creating a cursor to execute queries on db
            cursor=db.connection.cursor()
            cursor.execute("SELECT * from login2 WHERE email=%s AND password=%s",(email,password))

            info=cursor.fetchone()
            print("info - " ,info)
            if info:
                return render_template("profile.html")

            else:
                return("Login Unsuccessful")
    


@app.route('/new',methods=['Get','POST'])
def register():
    if request.method == 'POST':
        if "email" in request.form and "password" in request.form and "SecretKey" in request.form:

            
            email = request.form['email']

            password = request.form['password']

            SecretKey = request.form['SecretKey']

            print(email,password,SecretKey)

            cursor = db.connection.cursor()
            print(cursor)

            cursor.execute('INSERT INTO login2 VALUES (NULL,%s,%s,%s)', (email, password, SecretKey))
            #cursor.commit()
            db.connection.commit()

           

        
            return render_template("login.html")

    return render_template('register.html')

@app.route('/final',methods=['POST'])
def final():
    data= [
    float(request.form['Longitude']),
    float(request.form['Latitude']),
    float(request.form['Housing Median Age']),
    float(request.form['Total Rooms']),
    float(request.form['Total Bedrooms']),
    float(request.form['Population']),float(request.form['Households']),
    float(request.form['Median Income'])]
    print(data)
    loaded_model = pickle.load(open('model.pkl', 'rb'))
    pred=loaded_model.predict([data])
    print(pred)
    return render_template('final.html',pred=pred[0][0],Longitude=request.form['Longitude'],Latitude=request.form['Latitude'],Housing_Median_Age=request.form['Housing Median Age'],Total_Rooms=request.form['Total Rooms'],Total_Bedrooms=request.form['Total Bedrooms'],Population=request.form['Population'],Households=request.form['Households'],Median_Income=request.form['Median Income'])









#Create API for register
#get secret key fromm request.form
#Change selecct command to Insert command and execute using cursor
#Once data is inserted (Cursor.execute is successful) then open profile page

if __name__=='__main__' :
    app.run(debug=True)