from flask import Flask,render_template,redirect,url_for,request,session,flash
from functools import wraps
import sqlite3
from forms import add_po_form,add_holiday_form,add_employee_form,add_fpn_form
from forms import view_po_form,view_fpn_form
from forms import update_po_search_form,update_employee_search_form,update_fpn_search_form


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

#############################################################################################p;i
##############################################    ROUTES    #################################

@app.route('/')
@login_required
def hello():

	error = "Invalid route. Go to /login"
	return render_template('login.html',error=error)

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
		
		c.execute("INSERT INTO MS_PO_MASTER(resource_name,po_vendor,month,noofdays,leavestaken,billeddays,billingrate,billableamount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(resource_name,po_vendor,month,noofdays,leavestaken,billeddays,billingrate,billableamount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date,))
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
		c.execute("INSERT INTO MS_HOLIDAY_MASTER(date,reason) VALUES(?,?)",(date,reason,))

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
	conn = connect_db()
	if form.validate_on_submit():
		c = conn.cursor()

		fpn = form.fpn.data
		fpn_description = form.fpn_description.data
		resource_duration = form.resource_duration.data
		amount = form.amount.data
		vendor = form.vendor.data
		opening_balance = form.opening_balance.data
		amount_utilized = form.amount_utilized.data
		remaining_amount = form.remaining_amount.data
		go_live = form.go_live.data
		remarks = form.remarks.data
		

		c.execute("INSERT INTO MS_FPN_MASTER(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks) VALUES(?,?,?,?,?,?,?,?,?,?)",(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks,))
		conn.commit()
		conn.close()

		print('validated form')
		flash(f'Added FPN:{fpn}!', 'success')
		return redirect(url_for('dashboard'))
	else:
		print(form.errors)
		print('invalid form')

	return render_template("add_new_fpn.html",error=error,title = 'Add New FPN',form = form)

@app.route('/addnewemployee',methods=['GET','POST'])
@login_required
def addnewemployee():
	error = None
	form = add_employee_form()
	conn = connect_db()
	
	if form.validate_on_submit():

		c = conn.cursor()
		emp_code = form.emp_code.data
		emp_name = form.emp_name.data
		vendor = form.vendor.data
		joining_date  = form.joining_date.data
		rate = form.rate.data
		status = form.status.data
		manager = form.manager.data

		# print("DATA TYPE OF JOINING DATE:",type(joining_date))
		# print("DATA TYPE OF RATE:",type(rate))
		
		c.execute("INSERT INTO MS_EMP_MASTER(emp_code,emp_name,vendor,joining_date,rate,status,manager) VALUES(?,?,?,?,?,?,?)",(emp_code,emp_name,vendor,joining_date,rate,status,manager,))
		conn.commit()
		conn.close()
		
		flash(f'Added Employee {form.emp_code.data}!', 'success')
		return redirect(url_for('dashboard'))


	return render_template("add_new_employee.html",error=error,title = 'Add New Employee',form = form)
##################################### View_fucntionality Routes##############################################################

@app.route('/viewpo',methods = ['GET','POST'])
@login_required
def viewpo():
	error = None
	# form = view_po_form()

	# pono = form.view_po_pono.data
	# porf = form.view_po_porf.data
	# fpn = form.view_po_fpn.data
	# invoice_no = form.view_po_invoice_no.data

	# conn = connect_db()
	# c = conn.cursor()

	# if form.validate_on_submit():

	# 	if pono=="" and porf=="" and fpn=="" and invoice_no=="":
	# 		return render_template("view_po.html",error = error,title = 'View PO',form=form)
		
	# 	if pono=="" and porf=="" and fpn=="":
	# 		c.execute("select * from MS_PO_MASTER WHERE invoice_no=?",(invoice_no,))
	# 		rows = c.fetchall()
	# 		return render_template("view_po_results.html",error = error,title = 'Search Results',form=form,rows = rows)

	# 	if pono=="" and porf=="" and invoice_no=="":
	# 		c.execute("select * from MS_PO_MASTER WHERE fpn=?",(fpn,))
	# 		rows = c.fetchall()
	# 		return render_template("view_po_results.html",error = error,title = 'Search Results',form=form,rows = rows)

	# 	if pono=="" and invoice_no=="" and fpn=="":
	# 		c.execute("select * from MS_PO_MASTER WHERE porf=?",(porf,))
	# 		rows = c.fetchall()
	# 		return render_template("view_po_results.html",error = error,title = 'Search Results',form=form,rows = rows)

	# 	if invoice_no=="" and porf=="" and fpn=="":
	# 		c.execute("select * from MS_PO_MASTER WHERE pono=?",(pono,))
	# 		rows = c.fetchall()
	# 		return render_template("view_po_results.html",error = error,title = 'Search Results',form=form,rows = rows)
	if error==None:
		conn = connect_db()
		c = conn.cursor()
		c.execute("select * from MS_PO_MASTER")
		rows = c.fetchall()

		return render_template("view_po_results.html",error = error,title = "All Raised Purchase Orders",rows = rows)

	
	return render_template("view_po.html",error = error,title = 'View PO',form=form)

@app.route('/viewfpn',methods = ['GET','POST'])
@login_required
def viewfpn():
	# error = None
	# form = view_fpn_form()

	# conn = connect_db()
	# c = conn.cursor()

	# if form.validate_on_submit():
	# 	fpn = form.view_fpn_fpn.data

	# 	c.execute("select * from MS_FPN_MASTER WHERE fpn=?",(fpn,))
	# 	rows = c.fetchall()

	# 	return render_template("view_fpn_results.html",error = error,title = 'Search Results',form=form,rows = rows)
	error = None

	if error==None:
		conn = connect_db()
		c = conn.cursor()
		c.execute("select * from MS_FPN_MASTER")
		rows = c.fetchall()

		return render_template("view_fpn_results.html",error = error,title = '',rows = rows)



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



############################################################### Employees New Code #####################################################################################################################################


@app.route('/employees',methods = ['GET','POST'])
@login_required
def employees():
	conn = connect_db()
	c = conn.cursor()
	c.execute("select * from MS_EMP_MASTER")
	rows = c.fetchall()

	return render_template("employees.html", rows=rows, title="Employees")



@app.route('/updateemployee',methods=['GET','POST'])
@login_required
def updateemployee():
	
	if request.method == "POST":
		emp_code = request.form["emp_code"]
		emp_name = request.form["emp_name"]
		vendor = request.form["vendor"]
		joining_date  = request.form["joining_date"]
		rate = request.form["rate"]
		status = request.form["status"]
		manager = request.form["manager"]

		conn = connect_db()
		c = conn.cursor()

		c.execute("UPDATE MS_EMP_MASTER SET emp_code=?,emp_name=?,vendor=?,joining_date=?,rate=?,status=?,manager=? WHERE emp_code=?",(emp_code,emp_name,vendor,joining_date,rate,status,manager,emp_code,))

		conn.commit()
		conn.close()

	return redirect(url_for('employees'))



@app.route('/addemployee',methods = ['GET','POST'])
@login_required
def addemployee():
	
	if request.method == "POST":

		conn = connect_db()
		c = conn.cursor()
		emp_code = request.form["emp_code"]
		emp_name = request.form["emp_name"]
		vendor = request.form["vendor"]
		joining_date  = request.form["joining_date"]
		rate = request.form["rate"]
		status = request.form["status"]
		manager = request.form["manager"]

		c.execute("INSERT INTO MS_EMP_MASTER(emp_code,emp_name,vendor,joining_date,rate,status,manager) VALUES(?,?,?,?,?,?,?)",(emp_code,emp_name,vendor,joining_date,rate,status,manager,))
		conn.commit()
		conn.close()

	return redirect(url_for('employees'))



#################################################### Holidays new Code #################################################################################

@app.route('/holidays',methods = ['GET','POST'])
@login_required
def holidays():
	conn = connect_db()
	c = conn.cursor()
	c.execute("select * from MS_HOLIDAY_MASTER")
	rows = c.fetchall()

	return render_template("holidays.html", rows=rows, title="Holidays")


@app.route('/addholiday',methods = ['GET','POST'])
@login_required


def addholiday():

	if request.method == 'POST':
		conn = connect_db()
		c = conn.cursor()

		date = request.form["date"]
		reason = request.form["reason"]

		c.execute("INSERT INTO MS_HOLIDAY_MASTER(date,reason) VALUES(?,?)",(date,reason,))
		conn.commit()
		conn.close()

	return redirect(url_for('holidays'))


@app.route('/updateholiday',methods = ['GET','POST'])
@login_required

def updateholiday():

	if request.method == "POST":

		conn = connect_db()
		c = conn.cursor()

		date = request.form["date"]
		reason = request.form["reason"]

		c.execute("UPDATE MS_HOLIDAY_MASTER SET date=?,reason=? WHERE date=?",(date,reason,date,))
		conn.commit()
		conn.close()

	return redirect(url_for('holidays'))

########################################## FPN new Code ##########################################################################

@app.route('/fpn',methods = ['GET','POST'])
@login_required
def fpn():
	conn = connect_db()
	c = conn.cursor()
	c.execute("select * from MS_FPN_MASTER")
	rows = c.fetchall()

	return render_template("fpn.html", rows=rows , title="FPN")


@app.route('/addfpn',methods = ['GET','POST'])
@login_required
def addfpn():

	if request.method == "POST":
		
		conn = connect_db()
		c = conn.cursor()

		fpn = request.form["fpn"]
		fpn_description = request.form["fpn_description"]
		resource_duration = request.form["resource_duration"]
		amount = request.form["amount"]
		vendor = request.form["vendor"]
		opening_balance = request.form["opening_balance"]
		amount_utilized = request.form["amount_utilized"]
		remaining_amount = request.form["remaining_amount"]
		go_live = request.form["go_live"]
		remarks = request.form["remarks"]
		

		c.execute("INSERT INTO MS_FPN_MASTER(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks) VALUES(?,?,?,?,?,?,?,?,?,?)",(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks,))
		conn.commit()
		conn.close()
	return redirect(url_for('fpn'))

@app.route('/updatefpn',methods = ['GET','POST'])
@login_required

def updatefpn():
	 
	if request.method == "POST":
		conn = connect_db()
		c = conn.cursor()

		fpn = request.form["fpn"]
		fpn_description = request.form["fpn_description"]
		resource_duration = request.form["resource_duration"]
		amount = request.form["amount"]
		vendor = request.form["vendor"]
		opening_balance = request.form["opening_balance"]
		amount_utilized = request.form["amount_utilized"]
		remaining_amount = request.form["remaining_amount"]
		go_live = request.form["go_live"]
		remarks = request.form["remarks"]
		c.execute("UPDATE MS_FPN_MASTER SET fpn=?,fpn_description=?,resource_duration=?,amount=?,vendor=?,opening_balance=?,amount_utilized=?,remaining_amount=?,go_live=?,remarks=? WHERE fpn=?",(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks,fpn,))
		conn.commit()
		conn.close()
	return redirect(url_for('fpn'))

#########################################################  PO New Code ############################################################################

@app.route('/po',methods = ['GET','POST'])
@login_required

def po():
	conn = connect_db()
	c = conn.cursor()
	c.execute("select * from MS_PO_MASTER")
	rows = c.fetchall()

	return render_template("po.html", rows=rows , title="PO")

@app.route('/addpo',methods = ['GET','POST'])
@login_required

def addpo():
	
	if request.method == "POST":
		conn = connect_db()
		c = conn.cursor()

		resource_name = request.form["resource_name"]
		po_vendor = request.form["po_vendor"]
		month = request.form["month"]
		noofdays = request.form["noofdays"]
		leavestaken = request.form["leavestaken"]
		billeddays = request.form["billeddays"]
		billingrate = request.form["billingrate"]
		billableamount = request.form["billableamount"]
		gst = request.form["gst"]
		total = request.form["total"]
		fpn = request.form["fpn"]
		porf = request.form["porf"]
		project = request.form["project"]
		date_raised = request.form["date_raised"]
		pono = request.form["pono"]
		invoice_no = request.form["invoice_no"]
		golive_date = request.form["golive_date"]

		
		c.execute("INSERT INTO MS_PO_MASTER(resource_name,po_vendor,month,noofdays,leavestaken,billeddays,billingrate,billableamount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(resource_name,po_vendor,month,noofdays,leavestaken,billeddays,billingrate,billableamount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date,))

	return redirect(url_for('po'))




@app.route('/updatepo', methods = ['GET','POST'])
@login_required

def updatepo():
	if request.method =="POST":

		conn = connect_db()
		c = conn.cursor()

		resource_name = request.form["resource_name"]
		po_vendor = request.form["po_vendor"]
		month = request.form["month"]
		noofdays = request.form["noofdays"]
		leavestaken = request.form["leavestaken"]
		billeddays = request.form["billeddays"]
		billingrate = request.form["billingrate"]
		billableamount = request.form["billableamount"]
		gst = request.form["gst"]
		total = request.form["total"]
		fpn = request.form["fpn"]
		porf = request.form["porf"]
		project = request.form["project"]
		date_raised = request.form["date_raised"]
		pono = request.form["pono"]
		invoice_no = request.form["invoice_no"]
		golive_date = request.form["golive_date"]

		c.execute("UPDATE MS_PO_MASTER SET resource_name=?,po_vendor=?,month=?,noofdays=?,leavestaken=?,billeddays=?,billingrate=?,billableamount=?,gst=?,total=?,fpn=?,porf=?,project=?,date_raised=?,pono=?,invoice_no=?,golive_date=?",(resource_name,po_vendor,month,noofdays,leavestaken,billeddays,billingrate,billableamount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date,))
		conn.commit()
		conn.close()

	return redirect(url_for('po'))






####################################### END ROUTES ##########################################################################


def connect_db():
	conn = sqlite3.connect(database)
	print("Connection Established")
	print(sqlite3.version)
	return conn



if __name__=='__main__':
	app.run(debug=1)

