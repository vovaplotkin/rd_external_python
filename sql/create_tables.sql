CREATE TABLE department (
	department_id SERIAL PRIMARY KEY,
	department_name TEXT
);

CREATE TABLE employee (
	employee_id SERIAL PRIMARY KEY,
	employee_name TEXT,
	department_id INTEGER,
	date_of_birth DATE,
	salary NUMERIC,
	FOREIGN KEY (department_id) REFERENCES department (department_id) ON UPDATE CASCADE ON DELETE CASCADE
);