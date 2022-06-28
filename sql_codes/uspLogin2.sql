CREATE OR ALTER PROCEDURE uspLogin2 (@pLoginName NVARCHAR(50),@pPassword NVARCHAR(50) )
/*
-login by username and password after that return message and level number.
-input params:  @pLoginName, @pPassword
-output :       'Incorrect password'
                'User successfully logged in',user data -> OK
                'Invalid login'
*/
AS
BEGIN

    SET NOCOUNT ON

    DECLARE @userID INT
    DECLARE @level INT

    IF EXISTS (SELECT TOP 1 UserID FROM [dbo].[User] WHERE LoginName=@pLoginName)
    BEGIN
        SET @userID=(SELECT UserID FROM [dbo].[User] WHERE LoginName=@pLoginName AND PasswordHash=HASHBYTES('SHA2_512', @pPassword))
         
       IF(@userID IS NULL)
           select 'Incorrect password' as ch_message
       ELSE 
       BEGIN
            --SET @level = (SELECT levels FROM [dbo].[User] WHERE UserID = @userID)
            --SELECT 'User successfully logged in' +','+CONVERT(varchar(10),@userID)+','+CONVERT(varchar(10),@level) as ch_message
            SELECT 'User successfully logged in' as ch_message , UserID ,LoginName, PhoneBook_name , levels from [User] where UserID = @userID
        END
    END
    ELSE
       select 'Invalid login' as ch_message

END