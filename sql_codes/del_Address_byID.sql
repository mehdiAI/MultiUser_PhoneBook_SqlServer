create or alter PROCEDURE del_Address_byID( @addrID as INT )
/*
-Delete specific Address by specific Address ID.
-Input parameters: @addrID .
-Output: result message.     'Address_deleting_done':OK
                            'Problems!,Address dont exist.'     
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @addrID IS NOT NULL AND  EXISTS (SELECT Address_id from Address where Address_id = @addrID )
                Begin
                        --Delete Email
                        DELETE from Address where Address_id = @addrID
                        select 'Address_deleting_done' as ch_message
                END
            ELSE
                THROW 51000 , N'Problems!,Address dont exist.' , 1 ; 

        COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END