-- exercise 0: friends table
CREATE TABLE friends (
    name VARCHAR2(50), 
    age NUMBER(3),
    main_game VARCHAR2(50)
);

SELECT * FROM friends;

-- exercise 1: projects table
CREATE TABLE projects (
    project_id NUMBER(5),
    project_name VARCHAR2(100),
    start_date DATE DEFAULT SYSDATE
);

SELECT * FROM projects;