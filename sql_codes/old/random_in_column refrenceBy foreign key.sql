--Find the Foreign Key Constraint with Table Name
    USE PhoneBook
    GO
    Select 
    Schema_name(Schema_id) as SchemaName,
    object_name(Parent_object_id) as TableName,
    name as ForeignKeyConstraintName
    from sys.foreign_keys

--Disable Foregin Key by using NOCHECK
ALTER TABLE phoneNumber
NOCHECK CONSTRAINT FK__phoneNumb__type___06CD04F7

--Run Update Statements
update phoneNumber
set type_id = (CRYPT_GEN_RANDOM(2) % 6)
where type_id = 1 ;



--Enable Foreign Key Constraint by using CHECK
ALTER TABLE phoneNumber
CHECK CONSTRAINT FK__phoneNumb__type___06CD04F7