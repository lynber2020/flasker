
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
# import MySQLdb


# Create Flask
app = Flask(__name__)
# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:LynBer01@localhost/our_users'


#secret key
app.config['SECRET_KEY'] = " my little secret"
#initialize database
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LynBer01'
app.config['MYSQL_DB'] = 'owner_db'

mysql = MySQL(app)



@app.route('/')
def Index2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM tbltaxdec")
    data = cur.fetchall()
    cur.close()




    return render_template('index2.html', tbltaxdec=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        TC = request.form['TC']
        LastName = request.form['LastName']
        FirstName = request.form['FirstName']
        MiddleName = request.form['MiddleName']
        TDN = request.form['TDN']
        PIN = request.form['PIN']
        Sitio = request.form['Sitio']
        Barangay = request.form['Barangay']
        Kind = request.form['Kind']
        Class = request.form['Class']
        Class2 = request.form['Class2']
        Area = request.form['Area']
        Area2 = request.form['Area2']
        MV = request.form['MV']
        MV2 = request.form['MV2']
        AV = request.form['AV']
        AV2 = request.form['AV2']
        ClassCode = request.form['ClassCode']
        LotNo = request.form['LotNo']
        TitleNo = request.form['TitleNo']
        LegalBasis = request.form['LegalBasis']
        Effectivity = request.form['Effectivity']
        Remarks = request.form['Remarks']
        PrevOwner = request.form['PrevOwner']
        PrevTDN = request.form['PrevTDN']
        PrevArea = request.form['PrevArea']
        PrevMV = request.form['PrevMV']
        PrevAV = request.form['PrevAV']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbltaxdec (TC, LastName, FirstName, MiddleName, TDN, PIN, Sitio, Barangay, Kind, Class, Class2, Area, Area2, MV, MV2, AV, AV2, ClassCode, LotNo, TitleNo, LegalBasis, Effectivity, Remarks, PrevOwner, PrevTDN, PrevArea, PrevMV, PrevAV) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (TC, LastName, FirstName, MiddleName, TDN, PIN, Sitio, Barangay, Kind, Class, Class2, Area, Area2, MV, MV2, AV, AV2, ClassCode, LotNo, TitleNo, LegalBasis, Effectivity, Remarks, PrevOwner, PrevTDN, PrevArea, PrevMV, PrevAV))
        mysql.connection.commit()
        return redirect(url_for('Index2'))




@app.route('/delete/<string:RPID_data>', methods = ['GET'])
def delete(RPID_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbltaxdec WHERE RPID=%s", (RPID_data,))
    mysql.connection.commit()
    return redirect(url_for('Index2'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        RPID_data = request.form['RPID']
        TC = request.form['TC']
        LastName = request.form['LastName']
        FirstName = request.form['FirstName']
        MiddleName = request.form['MiddleName']
        TDN = request.form['TDN']
        PIN = request.form['PIN']
        Sitio = request.form['Sitio']
        Barangay = request.form['Barangay']
        Kind = request.form['Kind']
        Class = request.form['Class']
        Class2 = request.form['Class2']
        Area = request.form['Area']
        Area2 = request.form['Area2']
        MV = request.form['MV']
        MV2 = request.form['MV2']
        AV = request.form['AV']
        AV2 = request.form['AV2']
        ClassCode = request.form['ClassCode']
        LotNo = request.form['LotNo']
        TitleNo = request.form['TitleNo']
        LegalBasis = request.form['LegalBasis']
        Effectivity = request.form['Effectivity']
        Remarks = request.form['Remarks']
        PrevOwner = request.form['PrevOwner']
        PrevTDN = request.form['PrevTDN']
        PrevArea = request.form['PrevArea']
        PrevMV = request.form['PrevMV']
        PrevAV = request.form['PrevAV']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE tbltaxdec
               SET TC=%s, LastName=%s, FirstName=%s, MiddleName=%s, TDN=%s, PIN=%s, Sitio=%s, Barangay=%s, Kind=%s, Class=%s, Class2=%s, Area=%s, Area2=%s, MV=%s, MV2=%s, AV=%s, AV2=%s, ClassCode=%s, LotNo=%s, TitleNo=%s, LegalBasis=%s, Effectivity=%s, Remarks=%s, PrevOwner=%s, PrevTDN=%s, PrevArea=%s, PrevMV=%s, PrevAV=%s
               WHERE RPID=%s
            """, (TC, LastName, FirstName, MiddleName, TDN, PIN, Sitio, Barangay, Kind, Class, Class2, Area, Area2, MV, MV2, AV, AV2, ClassCode, LotNo, TitleNo, LegalBasis, Effectivity, Remarks, PrevOwner, PrevTDN, PrevArea, PrevMV, PrevAV, RPID_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index2'))









if __name__ == "__main__":
    app.run(debug=True)