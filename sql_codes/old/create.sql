--drop table types;

create table types(
    type_id smallint not null PRIMARY key identity(1,1),
    t_name nvarchar(50) 
)

INSERT into types (t_name) VALUES 
('Not assigned'),
('Home'),
('Work'),
('main'),
('Other')