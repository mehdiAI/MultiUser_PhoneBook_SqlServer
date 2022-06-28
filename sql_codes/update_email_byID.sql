CREATE or alter PROCEDURE update_email_byID( @emailID as INT ,@Nemail as NVARCHAR(50) )
/*
-update specific email by specific email ID IF email ID exist.
-Input parameters: @emailID , @Nemail .
Output: result message.     1-'Email_updating_done':OK
                            2-'Problems!,Email ID dont exist.'
                            3-'Problems!,@Nemail is empty or params are null.'   
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @emailID IS NOT NULL AND @Nemail IS NOT NULL AND  @Nemail <> '' AND @Nemail <> ' ' 
                BEGIN
                            
                        IF  EXISTS (SELECT email_id from email where email_id = @emailID )
                        BEGIN
                                --Update email
                                UPDATE  email SET email = @Nemail WHERE email_id = @emailID
                                select 'Email_updating_done' as ch_message
                        END   
                        ELSE
                            THROW 51000 , N'Problems!,Email ID dont exist.' , 1 ; 


                END
            ELSE
                THROW 51000 , N'Problems!,@Nemail is empty or params are null.' , 1 ; 
                
        COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END