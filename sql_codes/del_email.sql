create or alter PROCEDURE del_email( @email as NVARCHAR(50) , @name_ID as INT )
/*
-Delete specific email by specific email and ID in input(All same emails  will delete for that name. ).
-Input parameters: @email -> must be same with the record in table   and  @name_ID -> related specific name ID in names table.
-Output: result message.     'Email_deleting_done':OK
                            'Problems!,Email dont exist.'       
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @email IS NOT NULL AND @name_ID IS NOT NULL AND EXISTS (SELECT email from email where email = @email AND name_id = @name_ID )
                Begin
                        --Delete Email
                        DELETE from email where email = @email AND name_id = @name_ID 
                        select 'Email_deleting_done' as ch_message
                END
            ELSE
                THROW 51000 , N'Problems!,Email dont exist.' , 1 ; 

        COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END