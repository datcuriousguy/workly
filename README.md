# workly
A To Do App for Desktop that uses electron and flask.

To turn her on open cmd in directory as all the files and type 'npm start'.

You have to have electron installed for npm start to work. If you don't have electron,
install electron using pip or any online source u find.

Note: Workly stores all your tasks and their 'done' / 'not done' statuses in a mysql
database so ensure you have a database called 'todolist' with a table called 'workly' with specific properties.
Here is the mysql statement to create such a database and table:

create database todolist;
CREATE TABLE workly (
    id INT NOT NULL AUTO_INCREMENT,
    task_text VARCHAR(255) NOT NULL,
    category ENUM('Work', 'Personal', 'Shopping', 'Custom') NOT NULL,
    priority ENUM('Low', 'Medium', 'High') NOT NULL,
    due_date DATE DEFAULT NULL,
    completed TINYINT(1) DEFAULT 0,
    PRIMARY KEY (id)
);

If you find any discrepancies in the code, please reach out so I can further improve the app.

cheerios and have fun doing things


