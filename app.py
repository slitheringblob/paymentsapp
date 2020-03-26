from flask import Flask,render_template,redirect,url_for,request,session,flash,g
from functools import wraps
import sqlite3


app=Flask(__name__)

app.secret_key= "my precious"
app.database = "/db/vpt.db"

################################login required decorator ####################################

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
############################################################################################# 
##############################################    ROUTES    #################################

@app.route('/')
@login_required
def hello():
	

	g.db = connect_db()
	return render_template("index.html")
	

@app.route('/home')
def home():
	return render_template("home.html")

@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method=='POST':
		if request.form['username']!='admin' or request.form['password']!='Pinkfloyd890!':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('You were just logged in!')
			return redirect(url_for('home'))

	return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You were just logged Out!')
	return redirect(url_for('login'))

####################################### END ROUTES ##########################################################################

def connect_db():
    conn = None
    try:
        conn = sqlite3.connect(app.database)
        print("Connection Established")
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)



if __name__=='__main__':
	app.run(debug=True)

