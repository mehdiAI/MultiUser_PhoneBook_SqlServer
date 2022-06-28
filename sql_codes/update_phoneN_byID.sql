CREATE or alter PROCEDURE update_phoneN_byID( @phoneNID as INT ,@phoneN as NVARCHAR(50) )
/*
-update specific Phone number by specific phone ID IF Phone number ID exist.
-Input parameters: @phoneNID , @phoneN .
-Output: result message.    1-'phoneN_updating_done':OK
                            2-'Problems!,Phone number ID dont exist.'
                            3-'Problems!,@phoneN is empty or params are null.'

*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @phoneNID IS NOT NULL AND @phoneN IS NOT NULL AND  @phoneN <> '' AND @phoneN <> ' ' 
                BEGIN

                        IF  EXISTS (SELECT phoneN_id from phoneNumber where phoneN_id = @phoneNID )
                        BEGIN
                                --Update Phone number
                                UPDATE  phoneNumber SET phone_number = @phoneN WHERE phoneN_id = @phoneNID
                                select 'phoneN_updating_done' as ch_message
                        END   
                        ELSE
                            THROW 51000 , N'Problems!,Phone number ID dont exist.' , 1 ; 
                END
            ELSE
                THROW 51000 , N'Problems!,@phoneN is empty or params are null.' , 1 ; 
                
        COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END