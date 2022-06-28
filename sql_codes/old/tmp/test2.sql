--exec insert_all @fname = N'آرش' , @lname= N'کیان', @phoneN='0912 45 85 698' , @email = 'qqqq12@yahoo.com'
--exec insert_all @fname = N'a' , @lname= N'bb', @phoneN='155555511' , @email = 'wwww@yahoo.com' , @addr= 'qqqqqqqqqqqqqqqqqq'
--exec update_row @name_ID =1014 , @fname_n='reza'  , @lname_n = 'Ahmadigggggffvvvv' , @addr='wwwe@ffhfh.com' , @addr_n ='wwewe@yahoo.com'
--exec update_row @fname='alina' , @lname = 'lye'  , @lname_n = 'martin'
exec update_row @name_ID=500 , @phoneN = '0935 45 85 45' , @phoneN_n = '0935 11111111' , @email_n='fddfkldjfldjf' , @email ='fjjgjfgkj'
--exec  delete_row @del_state ='pead' , @phoneN = '45656655' , @email= '989565@yahoo.com'
--exec delete_row @fname= 'a' , @lname= 'bb'
--exec delete_row @name_ID=1043