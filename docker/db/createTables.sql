create table courses(
    name varchar(255) not null,
    id serial not null,
    exams int not null,
    creator_id int not null,
    type varchar(255) not null,
    subscription varchar(255) not null,
    description varchar(1500) not null,
    hashtags varchar(1000) default (''),
    location varchar(255) not null,
    primary key(id),
    unique (name, creator_id)
);

create table enrolled(
    id_course int not null,
    id_student int not null,
    status int not null,
    foreign key(id_course) references courses(id) on delete cascade,
    primary key(id_course, id_student)
);

create table colaborators(
    id_colaborator int not null,
    id_course int not null,
    foreign key(id_course) references courses(id) on delete cascade,
    primary key(id_course, id_colaborator)
);