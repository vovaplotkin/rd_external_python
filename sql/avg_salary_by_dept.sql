select department_name, round(avg(salary), 2)
from employee a
left join department b on a.department_id = b.department_id
group by 1
order by 2 desc