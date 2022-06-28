--SELECT FLOOR(RAND()*(b-a+1))+a;

--SELECT FLOOR(RAND()*(5-1+1))+1;

update phoneNumber
set type_id = (CRYPT_GEN_RANDOM(2) % 6)
where type_id = 1 ;

--select CAST(CRYPT_GEN_RANDOM(4) as tinyint)/10  ;
--select CRYPT_GEN_RANDOM(2) % 6;