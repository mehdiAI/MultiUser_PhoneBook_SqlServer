CREATE PROCEDURE search (
                        @name_ID as INT = null , 
                        @L_limit as INT =null ,
                        @H_limit as INT =null ,
                        @numberRow as smallint =NULL ,
                        @fname as NVARCHAR(50)='',
                        @lname as NVARCHAR(50)='',
                        @phoneN as NVARCHAR(50)=null,
                        @email as NVARCHAR(50) = null,
                        @addr as NVARCHAR(200) = null,
                        @g_id as SMALLINT = null,
                        @typ_id as SMALLINT = null

)

as 
SET NOCOUNT ON
--DECLARE @nid as INT =0;
DECLARE @nid TABLE (n_id int);
DECLARE @pid TABLE (p_id int);
DECLARE @eid TABLE (e_id int);
DECLARE @aid TABLE (a_id int);

BEGIN
        BEGIN TRY

        insert into @nid SELECT id from names where first_name LIKE '%'+@fname+'%' AND last_name LIKE '%'+@lname+'%' ;
        --select name_id, max(phoneN_id) over(PARTITION by name_id ) as partition_id from phoneNumber where name_id in (select n_id from @nid);
        insert into @pid select distinct max(phoneN_id) over(PARTITION by name_id ) as Ppartition_id from phoneNumber where name_id in (select n_id from @nid);
        insert into @eid select distinct max(email_id) over(PARTITION by name_id ) as Epartition_id from email where name_id in (select n_id from @nid);
        insert into @aid select distinct max(Address_id) over(PARTITION by name_id ) as Apartition_id from Address where name_id in (select n_id from @nid);
        --select * from @nid;
        --select * from @pid;
        --select * from @eid;
        --select * from @aid;
        --SELECT * from names where id in (select n_id from @nid); 
        --SELECT  * from phoneNumber where name_id in (select n_id from @nid);
        --SELECT * from email where name_id in (select n_id from @nid);
        --select * from Address where name_id in (select n_id from @nid);

        select * from names 
                        full OUTER JOIN phoneNumber
                        on  id = phoneNumber.name_id AND phoneN_id in (select p_id from @pid)
                        FULL OUTER JOIN email
                        ON id = email.name_id AND email_id in (select e_id from @eid)
                        FULL OUTER JOIN address 
                        ON id = Address.name_id AND Address_id in (select a_id from @aid)
                        where id in (select n_id from @nid) ;

        END TRY

        BEGIN CATCH
            --select 'errorrrrrr'
            select ERROR_MESSAGE() as ch_message
        END CATCH


END


