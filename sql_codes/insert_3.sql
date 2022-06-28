CREATE OR ALTER PROCEDURE insert_3(
                            @name_ID as INT           = 0   ,
                            @UserID as INT            = 0   ,
                            @fname   as NVARCHAR(50)        ,
                            @lname   as NVARCHAR(50)  = ''  ,
                            @g_id    as SMALLINT      = 1   , 
                            @phoneN  as NVARCHAR(50)  = ''  ,
                            @Pntyp_id  as SMALLINT    = 1   ,
                            @email   as NVARCHAR(50)  = ''  ,
                            @Emtyp_id  as SMALLINT    = 1   ,
                            @addr    as NVARCHAR(200) = ''  ,
                            @Addrtyp_id  as SMALLINT  = 1   
                                  
                                    )
/*
-Insert a new contact or insert to @name_ID contact if it existed 
    with phone number, email and address or just one or 
    combination of them .

-Input parameters: @name_ID, @UserID, @fname(must be), @lname, @g_id(group),
                    @phoneN, @Pntyp_id, @email, @Emtyp_id, @addr, @Addrtyp_id .

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
                    insert into names (first_name,last_name,group_id,UserID) values (@fname,@lname,@g_id,@UserID);
                    set @thisNameID = (select IDENT_CURRENT('names'));
                    SET @which = 'N'+','
                END
            ELSE            --insert existed contact
                BEGIN
                    IF NOT EXISTS ( SELECT id FROM names where id = @name_ID)
                        THROW 51000 , N'Problems!,name ID dont exist.' , 1 ;
                    ELSE
                    BEGIN
                         set @thisNameID = @name_ID  --set existed name ID and continue.
                         SET @which = 'N_EXIST'+','
                    END
                END



            IF @phoneN <>'' AND @phoneN <>' '
            BEGIN
                insert into phoneNumber (phone_number,name_id,type_id) values (@phoneN,@thisNameID ,@Pntyp_id);
                SET @which = @which +'P'+','
            END

            IF @email <>'' AND @email <>' '
            BEGIN
                insert into email (email,name_id,type_id) values (@email,@thisNameID,@Emtyp_id);
                SET @which = @which +'E'+','
            END

            IF @addr <>'' AND @addr <>' '
            BEGIN
                insert into Address (Address,name_id,type_id) values (@addr,@thisNameID,@Addrtyp_id);
                SET @which = @which +'A'+','
            END

            COMMIT TRANSACTION
            select @which+CONVERT(nvarchar(max),@thisNameID) +','+'inserting_done' as ch_message
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            select ERROR_MESSAGE() as ch_message  
        END CATCH

END