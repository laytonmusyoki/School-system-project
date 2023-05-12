from flask import Flask,redirect,render_template,flash,request,url_for,session
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
import re
app=Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='laytonmatheka7@gmail.com'
app.config['MAIL_PASSWORD']='qamfnggyldkpbhje'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

app.secret_key="layton"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="school_system"
mysql=MySQL(app)


@app.route('/')
def index():
    return render_template('index.html',title="Home")


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['uname']
        email=request.form['email']
        password=request.form['password']
        img=request.form['image']
        if name=='' or username=='' or email=='' or password==''or img=='':
            flash("All fields are required....",'error')        
        elif len(password) < 6:
            flash("password must be more than 8 characters!",'error')
            return render_template('register.html', name=name, username=username, email=email,password=password)
        elif not re.search("[a-z]", password):
            flash("password must have small letters!",'error')
            return render_template('register.html', name=name, username=username, email=email,password=password)
        elif not re.search("[A-Z]", password):
            flash("password must have capital letters!",'error')
            return render_template('register.html', name=name, username=username, email=email,password=password)
        elif not re.search("[_@$]+", password):
          flash("Password must contain special characters!",'error')
          return render_template('register.html', name=name, username=username, email=email, password=password)
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(img,name, username, email, password) VALUES(%s, %s,%s, %s, %s)",(img,name, username, email, password))
            mysql.connection.commit()
            cur.close()
            flash("Account created successfully",'success')
            return redirect(url_for('login'))
    else:
        return render_template('register.html',title="Register")
    return render_template('register.html',title="Register")



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT *FROM users WHERE username=%s AND password=%s",(username,password))
        result=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result is not None:
            session['loggedin']=True
            session['username']=result[3]
            session['user_id']=result[0]
            return redirect(url_for('dashboard'))
        else:
           flash("Invalid username or password !!",'error')
           return render_template('login.html',username=username,password=password)
    return render_template('login.html',title="login")



@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html',title="Dashboard",username=session['username'])



