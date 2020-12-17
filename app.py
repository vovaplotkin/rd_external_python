from datetime import date
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epam.db'
db = SQLAlchemy(app)


class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        return f'<Department {self.id}>'


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Employee {self.id}>'


@app.route('/')
def departments():
    departments_salary = db.session.\
        query(
            Departments.id,
            Departments.department,
            db.func.avg(Employees.salary).label('avg_salary')
        ).outerjoin(Employees, Departments.id == Employees.department_id)\
        .group_by(Departments.id, Departments.department).all()
    return render_template('departments.html', departments_salary=departments_salary)


@app.route('/departments/add', methods=['POST', 'GET'])
def add_department():
    if request.method == 'POST':
        department = request.form['department']
        new_dept = Departments(department=department)
        try:
            db.session.add(new_dept)
            db.session.commit()
            return redirect('/')
        except:
            return 'The error occurs while adding new department'
    else:
        return render_template('add_department.html')


@app.route('/departments/delete/<int:id>')
def delete_department(id):
    employees = Employees.query.filter_by(department_id=id)
    dept_to_delete = Departments.query.get_or_404(id)
    try:
        if employees:
            dept_others = Departments.query.filter_by(department='Others').first()
            if not dept_others:
                new_dept = Departments(department='Others')
                db.session.add(new_dept)
                db.session.commit()
                dept_others = Departments.query.filter_by(department='Others').first()
            employees.update({'department_id': dept_others.id})
            db.session.commit()
        db.session.delete(dept_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'The error occurs while deleting department'


@app.route('/departments/edit/<int:id>', methods=['POST', 'GET'])
def edit_department(id):
    department = Departments.query.get_or_404(id)
    if request.method == 'POST':
        department.department = request.form['department']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'The error occurs while editing department'
    else:
        return render_template('edit_department.html', department=department)


@app.route('/departments/<int:id>')
def employees_by_department(id):
    employees = Employees.query.filter_by(department_id=id).all()
    department = Departments.query.get_or_404(id)
    return render_template('employees_by_department.html', employees=employees, department=department)


@app.route('/departments/<int:id>/employees/add', methods=['POST', 'GET'])
def add_employee(id):
    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = date.fromisoformat(request.form['date_of_birth'])
        salary = request.form['salary']
        new_employee = Employees(
            name=name,
            department_id=id,
            date_of_birth=date_of_birth,
            salary=salary
        )
        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect(f'/departments/{id}')
        except:
            return 'The error occurs while adding new employee'
    else:
        department = Departments.query.get_or_404(id)
        return render_template('add_employee.html', department=department)


@app.route('/employees/delete/<int:id>')
def delete_employee(id):
    employee = Employees.query.get_or_404(id)
    department_id = employee.department_id
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect(f'/departments/{department_id}')
    except:
        return 'The error occurs while deleting employee'


@app.route('/employees/edit/<int:id>', methods=['POST', 'GET'])
def edit_employee(id):
    employee = Employees.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.department_id = db.session.query(Departments.id)\
            .filter_by(department=request.form['department']).first().id
        employee.date_of_birth = date.fromisoformat(request.form['date_of_birth'])
        employee.salary = float(request.form['salary'])
        try:
            db.session.commit()
            return redirect(f'/departments/{employee.department_id}')
        except:
            return 'The error occurs while editing employee'
    else:
        departments = Departments.query.all()
        return render_template('edit_employee.html', employee=employee, departments=departments)


if __name__ == '__main__':
    app.run(debug=True)
