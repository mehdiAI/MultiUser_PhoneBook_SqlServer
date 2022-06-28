create PROCEDURE delete_row(
                        --@delNot_name as BIT =0,  --delete components without considering to their name.
                        @del_state as CHAR(4)='a',  -- a=all components related the specific name and its id, p=phone, e = email , ad = address
                        @name_ID as INT =null,
                        @fname as NVARCHAR(50)=null,
                        @lname as NVARCHAR(50)='',
                        @phoneN as NVARCHAR(50)=null,
                        @email as NVARCHAR(50) = null,
                        @addr as NVARCHAR(200) = null,
                        @g_id as SMALLINT =1,
                        @typ_id as SMALLINT = 1
                                            )
as 

BEGIN
DECLARE @thisNameID INT =0;
    BEGIN TRAN  --transaction
        BEGIN TRY   -- try catch

            --If @del_state='a' and Exists(SELECT first_name , last_name from names where first_name = @fname and last_name = @lname )
            If (@name_ID is not NULL AND Exists(SELECT id from names where id = @name_ID ) ) or 
                @fname is not NULL and @lname is not NULL AND 
                Exists(SELECT first_name , last_name from names where first_name = @fname and last_name = @lname )
            Begin
                    --set @thisNameID = (select id from names where first_name=@fname and last_name=@lname);
                    set @thisNameID = IIF(@name_ID is not null , @name_ID,(select id from names where first_name=@fname and last_name=@lname));
                    DELETE from Address where name_id = @thisNameID
                    DELETE from email where name_id = @thisNameID
                    DELETE from phoneNumber where name_id = @thisNameID
                    DELETE from names where id = @thisNameID
                    select 'New_deleting_done' as message

            END

            ELSE

            BEGIN

                print 'name_not_existed or delState != a';
                select  'name_not_existed or delState != a' as ch_message;

                IF @del_state <> 'a' --delete components without considering to their name.
                BEGIN
                        IF (@phoneN is not NULL) AND EXISTS (SELECT phone_number from phoneNumber where phone_number=@phoneN )
                        BEGIN
                                DELETE from phoneNumber where phone_number=@phoneN
                        END
                        ELSE
                        BEGIN
                                SELECT 'p not existed' as ch_message
                        END

                        IF (@email is not NULL) AND EXISTS (SELECT email from email where email=@email )
                        BEGIN
                                DELETE from email where email=@email
                        END
                        ELSE
                        BEGIN
                                SELECT 'e not existed' as ch_message
                        END

                        IF (@addr is not NULL) AND EXISTS (SELECT Address from Address where Address=@addr )
                        BEGIN
                                DELETE from Address where Address=@addr
                        END
                        ELSE
                        BEGIN
                                SELECT 'A not existed' as ch_message
                        END
                END
                
                --select 'f_l_name_not_existed' as message 

            END

            COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
        END CATCH



END;