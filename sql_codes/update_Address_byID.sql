CREATE or alter PROCEDURE update_Address_byID( @addrID as INT ,@Naddr as NVARCHAR(50) )
/*
-update specific address by specific address ID IF address ID exist.
-Input parameters: @addrID , @Naddr .
Output: result message.     1-'Address_updating_done':OK
                            2-'Problems!,Address ID dont exist.'
                            3-'Problems!,@Naddr is empty or params are null.'   
*/
AS
BEGIN
    BEGIN TRANSACTION
        BEGIN TRY
            IF @addrID IS NOT NULL AND @Naddr IS NOT NULL AND  @Naddr <> '' AND @Naddr <> ' ' 
                BEGIN
                            
                        IF  EXISTS (SELECT Address_id from Address where Address_id = @addrID )
                        BEGIN
                                --Update email
                                UPDATE  Address SET Address = @Naddr WHERE Address_id = @addrID
                                select 'Address_updating_done' as ch_message
                        END   
                        ELSE
                            THROW 51000 , N'Problems!,Address ID dont exist.' , 1 ; 


                END
            ELSE
                THROW 51000 , N'Problems!,@Naddr is empty or params are null.' , 1 ; 
                
        COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END