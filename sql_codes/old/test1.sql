USE PhoneBook
--exec insert_ @fname = 'Alex' , @lname = 'alexi' , @phoneN = '0937 48 40 785'

--select IDENT_CURRENT('names')
--exec insert_ @fname = 'Alex2' , @lname = 'alexi2' , @phoneN = '0938 45 86 524'
select * from names where id>1003
select * from phoneNumber where phoneN_id>2005
select * from email where email_id>1999

select IIF(id=1001,10,0) as ddd from [names] where id=1001
DECLARE @thisNameID as INT =0
set @thisNameID  = (select id from names where first_name='Amehdi' and last_name='vfakouri');
print @thisNameID

--select 'done' as message

--delete from phoneNumber where name_id=1007
--delete from [names] where id=1011

--BEGIN TRAN
--insert into names (first_name,last_name,group_id) values ('AAAAA','BBBBBB',1);
--COMMIT;
DECLARE @a as DECIMAL=1
DECLARE @b as DECIMAL=1
DECLARE @c as DECIMAL=0

BEGIN TRAN
BEGIN TRY
--SELECT last_name from names where id>1005
insert into names (first_name,last_name,group_id) values ('AAAAA','BBBBBB',1);
set @a = @b/@c
COMMIT TRANSACTION
END TRY
BEGIN CATCH
select ERROR_MESSAGE() as Emessage
ROLLBACK TRANSACTION
END CATCH

UPDATE names set last_name='ggg' where first_name='mona'

