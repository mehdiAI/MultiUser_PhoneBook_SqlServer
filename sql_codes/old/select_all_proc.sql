CREATE PROCEDURE select_all (@limit as INT = NULL,
                             @fname as nvarchar(50) = NULL ,
                             @lname as nvarchar(50) = NULL
                                                    ) 
as
BEGIN
    SELECT n.first_name , n.last_name , p.phone_number , e.email , a.Address
    FROM names AS n , phoneNumber AS p , email as e , address as a
    WHERE n.id = p.name_id AND n.id = e.name_id AND n.id = a.name_id and 
    (@limit is null or n.id <= @limit ) AND (@fname is null or n.first_name like @fname+'%') 
    AND (@lname is null or n.last_name like @lname+'%')  
    order by n.first_name ;

END;