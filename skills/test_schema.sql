drop table if exists skilltab;
create table skilltab (
	name string primary key,
	category string not null
);

drop table if exists user;
create table user (
	id integer primary key autoincrement,
	username string unique not null,
	password string not null,
	firstname string,
	lastname string,
	isadmin integer not null default 0
);

drop table if exists scoredescription;
create table scoredescription (
	score integer primary key,
	description string not null
);

drop table if exists userskill;
create table userskill (
	userid integer not null,
	skill string not null,
	score integer not null,
	constraint user_skill_pk primary key (userid, skill),
	constraint user_fk foreign key (userid) references user(id),
	constraint skill_fk foreign key (skill) references skilltab(name),
	constraint score_fk foreign key (score) references scoredescription(score)
);

-- Seed database:

insert into user(username, password, firstname, lastname, isadmin) values ('admin', 'admin', 'Admin', 'Adminson', 1);
insert into user(username, password, firstname, lastname) values ('default', 'd', 'Normal', 'User');
insert into user(username, password, firstname, lastname) values ('test', 't', 'Test', 'User');
insert into user(username, password, firstname, lastname) values ('test2', 't', 'Test', 'User 2');

insert into scoredescription(score, description) values (1, 'Don''t know it');
insert into scoredescription(score, description) values (2, 'Want to learn it');
insert into scoredescription(score, description) values (3, 'Know it');
insert into scoredescription(score, description) values (4, 'Can do it alone');
insert into scoredescription(score, description) values (5, 'Can teach it');

insert into skilltab(name, category) values ('Java', 'Programming');
insert into skilltab(name, category) values ('Groovy', 'Programming');
insert into skilltab(name, category) values ('Python', 'Programming');

insert into skilltab(name, category) values ('English', 'Language');
insert into skilltab(name, category) values ('Portuguese', 'Language');
insert into skilltab(name, category) values ('Spanish', 'Language');

insert into skilltab(name, category) values ('Test strategy creation', 'Testing');
insert into skilltab(name, category) values ('Build automated test frameworks', 'Testing');
insert into skilltab(name, category) values ('Manual Testing', 'Testing');