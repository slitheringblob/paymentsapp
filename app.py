from flask import Flask,render_template,redirect,url_for,request,session,flash,send_file,send_from_directory,safe_join,abort
from functools import wraps
import sqlite3
import os
import datetime
import subprocess
import xlrd
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from forms import add_po_form,add_holiday_form,add_employee_form,add_fpn_form
from forms import view_po_form,view_fpn_form
from forms import update_po_search_form,update_employee_search_form,update_fpn_search_form


app=Flask(__name__)

app.secret_key= "my precious"
database_filepath = "C:/Users/jayde/Documents/GitHub/paymentsapp/db/vpt.db"
app.config['MAX_CONTENT_LENGTH'] = 1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg','.png','.gif','.jpeg','.xls','.xlsx']
UPLOAD_PATH = 'C:\\Users\\jayde\\Documents\\GitHub\\paymentsapp\\uploads\\'


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

################################################################################################
##############################################    ROUTES    #################################

@app.route('/')
@login_required
def hello():

	error = "Invalid route. Go to /login"
	return render_template('login.html',error=error)

##################################################################################################
############################ Dashboard ###########################################################################################
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    conn = connect_db()
    c = conn.cursor()
    username = session.get("USERNAME")
    print("Username:",username)
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August","September","October","November","December"]
    values = [10, 9, 8, 7, 6, 4, 7, 8,1,9,1,5]
    for month in range(1,13):
        print("Month:",month)
        c.execute("SELECT total(total) from MS_PO_MASTER WHERE month=?",(month,))
        total_billable_amount = c.fetchone()[0]
        values[month-1] = total_billable_amount
        print("Monthly Values:",values)
        print("Sum of PO total column:",total_billable_amount)

    return render_template("dashboard.html",values=values, labels=labels, legend=legend,username = username)

########################################################################################################################
################################## Login ###############################################################################
@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method=='POST':
		if request.form['username']!='admin' or request.form['password']!='Pinkfloyd890!':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			session['USERNAME'] = request.form['username']
			# flash('You were just logged in!')
			return redirect(url_for('dashboard'))

	return render_template('login.html',error=error)

########################################################################################################################
################################## LogOut ###############################################################################
@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You were just logged Out!')
	return redirect(url_for('login'))
########################################################################################################################
################################## File Upload ###############################################################################
################# functional route that will be hit ftom the from the template submit button ####################################
@app.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    return render_template('uploadform.html')



@app.route('/uploader',methods=['GET','POST'])
@login_required
def uploader():
    if request.method == "POST":
        f = request.files['input_file']
        filename = secure_filename(f.filename)
        if f.filename !='':
            file_extension = os.path.splitext(filename)[1]
            if file_extension not in app.config['UPLOAD_EXTENSIONS']:
                message_alert = 'Upload Failed'
                return render_template('uploadform.html',message_alert = message_alert)
            else:
                # generate the output path and command string that needs to be executed
                global UPLOAD_PATH
                UPLOAD_PATH = UPLOAD_PATH + datetime.datetime.now().strftime("%d%m%y%H%M")
                os.makedirs(UPLOAD_PATH)
                f.save(os.path.join(UPLOAD_PATH,filename))

                ################################# Parsing the uploaded file to get no of leaves and present days ##############################################################
                fqfp = os.path.join(UPLOAD_PATH,filename) #fully qualified file name
                wb = xlrd.open_workbook(filename=fqfp) #open the workbook
                sheet = wb.sheet_by_index(0) # extract sheet
                day_status = []
                leave_dates = []
                py_dates = []
                present_counter = 0
                for i in range(sheet.nrows):
                    day_status.append(sheet.cell_value(i,6))
                    if day_status[i] == 'Present' or day_status[i] == 'present':
                        present_counter += 1
                    if day_status[i] == 'Leave' or day_status[i] == 'leave':
                        raw_date = sheet.cell_value(i,3)
                        converted_date = xlrd.xldate_as_tuple(raw_date,wb.datemode)
                        print("Converted Date:",converted_date)
                        actual_date = datetime.datetime(*converted_date).strftime("%d/%m/%y")
                        print("Actual Date:",actual_date)
                        leave_dates.append(actual_date)

                message_alert = 'Successfully Uploaded'
                return render_template('uploadform.html',message_alert=message_alert,leave_dates = leave_dates , present_counter = present_counter)
        else:
            message_alert = 'Upload Failed'
            return render_template('uploadform.html',message_alert = message_alert)



############################################################### Employees New Code #####################################################################################################################################


@app.route('/employees',methods = ['GET','POST'])
@login_required
def employees():
    conn = connect_db()
    c = conn.cursor()
    c.execute("select * from MS_EMP_MASTER")
    rows = c.fetchall()
    username = session.get("USERNAME")

    return render_template("employees.html", rows=rows,username = username, title="Employees")



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


@app.route('/deleteemployee/<id>/',methods = ['GET','POST'])
@login_required
def deleteemployee(id):


    conn = connect_db()
    c = conn.cursor()
    #emp_code = request.form["emp_code"]
    print("ID:",id)

    c.execute("DELETE FROM MS_EMP_MASTER WHERE id=?",(id,))
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
    username = session.get("USERNAME")
    return render_template("holidays.html", rows=rows,username = username, title="Holidays")


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
        print("Date and Reason:",date,reason)
        c.execute("UPDATE MS_HOLIDAY_MASTER SET date=?,reason=? WHERE date=?",(date,reason,date,))
        conn.commit()
        conn.close()

    return redirect(url_for('holidays'))

