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
    salary = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return f'<Employee {self.id}>'


@app.route('/', methods=['POST', 'GET'])
def index():
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
        departments = Departments.query.all()
        return render_template('index.html', departments=departments)


@app.route('/departments/delete/<int:id>')
def delete_department(id):
    dept_to_delete = Departments.query.get_or_404(id)
    try:
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


if __name__ == '__main__':
    app.run(debug=True)
