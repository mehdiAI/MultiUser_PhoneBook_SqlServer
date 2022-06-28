create PROCEDURE insert_all(
                        @fname as NVARCHAR(50),
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

            If Not Exists(SELECT first_name , last_name from names where first_name = @fname and last_name = @lname )
                --Not Exists(SELECT last_name from names where last_name = @lname ) 
                --Not Exists(SELECT email from email where email = @email ) OR
                --Not Exists(SELECT Address from Address where Address = @addr ) OR
                --Not Exists(SELECT group_id from names where group_id = @g_id ) OR
                --Not Exists(SELECT type_id from phoneNumber where type_id = @typ_id)

            Begin
                        insert into names (first_name,last_name,group_id) values (@fname,@lname,@g_id);
                        set @thisNameID = (select IDENT_CURRENT('names'));

                        IF @phoneN is not null
                        BEGIN
                            insert into phoneNumber (phone_number,name_id,type_id) values (@phoneN,@thisNameID ,@typ_id);
                        END

                        IF @email is not NULL
                        BEGIN
                            insert into email (email,name_id,type_id) values (@email,@thisNameID,@typ_id);
                        END

                        IF @addr is not NULL
                        BEGIN
                            insert into Address (Address,name_id,type_id) values (@addr,@thisNameID,@typ_id);
                        END

                        select 'New_inserting_done' as message

            End

            ELSE

            BEGIN

                    print 'name_existed';
                    --select 'f_l_name_existed_done' as message 

                    set @thisNameID  = (select id from names where first_name=@fname and last_name=@lname);

                    IF (@phoneN is Not null) AND not Exists(SELECT phone_number from phoneNumber where  phone_number = @phoneN ) 
                    BEGIN
                            insert into phoneNumber (phone_number,name_id,type_id) values (@phoneN,@thisNameID,@typ_id);
                    END
                    ELSE
                    BEGIN
                            IF @phoneN is not null AND  @phoneN in (SELECT phone_number from phoneNumber )
                            BEGIN         
                                    --select 'p  existed i failed' as ch_message;
                                    THROW 51000 , N'p existed i failed' , 1 ;
                            END
                    END
                    IF (@email is Not null) AND not Exists(SELECT email from email where  email = @email ) 
                    BEGIN
                            insert into email (email,name_id,type_id) values (@email,@thisNameID,@typ_id);
                    END
                    ELSE
                    BEGIN
                            IF @email is not null AND  @email in (SELECT email from email  )
                            BEGIN         
                                    --select 'e  existed i failed' as ch_message;
                                    THROW 51000 , N'e existed i failed' , 1 ;
                            END
                    END

                    IF (@addr is Not null) AND not Exists(SELECT Address from Address where  Address = @addr ) 
                    BEGIN
                            insert into Address (Address,name_id,type_id) values (@addr,@thisNameID,@typ_id);
                    END
                    ELSE
                    BEGIN
                            IF @addr is not null AND  @addr in (SELECT Address from Address )
                            BEGIN         
                                    --select 'a  existed i failed' as ch_message;
                                    THROW 51000 , N'a existed i failed' , 1 ;
                            END
                    END
            

            END

            COMMIT TRANSACTION
            select 'f_l_name_existed_done' as message 
        END TRY
        BEGIN CATCH
            select ERROR_MESSAGE() as ch_message
            ROLLBACK TRANSACTION
        END CATCH



END;