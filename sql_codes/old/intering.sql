DECLARE @responseMessage NVARCHAR(250)
/*
EXEC dbo.uspAddUser
          @pLogin = N'Admin',
          @pPassword = N'12345@',
          @pFirstName = N'Admin',
          @pLastName = N'test2',
          @responseMessage=@responseMessage OUTPUT
*/

EXEC dbo.uspAddUser
          @pLogin = 'Admin8',
          @pPassword = '1222',
          @pFirstName = 'Admin8',
          @pLastName = 'test8',
          @responseMessage=@responseMessage OUTPUT


SELECT *
FROM [dbo].[User]

select @responseMessage as ch_message