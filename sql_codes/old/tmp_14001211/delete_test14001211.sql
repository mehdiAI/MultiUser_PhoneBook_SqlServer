EXEC insert_all @fname ='mohi2' ,@lname='ssss' ,@phoneN='0955 45 85 365' , @email = 'ooo@yahoo.com',@addr = 'dd fooooooll kkk nnn';
EXEC insert_all @fname ='mohiii' ,@lname='ssss' ,@phoneN='095455 45 85 365' , @email = 'uwssw@yahoo.com',@addr = 'dd fswswswswkkk nnn';
EXEC insert_all @fname ='mohi2' ,@lname='ssss' ,@phoneN='0955 45 85 365';
EXEC insert_all @fname ='mohi2' ,@lname='ssss' ,@email = 'u7777@yahoo.com';
EXEC insert_all @fname ='mohi2' ,@lname='ssss' ,@addr = 'dd flllllllllllkk nnn';
--DBCC CHECKIDENT('names')
--DBCC CHECKIDENT('names',RESEED,1065)
declare @id as int=1067;
SELECT * from phoneNumber where name_id=@id;
SELECT * from email where name_id=@id;
SELECT * from Address where name_id=@id;

exec delete_row2 1500; 
EXEC del_phoneN '0955 45 85 365' , 1067
exec del_email 'u7777@yahoo.com' , 1067
exec del_Address 'dd flllllllllllkk nnn' , 1067

exec del_phoneN_byID 2121
exec del_email_byID 2081
exec del_Address_byID 1056
execute search3_apply @fname = 'mohi' , @lname='';

