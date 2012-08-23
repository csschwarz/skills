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
	lastname string
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

insert into user(username, password, firstname, lastname) values ('admin', 'admin', 'Admin', 'Adminson');

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