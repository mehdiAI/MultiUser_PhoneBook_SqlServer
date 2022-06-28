create or alter PROCEDURE del_address( @addr as NVARCHAR(50) , @name_ID as INT )
/*
-Delete specific Address by specific Address and ID in input(All same Addresss  will delete for that name. ).
-Input parameters: @addr(Address) -> must be same with the record in table  and  @name_ID -> related specific name ID in names table.
-Output: result message.     'Address_deleting_done':OK
                            'Problems!,Address dont exist.'       
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @addr IS NOT NULL AND @name_ID IS NOT NULL AND EXISTS (SELECT Address from Address where Address = @addr AND name_id = @name_ID )
                Begin
                        --Delete Address
                        DELETE from Address where Address = @addr AND name_id = @name_ID
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