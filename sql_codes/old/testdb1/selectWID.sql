create PROCEDURE selectWID(
    @id as int =0
)

as
BEGIN
    IF @id = 0
    BEGIN
        SELECT * from inventory;
    END
    ELSE
    BEGIN
        SELECT * from inventory WHERE id =@id;
    END


END