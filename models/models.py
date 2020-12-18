from app import db


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
