-- 1. List the following details of each employee: employee number, last name, first name, sex, and salary.
SELECT e.emp_no, e.last_name, e.first_name, e.sex, s.salary
FROM   employees as e
LEFT JOIN salary as s on e.emp_no = s.emp_no;

-- 2. List first name, last name, and hire date for employees who were hired in 1986.
SELECT first_name, last_name, hire_date
FROM   employees
WHERE hire_date LIKE '%/86';

-- 3. List the manager of each department with the following information: department number, department name, the manager's employee number, last name, first name.
SELECT d.dept_no, d.dept_name, dm.emp_no, e.last_name, e.first_name
FROM   departments as d
LEFT JOIN dept_manager as dm ON  d.dept_no = dm.dept_no
LEFT JOIN employees as e on dm.emp_no = e.emp_no
;

-- 4. List the department of each employee with the following information: employee number, last name, first name, and department name.
SELECT e.emp_no, e.last_name, e.first_name, d.dept_name
FROM   employees as e
LEFT JOIN dept_emp as de ON e.emp_no = de.emp_no
LEFT JOIN departments as d ON de.dept_no = d.dept_no
;


-- 5. List first name, last name, and sex for employees whose first name is "Hercules" and last names begin with "B."
SELECT first_name, last_name, sex
FROM   employees
WHERE  first_name = 'Hercules' AND
       last_name LIKE 'B%'
;

-- 6. List all employees in the Sales department, including their employee number, last name, first name, and department name.
SELECT de.emp_no, e.last_name, e.first_name, d.dept_name
FROM dept_emp AS de
LEFT JOIN employees  AS e on de.emp_no = e.emp_no
LEFT JOIN departments AS d on de.dept_no = d.dept_no
WHERE  de.dept_no IN
		(SELECT dept_no
		 FROM   departments
		 WHERE  dept_name = 'Sales'	
		) -- I dont like my solution but I can't think of another way to do it.
;
	
-- 7. List all employees in the Sales and Development departments, including their employee number, last name, first name, and department name.
SELECT de.emp_no, e.last_name, e.first_name, d.dept_name
FROM dept_emp AS de
LEFT JOIN employees  AS e on de.emp_no = e.emp_no
LEFT JOIN departments AS d on de.dept_no = d.dept_no
WHERE  de.dept_no IN
		(SELECT dept_no
		 FROM   departments
		 WHERE  dept_name = 'Sales'	OR
		        dept_name = 'Development'
		) -- I dont like my solution but I can't think of another way to do it.
;
	
-- 8. In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.
SELECT e.last_name, COUNT(e.last_name) AS num_last_name
FROM employees AS e
GROUP BY e.last_name
ORDER BY num_last_name DESC 
;
