CREATE OR ALTER PROCEDURE insert_2(
                            @name_ID as INT           = 0   ,
                            @fname   as NVARCHAR(50)        ,
                            @lname   as NVARCHAR(50)  = ''  ,
                            @phoneN  as NVARCHAR(50)  = ''  ,
                            @email   as NVARCHAR(50)  = ''  ,
                            @addr    as NVARCHAR(200) = ''  ,
                            @g_id    as SMALLINT =1         ,
                            @typ_id  as SMALLINT = 1
                                    )
/*
-Insert a new contact or insert to @name_ID contact if it existed 
    with phone number, email and address or just one or 
    combination of them .

-Input parameters: @name_ID, @fname(must be),  @lname, @phoneN, 
                    @email, @addr, @g_id(group), @typ_id(type).

-Output: result message.    @which+' inserting_done':OK.
                            'Problems!,name ID dont exist.'
                            ERROR_MESSAGE():Error     
*/
as 
BEGIN
DECLARE @thisNameID INT =0;
DECLARE @which VARCHAR(10) ='';  -- It shows which components inserted.

    BEGIN TRANSACTION  --transaction
        BEGIN TRY   --try catch

            IF @name_ID = 0  --insert new contact
                BEGIN
                    insert into names (first_name,last_name,group_id) values (@fname,@lname,@g_id);
                    set @thisNameID = (select IDENT_CURRENT('names'));
                    SET @which = 'N'+' '
                END
            ELSE            --insert existed contact
                BEGIN
                    IF NOT EXISTS ( SELECT id FROM names where id = @name_ID)
                        THROW 51000 , N'Problems!,name ID dont exist.' , 1 ;
                    ELSE
                         set @thisNameID = @name_ID  --set existed name ID and continue.
                END



            IF @phoneN <>'' AND @phoneN <>' '
            BEGIN
                insert into phoneNumber (phone_number,name_id,type_id) values (@phoneN,@thisNameID ,@typ_id);
                SET @which = @which +'P'+' '
            END

            IF @email <>'' AND @email <>' '
            BEGIN
                insert into email (email,name_id,type_id) values (@email,@thisNameID,@typ_id);
                SET @which = @which +'E'+' '
            END

            IF @addr <>'' AND @addr <>' '
            BEGIN
                insert into Address (Address,name_id,type_id) values (@addr,@thisNameID,@typ_id);
                SET @which = @which +'A'
            END

            COMMIT TRANSACTION
            select @which+' inserting_done' as ch_message
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message  
        END CATCH

END