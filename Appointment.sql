use hospital;
create table Appointment(Appt_ID int auto_increment primary key,Patient_ID int, Doc_ID int, appt_date date, time_slot varchar(255), status varchar(255));
select * from Appointment;