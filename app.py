from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    pf_no = db.Column(db.String(50))
    esi_no = db.Column(db.String(50))
    nop= db.Column(db.String(50), nullable=False)
    doj = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    ac_no = db.Column(db.String(50))
    ifsc_code = db.Column(db.String(50))
    pan_no = db.Column(db.String(10), nullable=False)
    aadhar_no = db.Column(db.String(12), nullable=False)
    uan = db.Column(db.String(50))
    basic_da = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, nullable=False)
    other_alw = db.Column(db.Float, nullable=False)
    cca = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add_employee_form():
    return render_template('add.html')

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        # Fetch form data
        employee_id = request.form['emp_id']
        employee_name = request.form['employee_name']
        pf_no = request.form['pf_no']
        esi_no = request.form['esi_no']
        nop=request.form['nop']
        doj = request.form['doj']
        designation = request.form['designation']
        department = request.form['department']
        ac_no = request.form['ac_no']
        ifsc_code = request.form['ifsc_code']
        pan_no = request.form['pan_no']
        aadhar_no = request.form['aadhar_no']
        uan = request.form['uan']
        basic_da = request.form['basic_da']
        hra = request.form['hra']
        other_alw = request.form['other_alw']
        cca = request.form['cca']

        # Create a new employee instance
        new_employee = Employee(employee_id=employee_id, employee_name=employee_name, 
                                pf_no=pf_no, esi_no=esi_no,nop=nop, doj=doj, designation=designation,
                                department=department, ac_no=ac_no, ifsc_code=ifsc_code, 
                                pan_no=pan_no, aadhar_no=aadhar_no, uan=uan, basic_da=basic_da,
                                hra=hra, other_alw=other_alw, cca=cca)
        # Add the new employee to the database session
        db.session.add(new_employee)
        # Commit the session to save changes to the database
        db.session.commit()
        return "Employee added successfully"

@app.route('/salary_slip/<int:employee_id>')
def generate_salary_slip(employee_id):
    # Fetch the employee from the database based on the employee_id
    employee = Employee.query.filter_by(id=employee_id).first()
    if employee:
        # Render the salary slip template with employee data
        return render_template('salary_slip.html', employee=employee)
    else:
        return "Employee not found"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
