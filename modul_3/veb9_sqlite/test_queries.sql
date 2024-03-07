SELECT *
FROM students;


UPDATE students
SET student_name = 'Наш человек'
WHERE age IN (15,16,17,18) and course = 'python-ai';


SELECT
    student_name,
    age
FROM students
WHERE course == 'python-ai'
ORDER BY age ASC;


SELECT
    student_name,
    id
FROM students
WHERE id % 2 = 0;


SELECT distinct student_name
FROM students
WHERE age > 14 and course = 'python-ai'
ORDER BY student_name asc;


SELECT *
FROM students
WHERE course <> 'python-ai'


select *
from students
where
    student_name = 'Владимир' and
    course = 'python-ai'


SELECT
    group_number,
    COUNT(id) as количество_студентов
FROM students
GROUP BY group_number;


DELETE
FROM students
WHERE id = 5;


DELETE
FROM students;


ALTER TABLE students
ADD math_mark_exam INTEGER NULL;
