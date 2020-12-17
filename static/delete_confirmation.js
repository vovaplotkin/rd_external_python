function delete_employee(employee_id) {
  var r = confirm("Delete employee?");
  if (r == true) {
    window.location.href = "/employees/delete/" + employee_id;
  }
};

function delete_department(department_id) {
  var r = confirm("Delete department?");
  if (r == true) {
    window.location.href = "/departments/delete/" + department_id;
  }
};