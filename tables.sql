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
    book_id int references books(id) not null,
    number int not null ,
    created_at timestamp default now()
    );

create table if not exists passages(
    id serial primary key,
    test_id int references tests(id) not null,
    number int not null,
    created_at timestamp default now()
   );

create table if not exists vocabulary(
    id serial primary key ,
    passage_id int references passages(id) not null ,
    word varchar(255) not null ,
    definition varchar(500),
    translation varchar(500) not null,
    created_at timestamp default now()
);

create table if not exists test_source(
    id serial primary key ,
    book_id int references books(id),
    test_id int references tests(id),
    passage_id int references passages(id),
    word_id int references vocabulary(id),
    created_at timestamp default now()
);

create table if not exists test(
    id serial primary key ,
    source_id int references test_source(id),
    user_id int references users(id),
    created_at timestamp default now()
);

create table if not exists test_results(
    id serial primary key ,
    user_id int references users(id),
    test_id int references test(id),
    score int not null ,
    created_at timestamp default now()
)