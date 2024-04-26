create table if not exists users(
                                    id serial primary key,
                                    telegram_id varchar(25) unique not null,
    username varchar(255) ,
    name varchar(255),
    invited_by int default 0,
    created_at timestamp default now()
    );

create table if not exists books(
                                    id serial primary key,
                                    name varchar(255) not null ,
    created_at timestamp default now()
    );

create table if not exists tests(
                                    id serial primary key,
                                    book_id int references  books(id),
    number int not null ,
    created_at timestamp default now()
    );

create table if not exists passages(
                                       id serial primary key,
                                       number int references tests(id),
    created_at timestamp default now()
    );

create table if not exists vocabulary(
                                         id serial primary key ,
                                         word varchar(255) not null ,
    definition varchar(500),
    translation varchar(500) not null,
    created_at timestamp default now()
    );
