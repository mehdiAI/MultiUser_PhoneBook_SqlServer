use PhoneBook
select names.first_name , names.last_name , phoneNumber.phone_number , email.email, Address.Address
from names 
full outer JOIN phoneNumber
ON phoneNumber.name_id = names.id
full outer JOIN email
ON email.name_id = names.id
full outer JOIN Address
ON Address.name_id = names.id
where names.id>999
order by names.first_name
