use hospital;
select * from users;
delete from users where User_Id="4";
alter table users drop primary key;
ALTER TABLE users ADD UNIQUE INDEX (User_ID);
alter table users modify Sr_No int not null auto_increment primary key;
alter table users add column Blood_Group varchar(10);
alter table users add column Age int;

ALTER TABLE Users DROP COLUMN User_ID;
ALTER TABLE Users CHANGE Sr_No User_Id INT;
alter table users modify User_Id int not null auto_increment;
ALTER TABLE Users MODIFY Gender CHAR(10);
ALTER TABLE Users MODIFY Address VARCHAR(50);
ALTER TABLE Users MODIFY Phone_No INT;
ALTER TABLE Users MODIFY Role_ID INT;

DELETE FROM users WHERE user_id BETWEEN  4 AND  10;

