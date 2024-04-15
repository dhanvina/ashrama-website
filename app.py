from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    # Add other columns as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add_employee_form():
    return render_template('add.html')

@app.route('/add_employee', methods=['POST'])
def add_employee():
    employee_id = request.form['emp_id']
    employee_name = request.form['employee_name']
    # Add other form fields as needed
    new_employee = Employee(employee_id=employee_id, employee_name=employee_name)
    db.session.add(new_employee)
    db.session.commit()
    return "Employee added successfully"

# @app.route('/generate_payslip_form')
# def generate_payslip_form():
#     return render_template('payslip.html')

# @app.route('/generate_payslip', methods=['POST'])
# def generate_payslip():
#     # Process the form data and generate the payslip
#     employee_id = request.form['employee_id']
#     month_year = request.form['month_year']
#     # Generate the payslip for the specified employee and month/year
#     return "Payslip generated successfully"

@app.route('/download_payslips')
def download_payslips():
    employees = Employee.query.all()
    # Assuming you have a method to generate payslips for each employee, 
    # you can create a dictionary with employee names as keys and payslips as values
    payslips = {employee.employee_name: generate_payslip(employee) for employee in employees}
    # Create a CSV file with employee names and payslips
    csv_data = '\n'.join([f'{name},{payslip}' for name, payslip in payslips.items()])
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=payslips.csv"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
