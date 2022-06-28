
EXEC insert_2 0,'mani7' , ' ' , '   ' , '     ' , '      ' 
EXEC insert_2 0, 'mani5' , 'tarr5' , '0985 69 85 411' , 'eee@yahoo.com' , 'eeee eee eee ee ee e' , 1, 1
EXEC insert_2 1079, 'mani66' , 'tarr5' , '' , 'tttttttttt@yahoo.com' , '' , 1, 1
EXEC insert_2 1079, 'mani66' , 'tarr5' , '' , '' , 'kkkkkkkkkkkkkkkk' , 1, 1
EXEC insert_2 1079, 'mani66' , 'tarr5' , '098888888888' , '' , '' , 1, 1
EXEC insert_2 1081, ' ' , ' ' , '   ' , '' , 'ssssssssssssssss' , 1, 1
DECLARE @thisNameID INT =0;
set @thisNameID = (select IDENT_CURRENT('names'));
select @thisNameID as last_row
SELECT * from names where id > @thisNameID-8
SELECT * from phoneNumber where name_id > @thisNameID-8
SELECT * from email where name_id > @thisNameID-8
SELECT * from Address where name_id > @thisNameID-8
--EXEC delete_row2 1073
EXEC search3_apply 'mani'
EXEC search3_join 'mani'