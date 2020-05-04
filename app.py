from flask import Flask,render_template,redirect,url_for,request,session,flash,g
from functools import wraps
import sqlite3
from forms import add_po_form,add_holiday_form,add_employee_form,add_fpn_form


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
	pass

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
	#conn = connect_db()
	return render_template("dashboard.html")

@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method=='POST':
		if request.form['username']!='admin' or request.form['password']!='Pinkfloyd890!':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			# flash('You were just logged in!')
			return redirect(url_for('dashboard'))

	return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You were just logged Out!')
	return redirect(url_for('login'))

######################### Add_Functionality Routes ########################

@app.route('/addnewpo',methods=['GET','POST'])
@login_required
def addnewpo():
	error = None
	form = add_po_form()

	if form.validate_on_submit():
		flash(f'Added PO for {form.porf.data}!', 'success')
		return redirect(url_for('dashboard'))


	return render_template("add_new_po.html",error=error,title = 'Add New PO',form = form)


@app.route('/addnewholiday',methods=['GET','POST'])
@login_required
def addnewholiday():
	error = None
	form = add_holiday_form()
	print(form.errors)

	if form.validate_on_submit():
		flash(f'Added New Holiday for {form.reason.data} on {form.date.data}!', 'success')
		print('validated holiday')
		return redirect(url_for('dashboard'))
	else:
		print(form.errors)		
		print('invalid holiday')

	return render_template("add_new_holiday.html",error=error,title = 'Add New Holiday',form = form)


@app.route('/addnewfpn',methods=['GET','POST'])
@login_required
def addnewfpn():
	error = None
	form = add_fpn_form()
	if form.validate_on_submit():
		flash(f'Added new FPN for {form.fpn.data} and {form.opening_balance.data}!', 'success')
		return redirect(url_for('dashboard')) 


	return render_template("add_new_fpn.html",error=error,title = 'Add New FPN',form = form)

@app.route('/addnewemployee',methods=['GET','POST'])
@login_required
def addnewemployee():
	error = None
	form = add_employee_form()

	if form.validate_on_submit():
		flash(f'Added Employee {form.emp_code.data}!', 'success')
		return redirect(url_for('dashboard'))


	return render_template("add_new_employee.html",error=error,title = 'Add New Employee',form = form)


####################################### END ROUTES ##########################################################################

def connect_db():
	conn = sqlite3.connect(app.database)
	print("Connection Established")
	print(sqlite3.version)
	return conn



if __name__=='__main__':
	app.run(debug=True)

