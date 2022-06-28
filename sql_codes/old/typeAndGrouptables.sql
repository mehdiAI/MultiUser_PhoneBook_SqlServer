SELECT TOP (1000) [type_id]
      ,[t_name]
  FROM  [dbo].[types]

 SELECT TOP (1000) [group_id]
      ,[g_name]
  FROM  [dbo].[groups] 

alter DATABASE Admin2_PhoneBook set READ_WRITE with no_wait;

SET IDENTITY_INSERT [dbo].[types] ON
INSERT into [dbo].[types] (type_id, t_name) values (1,'Not assigned') ,(2,'Home') ,(3,'Work') ,(4,'main') ,(5,'Other')
SET IDENTITY_INSERT [dbo].[types] OFF

SET IDENTITY_INSERT [dbo].[groups] ON
INSERT into [dbo].[groups] (group_id, g_name) values (1,'Not assigned') ,(2,'Emergency contacts') ,
                                                    (3,'Colleagues') ,(4,'Family') ,(5,'Friends') ,(6,N'تست فارسی')
SET IDENTITY_INSERT [dbo].[groups] OFF