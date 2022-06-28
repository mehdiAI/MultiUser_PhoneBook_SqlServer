CREATE PROCEDURE dbo.uspAddUser
    @pLogin NVARCHAR(50), 
    @pPassword NVARCHAR(50), 
    @pFirstName NVARCHAR(40) = NULL, 
    @pLastName NVARCHAR(40) = NULL,
    @responseMessage NVARCHAR(250) OUTPUT
AS
BEGIN
    SET NOCOUNT ON

    BEGIN TRY
            IF not EXISTS (SELECT * from dbo.[User] where LoginName=@pLogin)
            BEGIN

                INSERT INTO dbo.[User] (LoginName, PasswordHash, FirstName, LastName)
                VALUES(@pLogin, HASHBYTES('SHA2_512', @pPassword), @pFirstName, @pLastName)

            
                SET @responseMessage='Success'

            END
            ELSE
                THROW 51000,'loginName existed',1;

    END TRY
    BEGIN CATCH
        SET @responseMessage=ERROR_MESSAGE() 
    END CATCH

END