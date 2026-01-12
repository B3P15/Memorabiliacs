-- Add new user to user_database

use user_database;

insert into users(UserID, Username, PersonalDB)
values ('value', 'value', 'value');

	-- Create new user database (with adding a new user)

	create database usernameDB;

-- Access existing user database

use usernameDB;

-- If user doesn't have a collection of a specific item yet

-- create table CollectionName(
-- primary-key, varchar(45) not null, 
-- attribute varchar(45) not null,
-- attribute varchar(45),
-- attribute int(3), 
-- PRIMARY KEY (primary-key)
-- );

insert into Pokemon(CardID)
values('card-id');

-- insert into Pokemon(CardID)
-- values('card-id'),
-- ('card-id'),
-- ... etc;