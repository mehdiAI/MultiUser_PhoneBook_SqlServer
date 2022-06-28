
CREATE or ALTER PROCEDURE search_join_byUserID (
                        @UsrID as INT,
                        @fname as NVARCHAR(50)='',
                        @lname as NVARCHAR(50)=''
)

as 
SET NOCOUNT ON
--DECLARE table variable becuase of seaching results.
DECLARE @nid TABLE (n_id int);

BEGIN
        BEGIN TRY
            -- collect name Ids into @nid table that related to fname and lname .
            insert into @nid SELECT id from names where first_name LIKE '%'+@fname+'%' AND last_name LIKE '%'+@lname+'%' AND UserID=@UsrID ;

            select * from names 
                            full OUTER JOIN phoneNumber
                            on  id = phoneNumber.name_id AND ( phoneN_id in (select distinct max(phoneN_id) over(PARTITION by name_id ) as Ppartition_id
                                                                            from phoneNumber  ,@nid as i where name_id = i.n_id) )
                            FULL OUTER JOIN email
                            ON id = email.name_id AND ( email_id in (select distinct max(email_id) over(PARTITION by name_id ) as Epartition_id
                                                                    from email ,@nid as i where name_id = i.n_id) )
                            FULL OUTER JOIN address 
                            ON id = Address.name_id AND ( Address_id in (select distinct max(Address_id) over(PARTITION by name_id ) as Apartition_id
                                                                        from Address ,@nid as i where name_id = i.n_id) )
                            where id in (select n_id from @nid) ;

        END TRY

        BEGIN CATCH
            select ERROR_MESSAGE() as ch_message
        END CATCH


END
GO