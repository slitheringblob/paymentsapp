from flask_wtf import FlaskForm
from wtforms import (StringField,TextAreaField,SubmitField,PasswordField,DateField,SelectField,IntegerField,DecimalField)
from wtforms.validators import (DataRequired,Email,EqualTo,Length,URL)


################################# Add Classes ########################################################################################################

class add_po_form(FlaskForm):

	resource_name = StringField('Resource Name',validators=[DataRequired()])
	po_vendor = StringField('Vendor',validators = [DataRequired()])
	month = StringField('Month', validators = [DataRequired()])
	noofdays = DecimalField('No Of Days', validators = [DataRequired()])
	leavestaken = DecimalField('Leaves Taken',validators = [DataRequired()])
	billeddays = DecimalField('Billed Days',validators = [DataRequired()])
	billingrate = DecimalField('Billing Rate',validators = [DataRequired()])
	billableamount = DecimalField('Billable Amount', validators = [DataRequired()])
	gst = DecimalField('GST@18%' , validators = [DataRequired()])
	total = DecimalField('Total',validators = [DataRequired()])
	fpn = StringField('FPN',validators = [DataRequired()])
	porf = StringField('PORF',validators = [DataRequired()])
	project = StringField('Project',validators = [DataRequired()])
	date_raised = DateField('Date Raised',format='%d-%m-%Y',validators = [DataRequired()])
	pono = StringField('PO Number')
	invoice_no = StringField('Invoice Number')
	golive_date = DateField('Go live Date',format='%d-%m-%Y')
	add_po = SubmitField('Add PO')

class add_employee_form(FlaskForm):

	emp_code = StringField('Employee Code',validators = [DataRequired()])
	emp_name = StringField('Employee Name',validators = [DataRequired()])
	vendor = SelectField('Vendor',validators = [DataRequired()],choices = [('Saksoft','saksoft'),('Clover','clover'),('MindCraft','mindcraft')])
	joining_date  = DateField('Joining Date',format='%d-%m-%Y',validators = [DataRequired()])
	rate = DecimalField('Rate',validators = [DataRequired()])
	status = SelectField('Status',validators = [DataRequired()],choices = [('Active','active'),('Inactive','inactive')])
	manager = StringField('Manager Emp Code',validators = [DataRequired()])
	add_emp = SubmitField('Add Employee')

class add_fpn_form(FlaskForm):
	fpn = StringField('FPN',validators = [DataRequired()])
	fpn_description = StringField('FPN Description',validators = [DataRequired()])
	resource_duration = StringField('Resource Duration',validators = [DataRequired()])
	amount = StringField('Amount',validators = [DataRequired()])
	vendor = StringField('Vendors',validators = [DataRequired()])
	opening_balance = DecimalField('Opening Balance',validators = [DataRequired()])
	remaining_amount = DecimalField('Opening Balance',validators = [DataRequired()])
	go_live = StringField('Go Live Date')
	remarks = StringField('Remarks', validators = [DataRequired()])
	add_fpn = SubmitField('Add FPN')

class add_holiday_form(FlaskForm):

	date = DateField('Holiday Date(dd-mm-yyyy)',format='%d-%m-%Y',validators = [DataRequired()])
	reason = StringField('Holiday Reason',validators = [DataRequired()])
	add_holiday = SubmitField('Add Holiday')

################################## View Classes #####################################################################################################

class view_po_form(FlaskForm):

	view_po_pono = StringField('PO Number')
	view_po_porf = StringField('PORF')
	view_po_fpn = StringField('FPN')
	view_po_invoice_no = StringField('Invoice Number')
	view_po_submit = SubmitField("View List")

class view_fpn_form(FlaskForm):
	view_fpn_fpn = StringField('FPN')
	view_fpn_submit = SubmitField('View List')

class view_employee_form(FlaskForm):
	view_emp_code = StringField('Employee Code',validators = [DataRequired()])
	view_emp_name = StringField('Employee Name',validators = [DataRequired()])
	view_emp_submit = SubmitField('View List')

#view holiday will just be a list that is directly rendered over the layout by jinja.
#class view_holiday_form(FlaskForm):

#####################################################################################################################################################