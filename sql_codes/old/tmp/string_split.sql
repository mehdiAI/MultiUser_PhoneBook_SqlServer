
DECLARE @nnid as VARCHAR(max)=' 1001 1057 1058 1060 ';


-- collect name Ids into @nid table that related to fname and lname .
--insert into @nid SELECT id from names where first_name LIKE '%'+@fname+'%' AND last_name LIKE '%'+@lname+'%' ;
--SELECT @nnid = @nnid + CONVERT(varchar(max),id)+' ' from names where first_name LIKE '%'+@fname+'%' AND last_name LIKE '%'+@lname+'%' ;
SELECT @nnid as 'nnid'
print @nnid
select value from STRING_SPLIT(@nnid,' ');
select SUBSTRING(@nnid,CHARINDEX(' ',@nnid),len(@nnid)) as substring
select LEFT(@nnid, CHARINDEX(' ',@nnid)-1) as LLLLL

