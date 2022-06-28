create or alter PROCEDURE del_phoneN( @phoneN as NVARCHAR(50) , @name_ID as INT )
/*
-Delete specific Phone number by specific number and ID(All same P_numbers  will delete for that name. ).
-Input parameters: @phoneN -> must be same even spaces between numbers  and  @name_ID -> related specific name ID in names table.
-Output: result message.     'phoneN_deleting_done':OK
                            'Problems!,Phone number dont exist.'       
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @phoneN IS NOT NULL AND @name_ID IS NOT NULL AND EXISTS (SELECT phone_number from phoneNumber where phone_number = @phoneN AND name_id = @name_ID )
                Begin
                        --Delete Phone number
                        DELETE from phoneNumber where phone_number = @phoneN AND name_id = @name_ID
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