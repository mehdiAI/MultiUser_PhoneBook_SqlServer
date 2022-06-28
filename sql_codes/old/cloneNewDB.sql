
SET NOCOUNT ON
BEGIN TRY


        dbcc clonedatabase (PhoneBook,Admin2_PhoneBook);
        alter DATABASE Admin2_PhoneBook set READ_WRITE with no_wait;

        select 'Success' as ch_message;
END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() as ch_message
END CATCH