@app.route('/student', methods=['POST', 'GET'])
def student():
    if 'username' not in session:
        return redirect(url_for('login'))
         
    if request.method == 'POST':
        adm = request.form['adm']
        name = request.form['name']
        email = request.form['email']
        clas = request.form['class']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student(adm,name,email,class) VALUES(%s,%s,%s,%s)",(adm, name, email, clas))
        mysql.connection.commit()
        cur.close()
        flash("Student added successfully", 'success')
        return redirect(url_for('student'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    students = cur.fetchall()
    cur.close()
    return render_template('student.html', title="Student", username=session['username'], students=students)

@app.route('/delete/<id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%s",(id,))
    mysql.connection.commit()
    cur.close()
    flash('Student deleted successfully','error')
    return redirect(url_for('student'))

@app.route('/update/<id>',methods=['POST','GET'])
def update(id):
    if 'username' not in session:
        return redirect(url_for('login'))   
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE id=%s", (id,))
        data = cur.fetchone()
        mysql.connection.cursor()
        cur.close()
        if request.method == 'POST':
           adm = request.form['adm']
           name = request.form['name']
           email = request.form['email']
           clas = request.form['clas']
           cur = mysql.connection.cursor()
           cur.execute("UPDATE student SET adm=%s, name=%s, email=%s,class=%s WHERE id=%s", (adm, name, email, clas, id))
           mysql.connection.commit()
           cur.close()
           flash("information updated successfully", "success")
           return redirect(url_for("student"))
    return render_template('update.html',title="Update", adm=data[1],name=data[2],email=data[4],clas=data[3])





@app.route('/classmanager', methods=['POST','GET'])
def classmanager():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        class_no = request.form['class_no']
        name = request.form['name']
        teacher = request.form['teacher']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO class(class_no,class_name,class_teacher) VALUES(%s,%s,%s)",(class_no, name, teacher))
        mysql.connection.commit()
        cur.close()
        flash("Class added successfully", 'success')
        return redirect(url_for('classmanager'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM class")
    classes = cur.fetchall()
    cur.close()
    return render_template('class.html',title="Class",username=session['username'],classes=classes)


@app.route('/deletee/<id>')
def deletee(id):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM class WHERE id=%s",(id,))
    mysql.connection.commit()
    cur.close()
    flash('Class deleted successfully','error')
    return redirect(url_for('classmanager'))




@app.route('/updatee/<id>',methods=['POST','GET'])
def updatee(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM class WHERE id=%s", (id,))
        datta = cur.fetchone()
        mysql.connection.cursor()
        cur.close()
        if request.method == 'POST':
           class_no = request.form['class_no']
           name = request.form['name']
           teacher = request.form['teacher']
           cur = mysql.connection.cursor()
           cur.execute("UPDATE class SET class_no=%s, class_name=%s,class_teacher=%s WHERE id=%s", (class_no, name, teacher, id))
           mysql.connection.commit()
           cur.close()
           flash("information updated successfully", "success")
           return redirect(url_for("classmanager"))
    return render_template('update_class.html',title="Class update", class_no=datta[1],name=datta[2],teacher=datta[3])



@app.route('/resultmanager',methods=['POST','GET'])
def resultmanager():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        if request.method=='POST':
            name=request.form['name']
            adm=request.form['adm']
            clas=request.form['class']
            maths=float(request.form['maths'])
            eng=float(request.form['eng'])
            kisw=float(request.form['kisw'])
            chem=float(request.form['chem'])
            scie=float(request.form['scie'])
            humanities=float(request.form['humanities'])
            tech=float(request.form['tech'])
            french=float(request.form['french'])

            name=name
            adm=adm
            total=maths+eng+kisw+chem+scie+humanities+tech+french
            average=float(total/8)
            if average >85:
                return render_template('results.html',grade="A",remark="Excellent", total=total,name=name,average=average,adm=adm,clas=clas,title="Results",username=session['username'])
            elif average >79 :
                return render_template('results.html',grade="A-",remark="Excellent",total=total,name=name,average=average,adm=adm,clas=clas,title="Results",username=session['username'])
            elif average >74 :
                return render_template('results.html',grade="B+",remark="Very good",total=total,name=name,average=average,adm=adm,clas=clas,title="Results",username=session['username'])
            elif average >69 :
                return render_template('results.html',grade="B",remark="Very good",total=total,name=name,average=average,adm=adm,clas=clas,title="Results",username=session['username'])
            elif average >64 :
                return render_template('results.html',grade="B-",remark="Good",total=total,name=name,average=average,adm=adm,clas=clas,title="Results",username=session['username'])
            elif average >59 :
                return render_template('results.html',grade="C+",remark="Sactifactory",total=total,name=name,average=average,title="Results",adm=adm,clas=clas,username=session['username'])
            elif average >54 :
                return render_template('results.html',grade="C",remark="Below average",total=total,name=name,average=average,title="Results",adm=adm,clas=clas,username=session['username'])
            elif average >49 :
                return render_template('results.html',grade="C-",remark="Below average",total=total,name=name,average=average,adm=adm,clas=clas,username=session['username'])
            elif average >44 :
                return render_template('results.html',grade="D+",remark="Below average",total=total,name=name,average=average,title="Results",adm=adm,clas=clas,username=session['username'])
            elif average >39 :
                return render_template('results.html',grade="D",remark="Below average",total=total,name=name,average=average,title="Results",adm=adm,clas=clas,username=session['username'])
            elif average >34 :
                return render_template('results.html',grade="D-",remark="Below average",total=total,name=name,average=average,title="Results",adm=adm,clas=clas,username=session['username'])
            else:
                return render_template('results.html',grade="E",remark="Below average",total=total,name=name,average=average,adm=adm,clas=clas)
    return render_template('results.html',title="Results",username=session['username'])


@app.route('/mails', methods=['POST', 'GET'])
def mails():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM student WHERE class=%s", (name,))
        result = cur.fetchall()
        email = [row[0] for row in result]
        msg = Message(subject=subject, sender="laytonmatheka7@gmail.com", recipients=email)
        msg.body = message
        mail.send(msg)
        cur.close()
        flash('message send successfully','success')
    else:
        flash('No message send yet','error')
    return render_template('mails.html', title="mails", username=session['username'])
 
@app.route('/subject',methods=['POST','GET'])
def subject():
    if 'username'not in session:
        return redirect(url_for('login'))

    if request.method=='POST':
        code=request.form['code']
        subject=request.form['subject']

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO subject(code,subject)VALUES(%s,%s)",(code,subject))
        mysql.connection.commit()
        cur.close()
        flash('subject added successfully','success')

    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM subject")
    subjects=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('subject.html',title="subject",username=session['username'],subjects=subjects)


@app.route('/setting',methods=['POST','GET'])
def setting():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method=='POST':
            user_id=session['user_id']
            name=request.form['name']
            username=request.form['username']
            email=request.form['email']
            password=request.form['password']
            img=request.form['image']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET img=%s,name=%s,username=%s,email=%s,password=%s WHERE id=%s",(img,name,username,email,password,user_id,))
            mysql.connection.commit()
            cur.close()
            flash('Information updated successfully','success')
        user_id=session['user_id']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s",(user_id,))
        mysql.connection.commit()
        user=cur.fetchone()
        cur.close()
        return render_template('setting.html',name=user[2],img=user[1],username=user[3],email=user[4],password=user[5],title="setting")

    return render_template('setting.html',title="setting",username=session['username'])


@app.route('/staffportal')
def staffportal():
    if 'username' not in session:
        return redirect(url_for('login'))

    else:
        user_id=session['user_id']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM reports WHERE user_id=%s",(user_id,))
        mysql.connection.commit()
        report=cur.fetchall()
        cur.close()
        return render_template('staff.html',title="staff portal",username=session['username'], report=report )
    return render_template('staff.html',title="staff portal",username=session['username'])


@app.route('/add',methods=['POST','GET'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method=='POST':
        name=request.form['name']
        clas=request.form['class']
        subject=request.form['subject']
        term=request.form['term']
        report=request.form['report']
        dates=request.form['date']
        user_id=session['user_id']

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO reports(user_id,name,clas,subject,term,report,dates)VALUES(%s,%s,%s,%s,%s,%s,%s) ",(user_id,name,clas,subject,term,report,dates))
        mysql.connection.commit()
        cur.close()
        flash('Report updated successfully','success')
        return redirect(url_for('staffportal'))
    return render_template('report.html',title="Add",username=session['username'])

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('loggedin',None)
        session.pop('username',None)
        session.pop('user_id',None)
        flash("You have been logged out",'error')
        return redirect(url_for('login'))



if __name__=='__main__':
    app.run(debug=True)