@app.route('/deleteholiday/<id>',methods=['GET','POST'])
@login_required

def deleteholiday(id):
    conn = connect_db()
    c = conn.cursor()

    print("this is the rowID:",str(id))

    c.execute("DELETE FROM MS_HOLIDAY_MASTER WHERE id=?",(id,))
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
    username = session.get("USERNAME")
    return render_template("fpn.html", rows=rows ,username = username, title="FPN")


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
        project = request.form["project"]

        print("project:",project)

        c.execute("INSERT INTO MS_FPN_MASTER(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks,project) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks,project,))
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
        project = request.form["project"]

        #print("Updated Project:",project)
        print("UPDATE MS_FPN_MASTER SET fpn="+fpn+" fpn_description="+fpn_description+" resource_duration="+resource_duration+" project="+project)
        c.execute("UPDATE MS_FPN_MASTER SET fpn=?,fpn_description=?,resource_duration=?,amount=?,vendor=?,opening_balance=?,amount_utilized=?,remaining_amount=?,go_live=?,remarks=?,project=? WHERE fpn=?",(fpn,fpn_description,resource_duration,amount,vendor,opening_balance,amount_utilized,remaining_amount,go_live,remarks,project,fpn,))
        print("No of rows affected: ",c.rowcount)
        conn.commit()
        conn.close()
    return redirect(url_for('fpn'))

@app.route('/deletefpn/<id>',methods=['GET','POST'])
@login_required

def deletefpn(id):
    conn = connect_db()
    c = conn.cursor()

    print("thi is the rowID:",str(id))

    c.execute("DELETE FROM MS_FPN_MASTER WHERE id=?",(id,))
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
    print(rows)
    username = session.get("USERNAME")
    return render_template("po.html",rows=rows,username = username, title="PO")

@app.route('/addpo',methods = ['GET','POST'])
@login_required

def addpo():
    if request.method == "POST":
        conn = connect_db()
        c = conn.cursor()

        resource_name = request.form["resource_name"]
        vendor = request.form["vendor"]
        month = request.form["month"]
        no_of_days = request.form["no_of_days"]
        leaves_taken = request.form["leaves_taken"]
        billed_days = request.form["billed_days"]
        billing_rate = request.form["billing_rate"]
        billable_amount = request.form["billable_amount"]
        gst = request.form["gst"]
        total = request.form["total"]
        fpn = request.form["fpn"]
        porf = request.form["porf"]
        project = request.form["project"]
        date_raised = request.form["date_raised"]
        pono = request.form["pono"]
        invoice_no = request.form["invoice_no"]
        golive_date = request.form["golive_date"]
        c.execute("INSERT INTO MS_PO_MASTER(resource_name,vendor,month,no_of_days,leaves_taken,billed_days,billing_rate,billable_amount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(resource_name,vendor,month,no_of_days,leaves_taken,billed_days,billing_rate,billable_amount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date,))
        conn.commit()
        conn.close()
    return redirect(url_for('po'))




@app.route('/updatepo', methods = ['GET','POST'])
@login_required

def updatepo():
    if request.method =="POST":
        conn = connect_db()
        c = conn.cursor()
        resource_name = request.form["resource_name"]
        vendor = request.form["vendor"]
        month = request.form["month"]
        noofdays = request.form["no_of_days"]
        leavestaken = request.form["leaves_taken"]
        billeddays = request.form["billed_days"]
        billingrate = request.form["billing_rate"]
        billableamount = request.form["billable_amount"]
        gst = request.form["gst"]
        total = request.form["total"]
        fpn = request.form["fpn"]
        porf = request.form["porf"]
        project = request.form["project"]
        date_raised = request.form["date_raised"]
        pono = request.form["pono"]
        invoice_no = request.form["invoice_no"]
        golive_date = request.form["golive_date"]

        c.execute("UPDATE MS_PO_MASTER SET resource_name=?,vendor=?,month=?,no_of_days=?,leaves_taken=?,billed_days=?,billing_rate=?,billable_amount=?,gst=?,total=?,fpn=?,porf=?,project=?,date_raised=?,pono=?,invoice_no=?,golive_date=?",(resource_name,vendor,month,noofdays,leavestaken,billeddays,billingrate,billableamount,gst,total,fpn,porf,project,date_raised,pono,invoice_no,golive_date,))
        conn.commit()
        conn.close()

    return redirect(url_for('po'))

@app.route('/deletepo/<id>',methods=['GET','POST'])
@login_required

def deletepo(id):
    conn = connect_db()
    c = conn.cursor()

    print("thi is the rowID:",str(id))

    c.execute("DELETE FROM MS_PO_MASTER WHERE id=?",(id,))
    conn.commit()
    conn.close()

    return redirect(url_for('po'))


@app.route('/createpo',methods=['GET','POST'])
@login_required

def createpo():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT emp_name from MS_EMP_MASTER")
    employee_list_raw = c.fetchall()
    employee_list=[]

    for employee in employee_list_raw:
        employee_list.append(employee[0])

    return render_template(("create_po.html"),employee_list = employee_list)



####################################### END ROUTES ##########################################################################


def connect_db():
	conn = sqlite3.connect(database_filepath)
	print("Connection Established")
	print(sqlite3.version)
	return conn



if __name__=='__main__':
	app.run(debug=1)
