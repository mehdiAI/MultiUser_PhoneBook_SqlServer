create or alter PROCEDURE del_email_byID( @emailID as INT )
/*
-Delete specific email by specific email ID.
-Input parameters: @emailID .
-Output: result message.     'Email_deleting_done':OK
                            'Problems!,Email dont exist.'       
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @emailID IS NOT NULL AND  EXISTS (SELECT email_id from email where email_id = @emailID )
                Begin
                        --Delete Email
                        DELETE from email where email_id = @emailID
                        select 'Email_deleting_done' as ch_message
                END
            ELSE
                THROW 51000 , N'Problems!,Email dont exist.'  , 1 ; 

        COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END