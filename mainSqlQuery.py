
class sql_mssql_class():
    def __init__(self,pyodbc,
                driver:str,
                server:str,
                port:str,
                UID:str,
                PWD:str,
                loginDatabase:str):
        
        #self.pyodbc = pyodbc
        # this variables needed for connection to datbase py pyodbc pakage.
        self.driver = driver
        self.server = server
        self.port = port
        self.UID = UID
        self.PWD = PWD
        self. loginDatabase = loginDatabase
        
        #structure of conecction needed string for pyodbc.connect()
        self.cnctlog = ("DRIVER=" + self.driver
        + ";SERVER=" + self.server
        +";PORT="+ self.port
        + ";DATABASE=" + loginDatabase    # get this from out of class by object argumns
        + ";UID=" + UID
        + ";PWD=" + PWD
        + ";Trusted_connection=no")
        print('cnctlog string created!')
        
    def readGroups(self,MConn:object):
        """ -Get group names and its ids from groups table.

        Args:
            MConn (object): a connection object for executing query and command for main database.

        Returns:
            -return groupID , group from groups table
            -return nothing.
        """  
        #for more info about return(a list of tuple) structure see phonebook database.
        #create cursor for execution query and command for database. 
        cursor = MConn.cursor()
        return cursor.execute("select * from groups").fetchall()
    def readTypes(self,MConn:object):
        """ -Get types name and its id from type table.

        Args:
            MConn (object): a connection object for executing query and command for main database.

        Returns:
            -return typeID , type from types table
            -return nothing.
        """  
        #for more info about return(a list of tuple) structure see phonebook database.
        #create cursor for execution query and command for database. 
        cursor = MConn.cursor()
        return cursor.execute("select * from types").fetchall()

    def searchby_name_id_flname(self,MConn:object,name_id:int):
        """ -Search names by name_id(id of a contact in names table) related to a contact.

        Args:
            MConn (object): a connection object for executing query and command for main database.
            name_id (int): id of a contact in names table.

        Returns:
            -return id ,firstName lastName , groupID , UserID from names table
            -return nothing.
        """  
        #for more info about return(a list of tuple) structure see phonebook database.
        #create cursor for execution query and command for database. 
        cursor = MConn.cursor()
        return cursor.execute("select * from names where id =?",name_id).fetchall()

    def searchby_name_id_phoneN(self,MConn:object,name_id:int):
        """ -Search phone number by name_id(id of a contact in names table) related to a contact.

        Args:
            MConn (object): a connection object for executing query and command for main database.
            name_id (int): id of a contact in names table.

        Returns:
            -return phoneN_id , phone_number from phoneNumber table
            -return nothing.
        """  
        #for more info about return(a list of tuple) structure see phonebook database.
        #create cursor for execution query and command for database. 
        cursor = MConn.cursor()
        return cursor.execute("select phoneN_id , phone_number from phoneNumber where name_id =?",name_id).fetchall()
    def searchby_name_id_email(self,MConn:object,name_id:int):
        """ -Search email by name_id(id of a contact in names table) related to a contact.

        Args:
            MConn (object): a connection object for executing query and command for main database.
            name_id (int): id of a contact in names table.

        Returns:
            -return email_id,email from email table
            -return nothing.
        """  
        #for more info about return(a list of tuple) structure see phonebook database.
        #create cursor for execution query and command for database. 
        cursor = MConn.cursor()
        return cursor.execute("select email_id,email from email where name_id =?",name_id).fetchall()
    def searchby_name_id_Addr(self,MConn:object,name_id:int):
        """
        -Search addresses by name_id(id of a contact in names table) related to a contact. 
        -Parameters: 
            -MConn: a connection object for executing query and command for main database.
            -name_id: id of a contact in names table.
            
        -returns:
            -return Address_id , Address from Address table
            -return nothing.
        """
        #for more info about return(a list of tuple) structure see phonebook database.
        #create cursor for execution query and command for database. 
        cursor = MConn.cursor()
        return cursor.execute("select Address_id , Address from Address where name_id =?",name_id).fetchall()
        
    def insert_row(self,Mconn:object,name_ID:int=0,UserID:int=0,fname:str='',lname:str='',g_id:int=1,
                    phoneN:str='',Pntyp_id:int=1,email:str='',Emtyp_id:int=1,addr:str='',Addrtyp_id:int=1):
        """
        -Insert method for inserting new contact(name,PhoneN,email,address) separately or all of them thogether or insert to existed contact.
            -For adding new contact need name_ID=0 otherwise phoneN email and address will add to names with ID= name_ID .
            -If every phoneN ,email and addtess become empty or -''- this filed will ignore . 
            -Attention for adding new contact 'fname' is needed atleast . 
            -If name_ID!= 0 , fname,lname and g_id will ignore. 
            -for mor info refer to [dbo].[insert_3] procedure in PhoneBook database. 
        -Parameters: 
            -Mconn: a connection object for executing query and command for main database.
            -name_ID: id of a contact in names table. 
            -UserID: ID of a user . 
            -fname: first name.
            -lname: lasr name.
            -g_id: groupID.
            -phoneN: .
            -Pntyp_id: Phone type.
            -email: .
            -Emtyp_id: email type .
            -addr:  .
            -Addrtyp_id: address type .
            
        -returns:
            -return True,dataSplited ,'ok' - (result message)
            -return False,data[0][0], 'There are problems for inserting!' - (result message)
        """
            
        sql = """
                SET NOCOUNT ON  
                exec [dbo].[insert_3] @name_ID=? , @UserID=? , @fname=? , @lname=? ,@g_id=? , 
                                        @phoneN=? , @Pntyp_id=? , @email=? ,@Emtyp_id=? , @addr=? , @Addrtyp_id=?
        
        """
        #for more info 'data'(a list of tuple) structure see '[dbo].[insert_3]' procedure.
        #create cursor for execution query and command for database. 
        cursor = Mconn.cursor()
        data = cursor.execute(sql,(name_ID,UserID,fname,lname,g_id,phoneN,Pntyp_id,email,Emtyp_id,addr,Addrtyp_id)).fetchall()
        print('message after inserting executation: ',data[0][0])
        
        if 'inserting_done' in data[0][0]:  # approvment inserting.
            Mconn.commit()
            dataSplited = data[0][0].split(',')
            print('insert resposed data:',dataSplited)
            return True,dataSplited ,'ok'   
        else:
            return False,data[0][0], 'There are problems for inserting!'

    def delete_row(self,Mconnection:object,Name_ID:int):
        delSql = """
                        SET NOCOUNT ON
                        EXECUTE [dbo].[delete_row2] ?
        """
        state = [()]
        cursor = Mconnection.cursor()
        state = cursor.execute(delSql,(Name_ID)).fetchall()
        #cursor.execute("delete from names where id = {}".format(Name_ID))
        if state[0][0] == 'Row_deleting_done':       
            cursor.commit()
            print("deleteRow state : " , state[0][0])
            return True, state[0][0]
        else:
            return False, state[0][0]

    def delete_phoneN_byID(self,Mconnection:object,PhoneN_ID:int):
        """
        -Delete a phone number by phoneN id in phoneNumber table.
        -Parameters: 
            -Mconnection: a connection object for executing query and command for main database.
            -PhoneN_ID: ID of a phone number in phoneNumber table.
            
        -returns:
            -return True , state[0][0] (result message)
            -return False , state[0][0] (result message)
        """
        delSql = """
                        SET NOCOUNT ON
                        EXECUTE [dbo].[del_phoneN_byID] ?
        """
        state = [()]
        #for more info 'state'(a list of tuple) structure see 'update_Address_byID' procedure.
        #create cursor for execution query and command for database. 
        cursor = Mconnection.cursor()
        state = cursor.execute(delSql,(PhoneN_ID)).fetchall()
        if state[0][0] == 'phoneN_deleting_done':       
            cursor.commit()
            print("deletePhoneN state : " , state[0][0])
            return True , state[0][0]
        else:
            return False , state[0][0]
    def delete_email_byID(self,Mconnection:object,email_ID:int):
        """
        -Delete an email by email id in email table.
        -Parameters: 
            -Mconnection: a connection object for executing query and command for main database.
            -email_ID: ID of an email in email table.
            
        -returns:
            -return True , state[0][0] (result message)
            -return False , state[0][0] (result message)
        """
        delSql = """
                        SET NOCOUNT ON
                        EXECUTE [dbo].[del_email_byID] ?
        """
        state = [()]
        #for more info 'state'(a list of tuple) structure see 'del_email_byID' procedure.
        #create cursor for execution query and command for database. 
        cursor = Mconnection.cursor()
        state = cursor.execute(delSql,(email_ID)).fetchall()
        if state[0][0] == 'Email_deleting_done':       
            cursor.commit()
            print("deleteEmail state : " , state[0][0])
            return True , state[0][0]
        else:
            return False , state[0][0]
    def delete_address_byID(self,Mconnection:object,address_ID:int):
        """
        -Delete an address by Address id in Address table.
        -Parameters: 
            -Mconnection: a connection object for executing query and command for main database.
            -address_ID: ID of an address in Address table.
            
        -returns:
            -return True , state[0][0] (result message)
            -return False , state[0][0] (result message)
        """
        delSql = """
                        SET NOCOUNT ON
                        EXECUTE [dbo].[del_Address_byID] ?
        """
        state = [()]
        #create cursor for execution query and command for database. 
        cursor = Mconnection.cursor()
        #for more info 'state'(a list of tuple) structure see 'del_Address_byID' procedure.
        state = cursor.execute(delSql,(address_ID)).fetchall()
        if state[0][0] == 'Address_deleting_done':       
            cursor.commit()
            print("deleteAddress state : " , state[0][0])
            return True , state[0][0]
        else:
            return False , state[0][0]

    def update_phoneN_byID(self,Mconnection:object,PhoneN_ID:int ,PhoneN:str):
        
        """
        -Update a phone number by phoneNumber id in phoneNumber table.
        -Parameters: 
            -Mconnection: a connection object for executing query and command for main database.
            -PhoneN_ID: ID of an phonne number in phoneN table.
            -PhoneN: .
            
        -returns:
            -return True , state[0][0] (result message)
            -return False , state[0][0] (result message)
        """
        updateSql = """
                        SET NOCOUNT ON
                        EXECUTE [dbo].[update_phoneN_byID] ? , ?
        """
        state = [()]
        #create cursor for execution query and command for database. 
        cursor = Mconnection.cursor()
        #for more info 'state'(a list of tuple) structure see 'update_phoneN_byID' procedure.
        state = cursor.execute(updateSql,(PhoneN_ID,PhoneN)).fetchall()
        if state[0][0] == 'phoneN_updating_done':       
            cursor.commit()
            print("Update PhoneN state : " , state[0][0])
            return True , state[0][0]
        else:
            return False , state[0][0]
        
    def update_email_byID(self,Mconnection:object,email_ID:int ,newEmail:str):
        """
        -Update an email by email id in email table.
        -Parameters: 
            -Mconnection: a connection object for executing query and command for main database.
            -email_ID: ID of an email in email table.
            -newEmail: .
            
        -returns:
            -return True , state[0][0] (result message)
            -return False , state[0][0] (result message)
        """

        updateSql = """
                        SET NOCOUNT ON
                        EXECUTE [dbo].[update_email_byID] ? , ?
        """
        state = [()]
        #create cursor for execution query and command for database. 
        cursor = Mconnection.cursor()
        #for more info 'state'(a list of tuple) structure see 'update_email_byID' procedure.
        state = cursor.execute(updateSql,(email_ID,newEmail)).fetchall()
        if state[0][0] == 'Email_updating_done':       
            cursor.commit()
            print("Update Email state : " , state[0][0])
            return True , state[0][0]
        else:
            return False , state[0][0]
        
    def update_Address_byID(self,Mconnection:object,Address_ID:int ,NewAddress:str):
        """
        -Update an address by Address id in Address table.
        -Parameters: 
            -Mconnection: a connection object for executing query and command for main database.
            -Address_ID: ID of an address in Address table.
            -NewAddress: .
            
        -returns:
            -return True , state[0][0] (result message)
            -return False , state[0][0] (result message)
        """
        
        updateSql = """
                        SET NOCOUNT ON
                        EXECUTE [dbo].[update_Address_byID] ? , ?
        """
        state = [()]
        #create cursor for execution query and command for database. 
        cursor = Mconnection.cursor()
        state = cursor.execute(updateSql,(Address_ID,NewAddress)).fetchall()
        #for more info 'state'(a list of tuple) structure see 'update_Address_byID' procedure.
        if state[0][0] == 'Address_updating_done':       
            cursor.commit()
            print("Update Address state : " , state[0][0])
            return True , state[0][0]
        else:
            return False , state[0][0]

    
    def searchShow(self,Mconnection:object,fname:str='',lname:str='',UserID:int=0):
        """
        -Show data in search section base on first name and last name and userID.
        -Parameters: 
            -Mconnection: a connection object for executing query and command for main database.
            -fname: first name.
            -lname: last name.
            -UserID: .
            
        -returns:
            - return data related 'dbo.search_join_byUserID' proc and first name, last name, UserID.
            -return ERROR_MESSAGE() from database engin.
        """
        
        cursor = Mconnection.cursor()
        return cursor.execute("{CALL dbo.search_join_byUserID (?,?,?)}",(UserID,fname,lname)).fetchall()
    
    def add_signUp(self,logConn:object,Nusername:str,Npassword:str,PhBook_name:str,Creator_name:str,level:int):

        accessLevel = {'High':2,'Medium':1,'Low':0}
        """
        -Create new account.
        -Parameters: 
            -logConn: a connection object for executing query and command for login database.
            -Nusername: new user name.
            -Npassword: .
            -PhBook_name: .
            -Creator_name: .
            -level: level of this new user.
            
            
        -returns:
            - return True,'user_added'.
            -return False, 'user_added_failed'.
        """
        signIn_sql =   """
                SET NOCOUNT ON 
                EXEC [dbo].[uspAddUser2]
                                @UsrLogin = ?, 
                                @UsrPassword = ?, 
                                @PhBook_name = ?, 
                                @Creator_name = ?,
                                @level = ?
                    """
        #create cursor for execution query and command for database.        
        cursor = logConn.cursor()
        #create  new user . for more info 'state'(a list of tuple) structure see 'uspAddUser2' procedure.
        state = cursor.execute(signIn_sql,(Nusername,Npassword,PhBook_name,Creator_name,level)).fetchall()
        logConn.commit()

        approvedNname = cursor.execute("select UserID , loginName from [dbo].[User] where loginName = ?",Nusername).fetchall()
        print('user adding state: ',state[0][0])
        print('new user approved name: ',approvedNname[0])      # approvedNname[0] = (UserID,UserName)
        
        if state[0][0] == 'Success' and approvedNname[0][1] == Nusername:
            return True,'user_added'
        else:
            return False, 'user_added_failed'
    
    def login(self,username:str,password:str,logConn:object):
        """
        -Checking username and password stored in database for each users for logIn section..
        -Parameters: 
            -username: user name or ligin name.
            -password: .
            -logConn: a connection object for executing query and command for login database.
            
        -returns:
            - return True , cnctPB(connection string needed for "pyodbc"),
                [UserID, LoginName, PhoneBook_name, level] ,Usertable(Users that can shown in this user.).
            -return False ,'','','',[''].
        """
        
        Login_sql = """
                --checking login and password
                SET NOCOUNT ON 
                EXEC	dbo.uspLogin2
                        @pLoginName =  ?,
                        @pPassword =  ?
            """      
        #create cursor for execution query and command for database.
        cursor = logConn.cursor()
        #execute procedure and get state. state(a list of tuple) consist of result execution that use it in approvemnt.
        # for detail of state structure should read 'dbo.uspLogin2' proc.
        state = cursor.execute(Login_sql,(username,password)).fetchall()
        print('login state: ',state[0])
        check_msg = state[0][0]

        
        if check_msg == 'User successfully logged in':
            
            UserID = state[0][1]
            LoginName = state[0][2]
            PhoneBook_name = state[0][3]
            level = state[0][4]
            if level!= 0:  # High level user
                Usertable = cursor.execute('SELECT UserID, LoginName, PhoneBook_name from [User] ').fetchall()
            else: #Users have level=0
                Usertable =cursor.execute('SELECT UserID, LoginName, PhoneBook_name from [User] where UserID=0 or UserID =?',int(UserID)).fetchall()
            print('check message from login section: ', check_msg )
            cnctPB = ("DRIVER=" + self.driver
                + ";SERVER=" + self.server
                +";PORT="+self.port
                + ";DATABASE=" + 'PhoneBook'
                + ";UID=" + self.UID
                + ";PWD=" + self.PWD
                + ";Trusted_connection=no")
            
            return True , cnctPB, [UserID, LoginName, PhoneBook_name, level] ,Usertable
        else:
            return False ,'','','',['']
        
    def deleteUser(self,DelUserID:int,substitute_UserID:int,logConn:object,Mconnection:object):
        """
        -Delete a user by high level users and transfer that user to another user.
        -parameters: 
            -DelUserID: ID of user that want to delete.
            -substitute_UserID: ID of user that want to substitute.
            -logConn: a connection object for executing query and command for login database.
            -Mconnection: a connection object for executing query and command for main(PhonBook) database.
            
        -returns:
            -return False , 'deleteUser problem!It can not connect to database!'.
            -return True , 'ok'.
            -return False , 'removeState problem!'. 
            -return False , 'updateState problem!'.
        """
        #create cursor for execution query and command for database.
        logcursor = logConn.cursor()
        MconnCursor = Mconnection.cursor()
        #Get data needed from User table.
        state_Users =  logcursor.execute("SELECT UserID,LoginName,PhoneBook_name,Creator_name,levels from [User]").fetchall()
        print('state_DelUser from deleteUser func: ',state_Users)
        ch_DelUserID =False
        ch_substitute_UserID =False
        #checking for exist users or not in user table.
        if len(state_Users)>1:
            for item in state_Users:
                if item[0]==DelUserID:
                    ch_DelUserID =True
                    break
            for item in state_Users:
                if item[0]==substitute_UserID:
                    ch_substitute_UserID =True
                    break
        else:
            print('deleteUser problem!It can not connect to database!')
            return False , 'deleteUser problem!It can not connect to database!'
        
        print('from deleteUser-> ch_DelUserID: ',ch_DelUserID)
        print('from deleteUser-> ch_DelUserID: ',ch_substitute_UserID)
        updateSql = """
            SET NOCOUNT ON
            UPDATE names SET UserID =? WHERE UserID =?
            select 'Data_Updating_done' as ch_message
        """
        removingSql = """
            SET NOCOUNT ON
            DELETE from [User] WHERE UserID =?
            select 'User_Removing_done' as ch_message
        """
        #transfer data by updating UserID column in [names] table.
        #After that remove delUser.
        updateState = MconnCursor.execute(updateSql,(substitute_UserID,DelUserID)).fetchall()
        removeState = []
        if updateState[0][0] =='Data_Updating_done':
            removeState=logcursor.execute(removingSql,(DelUserID)).fetchall()
            print('removeState: ', removeState)
            if removeState[0][0]=='User_Removing_done':
                MconnCursor.commit()
                logcursor.commit()
                return True , 'ok'
            else:
                return False , 'removeState problem!'
        else:
            return False , 'updateState problem!'
            
        
        