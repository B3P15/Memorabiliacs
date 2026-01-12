-- use user_database;

-- create table Users ( 
-- UserID varchar(45) not null, 
-- Username varchar(45) not null,
-- PersonalDB varchar(45), 
-- PRIMARY KEY (UserID)
-- );

-- insert into Users(UserID, Username, PersonalDB)
-- values('Andrew', 'andrewrupp', 'ARuppDB');

use aruppdb;

drop table Pokemon;

create table Pokemon (
CardID varchar(45) not null);

insert into Pokemon(CardID)
values('ex2-8'),
('ex2-30'),
('base2-1'),
('dp7-1');