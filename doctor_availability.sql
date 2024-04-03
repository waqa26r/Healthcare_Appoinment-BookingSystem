
create table doctor_availability(Doc_ID int, Speciality varchar(255), Date_Available DATE, time_slot varchar(255), foreign key(Doc_Id) references users(User_Id));
select * from doctor_availability;
insert into doctor_availability values(19,"Physio", "2024-02-20", "Morning (12:00 PM- 2:00 PM)");
insert into doctor_availability values(17,"Orthopedics", "2024-02-20", "Morning (9:00 AM- 11:00 AM)");

select users.Name, doctor_availability.Speciality, doctor_availability.Doc_ID
from users inner join doctor_availability where users.User_ID=doctor_availability.Doc_ID;



