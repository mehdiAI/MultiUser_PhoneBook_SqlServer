
CREATE or ALTER PROCEDURE search3 (

                        @fname as NVARCHAR(50)='',
                        @lname as NVARCHAR(50)=''


)

as 
SET NOCOUNT ON
--DECLARE table variable becuase of seaching results.
DECLARE @nid TABLE (n_id int);
DECLARE @pid TABLE (p_id int);
DECLARE @eid TABLE (e_id int);
DECLARE @aid TABLE (a_id int);
 

BEGIN
        BEGIN TRY
        -- collect name Ids into @nid table that related to fname and lname .
        insert into @nid SELECT id from names where first_name LIKE '%'+@fname+'%' AND last_name LIKE '%'+@lname+'%' ;

        -- collect last phone Number , last email and last Address for each found name Ids.
        insert into @pid select distinct max(phoneN_id) over(PARTITION by name_id ) as Ppartition_id from phoneNumber  ,@nid as i where name_id = i.n_id;
        insert into @eid select distinct max(email_id) over(PARTITION by name_id ) as Epartition_id from email ,@nid as i where name_id = i.n_id;
        insert into @aid select distinct max(Address_id) over(PARTITION by name_id ) as Apartition_id from Address ,@nid as i where name_id = i.n_id;

        select * from names
                        full OUTER JOIN phoneNumber
                        on  id = phoneNumber.name_id AND phoneN_id in (select p_id from @pid)
                        FULL OUTER JOIN email
                        ON id = email.name_id AND email_id in (select e_id from @eid)
                        FULL OUTER JOIN address 
                        ON id = Address.name_id AND Address_id in (select a_id from @aid)
                        where id in (select n_id from @nid) ;

        select  id , first_name , last_name , group_id , 
                        p.phoneN_id , p.phone_number ,p.name_id , p.type_id ,
                        e.email_id , e.email ,e.name_id , e.type_id , 
                        a.Address_id , a.Address ,a.name_id  , a.type_id  
                        from names as Nm
                        OUTER APPLY ( select * from phoneNumber , @pid as pi where phoneN_id = pi.p_id AND name_id = Nm.id  ) p
                        OUTER APPLY ( select *from email , @eid as ei where email_id = ei.e_id AND name_id = Nm.id) e
                        OUTER APPLY ( select * from address , @aid as ai where Address_id = ai.a_id AND name_id = Nm.id) a
                        where id in (p.name_id,e.name_id,a.name_id)  ORDER by first_name

        END TRY

        BEGIN CATCH
            --select 'errorrrrrr'
            select ERROR_MESSAGE() as ch_message
        END CATCH


END
GO
