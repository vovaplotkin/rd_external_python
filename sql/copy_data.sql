COPY department(department_id, department_name)
FROM 'C:\Program Files\PostgreSQL\12\data\department.csv'
DELIMITER ','
CSV HEADER;

COPY employee(employee_name, department_id, date_of_birth, salary)
FROM 'C:\Program Files\PostgreSQL\12\data\employee.csv'
DELIMITER ','
CSV HEADER;