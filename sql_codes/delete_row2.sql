create or alter PROCEDURE delete_row2(@name_ID as INT)
/*
-Delete name and all Phone numbers, emails and Addresses related to this @name_ID
Input parameters: @name_ID -> This id related to specific name in names table.
Output: result message.     'Row_deleting_done':OK
                            'Problems!,ID dont exist.'       
*/
as 
BEGIN
    BEGIN TRAN  --transaction
        BEGIN TRY   -- try catch
            If @name_ID is not NULL AND Exists(SELECT id from names where id = @name_ID ) 
                Begin
                        --Delete name and all Phone numbers emails and Addresses related to this @name_ID
                        DELETE from names where id = @name_ID
                        select 'Row_deleting_done' as message
                END

                ELSE
                    THROW 51000 , N'Problems!,ID dont exist.' , 1 ; 
 
            COMMIT TRANSACTION

        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH



END;