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
    cancelled int default (0),
    created_at timestamp default (now()),
    updated_at timestamp default (now()),
    blocked boolean default (false),
    primary key(id),
    unique (name, creator_id)
);

create table enrolled(
    id_course int not null,
    id_student int not null,
    status varchar(255) default 'on course' check (status in ('on course', 'approved', 'failed')),
    foreign key(id_course) references courses(id) on delete cascade,
    primary key(id_course, id_student)
);

create table collaborators(
    id_collaborator int not null,
    id_course int not null,
    foreign key(id_course) references courses(id) on delete cascade,
    primary key(id_course, id_collaborator)
);

create table favoriteCourses(
    course_id int not null,
    user_id int not null,
    foreign key (course_id) references courses(id) on delete cascade,
    primary key (course_id, user_id)
);
