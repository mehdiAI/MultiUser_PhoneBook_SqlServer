CREATE OR ALTER PROCEDURE  uspAddUser2 (
                                @UsrLogin NVARCHAR(50), 
                                @UsrPassword NVARCHAR(50), 
                                @PhBook_name NVARCHAR(50), 
                                @Creator_name NVARCHAR(50),
                                @level TINYINT
                                   )
/*
-Sign up new user and creare new PhoneBook.
-input params:  @UsrLogin, @UsrPassword, @PhBook_name, @Creator_name .
-output :       
                'Success -> OK
                'loginName existed'
*/

AS
BEGIN
    SET NOCOUNT ON
    BEGIN TRANSACTION
        BEGIN TRY
                IF not EXISTS (SELECT * from  [User] where LoginName=@UsrLogin)
                BEGIN

                    INSERT INTO  [User] (LoginName, PasswordHash, PhoneBook_name, Creator_name , levels)
                    VALUES(@UsrLogin, HASHBYTES('SHA2_512', @UsrPassword), @PhBook_name, @Creator_name,@level)

                
                    select 'Success' as ch_message

                END
                ELSE
                    THROW 51000,'loginName existed',1;

                COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message
        END CATCH

END