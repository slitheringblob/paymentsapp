from flask import Flask,render_template,redirect,url_for,request,session,flash,g
from functools import wraps
import sqlite3
from forms import add_po_form,add_holiday_form,add_employee_form,add_fpn_form
from forms import view_po_form,view_fpn_form,view_employee_form


app=Flask(__name__)

app.secret_key= "my precious"
database = "C:/Users/jayde/Documents/GitHub/paymentsapp/db/vpt.db"

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

######################### Add_Functionality Routes #######################################################################################################

@app.route('/addnewpo',methods=['GET','POST'])
@login_required
def addnewpo():
	error = None
	form = add_po_form()
	conn = connect_db()
	print(form.errors)

	if form.validate_on_submit():
		c = conn.cursor()

		resource_name = form.resource_name.data
		po_vendor = form.po_vendor.data
		month = form.month.data
		noofdays = form.noofdays.data
		leavestaken = form.leavestaken.data
		billeddays = form.billeddays.data
		billingrate = form.billingrate.data
		billableamount = form.billableamount.data
		gst = form.gst.data
		total = form.total.data
		fpn = form.fpn.data
		porf = form.porf.data
		project = form.project.data
		date_raised = form.date_raised.data
		pono = form.pono.data
		invoice_no = form.invoice_no.data
		golive_date = form.golive_date.data
		
		c.execute("INSERT INTO MS_PO_MASTER VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(resource_name,po_vendor,month,noofdays,leavestaken,billeddays,billingrate,billableamount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date,))
		conn.commit()
		conn.close()

		print('validated form')
		flash(f'Added PO for PORF:{porf}!', 'success')
		return redirect(url_for('dashboard'))
	else:
		print(form.errors)
		print('invalid form')

	return render_template("add_new_po.html",error=error,title = 'Add New PO',form = form)


@app.route('/addnewholiday',methods=['GET','POST'])
@login_required
def addnewholiday():
	error = None
	form = add_holiday_form()

	date = form.date.data
	reason = form.reason.data


	print(form.errors)
	conn = connect_db()
	if form.validate_on_submit():
		c = conn.cursor()
		c.execute("INSERT INTO MS_HOLIDAY_MASTER VALUES(?,?)",(date,reason,))

		flash(f'Added New Holiday for {reason} on {date} !', 'success')
		print('validated holiday')
		conn.commit()
		conn.close()

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
##################################### View_fucntionality Routes##############################################################

@app.route('/viewpo',methods = ['GET','POST'])
@login_required
def viewpo():
	error = None
	form = view_po_form()

	return render_template("view_po.html",error = error,title = 'View PO',form=form)

@app.route('/viewfpn',methods = ['GET','POST'])
@login_required
def viewfpn():
	error = None
	form = view_fpn_form()

	return render_template("view_fpn.html",error = error,title = 'View FPN',form=form)

@app.route('/viewemployee',methods = ['GET','POST'])
@login_required
def viewemployee():
	error = None
	conn = connect_db()
	c = conn.cursor()
	c.execute("select * from MS_EMP_MASTER")
	rows = c.fetchall()


	return render_template("view_employee.html",error = error,title = 'View Employee',rows = rows)

@app.route('/viewholiday',methods = ['GET','POST'])
@login_required
def viewholiday():
	error = None
	conn = connect_db()
	c = conn.cursor()
	c.execute("select * from MS_HOLIDAY_MASTER")
	rows = c.fetchall()

	return render_template("view_holiday.html",error = error,title = 'View Holiday',rows = rows)


####################################### END ROUTES ##########################################################################

def connect_db():
	conn = sqlite3.connect(database)
	print("Connection Established")
	print(sqlite3.version)
	return conn



if __name__=='__main__':
	app.run(debug=True)

