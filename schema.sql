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

drop table if exists userskill;
create table userskill (
	userid integer not null,
	skill string not null,
	score integer not null,
	constraint user_skill_pk primary key (userid, skill),
	constraint user_fk foreign key (userid) references user(id),
	constraint skill_fk foreign key (skill) references skilltab(name)
);

-- Seed database:

insert into user(username, password, firstname, lastname, isadmin) values ('admin', 'admin', 'Admin', 'Adminson', 1);
insert into user(username, password, firstname, lastname) values ('default', 'd', 'Normal', 'User');

insert into skilltab(name, category) values ('Java', 'Programming');
insert into skilltab(name, category) values ('Groovy', 'Programming');
insert into skilltab(name, category) values ('Python', 'Programming');
-- insert into skilltab(name, category) values ('Ruby', 'Programming');
-- insert into skilltab(name, category) values ('Perl', 'Programming');
-- insert into skilltab(name, category) values ('Javascript', 'Programming');
-- insert into skilltab(name, category) values ('F#', 'Programming');
-- insert into skilltab(name, category) values ('C#', 'Programming');
-- insert into skilltab(name, category) values ('PHP', 'Programming');
-- insert into skilltab(name, category) values ('Ruby on Rails', 'Programming');
-- insert into skilltab(name, category) values ('C++', 'Programming');
-- insert into skilltab(name, category) values ('SQL', 'Programming');
-- insert into skilltab(name, category) values ('Dev Ops', 'Programming');
-- insert into skilltab(name, category) values ('iOS', 'Programming');
-- insert into skilltab(name, category) values ('Android', 'Programming');
-- insert into skilltab(name, category) values ('HTML', 'Programming');
-- insert into skilltab(name, category) values ('HTML5', 'Programming');
-- insert into skilltab(name, category) values ('Scala', 'Programming');
-- insert into skilltab(name, category) values ('CSS', 'Programming');
-- insert into skilltab(name, category) values ('JSP', 'Programming');

insert into skilltab(name, category) values ('English', 'Language');
insert into skilltab(name, category) values ('Portuguese', 'Language');
insert into skilltab(name, category) values ('Spanish', 'Language');
-- insert into skilltab(name, category) values ('Hindi', 'Language');
-- insert into skilltab(name, category) values ('Mandarin', 'Language');
-- insert into skilltab(name, category) values ('Cantonese', 'Language');
-- insert into skilltab(name, category) values ('Arabic', 'Language');
-- insert into skilltab(name, category) values ('French', 'Language');
-- insert into skilltab(name, category) values ('German', 'Language');
-- insert into skilltab(name, category) values ('Italian', 'Language');
-- insert into skilltab(name, category) values ('Afrikaans', 'Language');
-- insert into skilltab(name, category) values ('Dutch', 'Language');
-- insert into skilltab(name, category) values ('Malay', 'Language');

insert into skilltab(name, category) values ('Test strategy creation', 'Testing');
insert into skilltab(name, category) values ('Build automated test frameworks', 'Testing');
insert into skilltab(name, category) values ('Manual Testing', 'Testing');
-- insert into skilltab(name, category) values ('Load testing', 'Testing');
-- insert into skilltab(name, category) values ('Cucumber', 'Testing');
-- insert into skilltab(name, category) values ('Selenium', 'Testing');
-- insert into skilltab(name, category) values ('QTP', 'Testing');
-- insert into skilltab(name, category) values ('JMeter', 'Testing');
-- insert into skilltab(name, category) values ('Performance testing', 'Testing');