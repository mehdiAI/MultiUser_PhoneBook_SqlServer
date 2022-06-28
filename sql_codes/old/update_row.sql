create PROCEDURE update_row(
                        @fname as NVARCHAR(50)=null,
                        @lname as NVARCHAR(50)=null,
                        @name_ID as INT=NULL,
                        @phoneN as NVARCHAR(50)=null,
                        @email as NVARCHAR(50) = null,
                        @addr as NVARCHAR(200) = null,
                        @g_id as SMALLINT =1,
                        @typ_id as SMALLINT = 1,

                        @fname_n as NVARCHAR(50)=null,
                        @lname_n as NVARCHAR(50)=null,
                        @phoneN_n as NVARCHAR(50)=null,
                        @email_n as NVARCHAR(50) = null,
                        @addr_n as NVARCHAR(200) = null,
                        @g_id_n as SMALLINT =null,
                        @typ_id_n as SMALLINT = null
                                            )
as 

BEGIN
DECLARE @thisNameID INT =0;


    BEGIN TRAN  --transaction
        BEGIN TRY   -- try catch

            --If Exists(SELECT first_name , last_name from names where first_name = @fname and last_name = @lname )
            If (@name_ID is not NULL AND Exists(SELECT id from names where id = @name_ID ) ) or 
                @fname is not NULL and @lname is not NULL AND Exists(SELECT first_name , last_name from names where first_name = @fname and last_name = @lname )
            Begin
                    --set @thisNameID = (select id from names where first_name=@fname and last_name=@lname);
                    set @thisNameID = IIF(@name_ID is not null , @name_ID,(select id from names where first_name=@fname and last_name=@lname));
                    IF  @fname_n is not NULL --@fname_n <> (SELECT first_name from names where id = @thisNameID ) AND
                    BEGIN
                            UPDATE  names SET first_name = @fname_n WHERE id = @thisNameID
                    END

                    IF @lname_n is not NULL --(SELECT last_name from names where id = @thisNameID )
                    BEGIN
                            UPDATE  names SET last_name = @lname_n WHERE id = @thisNameID
                    END

                    IF @phoneN_n is not NULL AND --@phoneN_n not in (SELECT phone_number from phoneNumber where name_id = @thisNameID ) AND
                        @phoneN in (SELECT phone_number from phoneNumber where name_id = @thisNameID )
                    BEGIN
                            UPDATE  phoneNumber SET phone_number = @phoneN_n WHERE name_id = @thisNameID AND phone_number=@phoneN
                            IF @typ_id_n is not NULL   
                            BEGIN
                                    UPDATE  phoneNumber SET type_id = @typ_id_n WHERE name_id = @thisNameID AND 
                                    (phone_number=@phoneN_n ) 
                            END

                    END
                    ELSE
                    BEGIN
                            IF @phoneN is not null AND  @phoneN not in (SELECT phone_number from phoneNumber where name_id = @thisNameID )
                            BEGIN         
                                    select 'p not exist u failed' as ch_message;
                                    THROW 51000 , N'p not exist u failed' , 1 ;
                            END
                    END

                    IF @email_n is not NULL AND --@email_n not in (SELECT email from email where name_id = @thisNameID ) AND
                        @email in (SELECT email from email where name_id = @thisNameID )
                    BEGIN
                            UPDATE  email SET email = @email_n WHERE name_id = @thisNameID AND email=@email  
                           IF @typ_id_n is not NULL   
                            BEGIN
                                    UPDATE  email SET type_id = @typ_id_n WHERE name_id = @thisNameID AND 
                                    (email=@email_n ) 
                            END
                    END
                    ELSE
                    BEGIN
                            IF @email is not null AND   @email not in (SELECT email from email where name_id = @thisNameID )
                            BEGIN
                                    select 'e not exist u failed' as ch_message;
                                    THROW 51000 , N'e not exist u failed' , 1 ;
                            END
                    END

                    IF @addr_n is not NULL AND --@addr_n not in (SELECT Address from Address where name_id = @thisNameID ) AND
                        @addr in (SELECT Address from Address where name_id = @thisNameID )
                    BEGIN
                            UPDATE  Address SET Address = @addr_n WHERE name_id = @thisNameID AND Address=@addr 
                           IF @typ_id_n is not NULL   
                            BEGIN
                                    UPDATE  Address SET type_id = @typ_id_n WHERE name_id = @thisNameID AND 
                                    (Address=@addr_n ) 
                            END
                    END
                    ELSE
                    BEGIN
                            IF @addr is not null AND   @addr not in (SELECT Address from Address where name_id = @thisNameID )
                            BEGIN
                                    select 'A not exist u failed' as ch_message;
                                    THROW 51000 , N'A not exist u failed' , 1 ;
                            END
                    END

                    IF @g_id_n is not NULL --<> (SELECT group_id from names where id = @thisNameID )
                        
                    BEGIN
                            UPDATE  names SET group_id = @g_id_n WHERE id = @thisNameID                         
                    END

                    --IF @typ_id_n <> @typ_id   
                    --BEGIN
                            --UPDATE  phoneNumber SET type_id = @typ_id_n WHERE name_id = @thisNameID AND 
                            --(phone_number=@phoneN or phone_number=@phoneN_n) 
                    --END

                    select 'New_updating_done' as message

            End

            ELSE

            BEGIN

            print 'name_not_existed';

            select 'f_l_name_not_existed' as message 

            END

            COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
        END CATCH



END;