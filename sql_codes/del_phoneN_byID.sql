create or alter PROCEDURE del_phoneN_byID( @phoneNID as INT )
/*
-Delete specific Phone number by specific phone ID.
-Input parameters: @phoneNID .
-Output: result message.     'phoneN_deleting_done':OK
                            'Problems!,Phone number dont exist.'       
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @phoneNID IS NOT NULL AND  EXISTS (SELECT phoneN_id from phoneNumber where phoneN_id = @phoneNID )
                Begin
                        --Delete Phone number
                        DELETE from phoneNumber where phoneN_id = @phoneNID
                        select 'phoneN_deleting_done' as ch_message
                END
            ELSE
                THROW 51000 , N'Problems!,Phone number dont exist.' , 1 ; 

        COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END