create proc insertNEW (
        @name as NVARCHAR(50),
        @q as int=NULL
)

as 

BEGIN
        INSERT into inventory (name,quantity) VALUES (@name, @q)
END