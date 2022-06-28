USE PhoneBook
SELECT n.first_name , n.last_name , p.phone_number , e.email , a.Address
FROM names AS n , phoneNumber AS p , email as e , address as a
WHERE n.id = p.name_id AND n.id = e.name_id AND n.id = a.name_id and n.id<20 order by n.first_name;
go