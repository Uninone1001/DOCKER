create database if not exists
rezistra;
user rezistra;

CREATE TABLE IF not exist login (
    id int(11) auto_increment,
    user varchar(255),
    senha int(10,2)
    PRIMARY KEY (id)
);
insert into login value ('juan.almeida', 1234);