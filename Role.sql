use hospital;
create table Role(Role_ID int auto_increment primary key, Role_Name varchar(255));
insert into Role(Role_Name) values("Admin"), ("Doctor"),("Patient");
select * from Role;