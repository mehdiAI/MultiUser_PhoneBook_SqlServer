
import pyodbc as db
from mainSqlQuery import sql_mssql_class
import sys

from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import (QDialog , QApplication ,QMainWindow , QPushButton, QLineEdit, 
                                QMessageBox , QLabel ,QComboBox , QTabWidget ,QInputDialog)
from PyQt5.uic import loadUi

#All parameters need for connect to sql server database
driver = "{ODBC Driver 17 for SQL Server}"
server = "127.0.0.1"
port ='1433'
Mdatabase = ''
LoginDatabase = 'pufi'
username = "sa"
password = "7202@fasa"
cnctStringMdb= ' '   #main connection string for connection, this string will complete from sql_mssql_class.

UserLevel=' '
thisUser =[]   #[UserID, LoginName, PhoneBook_name, level] fo this user login.
Users =[]      #All of Users -> [UserID, LoginName, PhoneBook_name]. It a list of tuple.

#extract from tableWidget in main window when select a contact.
name_id = 0   # It is usen in showing, updating, deletimg and inserting to existed account.
WhichWin = 'mainWin'  #It use to detect which window come to inserting.
accessLevel = {'High':2,'Medium':1,'Low':0} #level od Users.
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.setFixedWidth(980)
        self.setFixedHeight(620)
        
        
        # initilize sql object for query#####################################################
        self.sqlQery = sql_mssql_class(db,driver,server,port,username,password,LoginDatabase) 
        print('logConnection string: ', self.sqlQery.cnctlog)
        self.logconn = db.connect(self.sqlQery.cnctlog)
        ###################################################################################
        
        #self.loginBtn = self.findChild(QPushButton, "loginBtn")
        #self.LiUNbx = self.findChild(QLineEdit, "LiUNbx")
        #self.LiPwdbx = self.findChild(QLineEdit, "LiPwdbx")
        self.loginBtn.clicked.connect(self.checkingLoggin)  #LogIn Button
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        
    def checkingLoggin(self):
        #get LoginName and password from texe line and check it.
        infologin = self.sqlQery.login(self.LiUNbx.text(), self.LiPwdbx.text(),self.logconn)
        print('info login: ',infologin)
        # chcking and set some variables specially globaly that need for another classes.
        if infologin[0]:
            global cnctStringMdb
            cnctStringMdb = infologin[1]
            global thisUser
            thisUser = infologin[2]
            global UserLevel
            UserLevel = thisUser[3]
            global Users
            Users = infologin[3]
            print('UserLevel: ', UserLevel)
            print('Login this user: ', thisUser)
            print('Users: ', Users)
            self.logconn.close()
            mainW=mainWin()
            widget.addWidget(mainW)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            print('Login failed!')
            self.msg.setText( "User name or password is not correct!")
            self.msg.exec_() 


class newAcc (QDialog):
    def __init__(self):
        super(newAcc,self).__init__()
        loadUi('createacc.ui',self)
        self.setFixedWidth(980)
        self.setFixedHeight(620)
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        
        # initilize sql object for query#####################################################
        self.sqlQery = sql_mssql_class(db,driver,server,port,username,password,LoginDatabase) 
        print('logConnection string: ', self.sqlQery.cnctlog)
        self.logconn = db.connect(self.sqlQery.cnctlog)
        ###################################################################################
        
        #self.gologinBtn = self.findChild(QPushButton,'gologinBtn')
        #self.signupbtn = self.findChild(QPushButton,'signupbtn')
        #self.SuUNbx = self.findChild(QLineEdit, "SuUNbx")
        #self.SuPassbx = self.findChild(QLineEdit, "SuPassbx")
        #self.SuPassbxConf = self.findChild(QLineEdit, "SuPassbxConf")
        #self.SuFNbx = self.findChild(QLineEdit, "SuFNbx")
        #self.SuLNbx = self.findChild(QLineEdit, "SuLNbx")
        
        self.gologinBtn.clicked.connect(self.gotologin)
        self.signupbtn.clicked.connect(self.addNewUser)
        self.BackBtn.clicked.connect(self.gotomainWin)
    
    def addNewUser(self):
        Levels = {'High':2,'Medium':1,'Low':0} #level od Users.
        #checking for that fileds is not empyty and pass= passconf. 
        if (self.SuPassbx.text() == self.SuPassbxConf.text() and self.SuPassbx.text().strip()!='' and
            self.SuUNbx.text().strip()!='' and self.FNnameLE.text().strip()!='' and self.creatorLE.text().strip()!='' ):
            
            infosignup = self.sqlQery.add_signUp(self.logconn,self.SuUNbx.text(),self.SuPassbx.text(),
                                            self.FNnameLE.text(),self.creatorLE.text(),Levels[self.lvlcbBox.currentText()])
            print('sign up info : ',infosignup)
            if infosignup[0] :
                self.msg.setText( "User_added!")
                self.msg.exec_()
            else:
                self.msg.setText( "User_adding failed! use other username!")
                self.msg.exec_()
                
                
        else:
            print('passwords not the same or requirements are empty!')
            self.msg.setText( 'passwords not the same or requirements are empty!')
            self.msg.exec_() 
        
    def gotologin(self):
            self.logconn.close()
            loginW=Login()
            widget.addWidget(loginW)
            widget.setCurrentIndex(widget.currentIndex()+1)
            
    def gotomainWin(self):
            self.logconn.close()
            mainWinW=mainWin()
            widget.addWidget(mainWinW)
            widget.setCurrentIndex(widget.currentIndex()+1)


class mainWin(QMainWindow):
    def __init__(self):
        super(mainWin,self).__init__()
        loadUi('dataWin.ui',self)
        self.setFixedWidth(980)
        self.setFixedHeight(620)
        self.setWindowTitle("Phone Book")
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        # initilize sql object for query#####################################################
        #create an object of sql_mssql_class
        self.sqlQery = sql_mssql_class(db,driver,server,port,username,password,LoginDatabase) 
        # cnctStringMdb has been set in login section
        print('connect string in mainWin: ',cnctStringMdb)
        #create a connection by pyodbc, its need for sql_mssql_class methodes
        self.MDBconn = db.connect(cnctStringMdb)
        ###################################################################################

        
        #self.fnamebx = self.findChild(QLineEdit, "fnamebx")
        #self.lnamebx = self.findChild(QLineEdit, "lnamebx")
        #self.phbx = self.findChild(QLineEdit, "phbx")
        #self.tabWidget = self.findChild(QTabWidget, "tabWidget")
        #self.UsercomboBox = self.findChild(QComboBox,'UsercomboBox')
        #self.insertBtn = self.findChild(QPushButton,'insertBtn')
        
        # set phoneBooks of users to combobox
        for item in Users:
            self.PhnBookcomboBox.addItem(item[2])
        self.PhnBookcomboBox.setCurrentText(thisUser[2]) #set this user phoneBook to current text of combobox. 
        


        self.insertBtn.clicked.connect(self.gotoInsert)
        
        self.actionCreate_Account.triggered.connect( self.gotoSignUp)
        self.actionDel_user.triggered.connect( self.gotoDelUser)
        self.actionlog_In.triggered.connect( self.gotologin)
        
        self.fnamebx.textChanged.connect( lambda: self.loadData(0))
        self.lnamebx.textChanged.connect(lambda: self.loadData(0))
        
        self.tableWidget.doubleClicked.connect(self.getRowid)
        
        #self.tabWidget.tabBarClicked.connect(self.loadData)
        self.tabWidget.setTabText(0,thisUser[1]) # set name of user to tab name.
        self.tableWidget.setColumnWidth(7,300) # address
        
        self.PhnBookcomboBox.currentTextChanged.connect(lambda: self.loadData(0))

        self.loadData(0)

        
    def getRowid(self):
        """This function get row and first column of that row of tableWidget when double clicked that.  
        """        
        row = self.tableWidget.currentRow()
        current_column = self.tableWidget.currentColumn()
        global name_id #id of first column in tableWidget. this is same with id of name from names table.
        name_id = int(self.tableWidget.item(row,0).text())
        print('name_id extract by getRowid from mainWin: ',name_id)
        #print(self.sqlQery.searchby_name_id_phoneN(self.MDBconn,name_id))
        self.MDBconn.close()
        srchshow=searchshow()
        widget.addWidget(srchshow)
        widget.setCurrentIndex(widget.currentIndex()+1)

        
    def loadData(self,rc:int):
        """Load data from database by searching to tableWidget.

        Args:
            rc (int): Limitation of row.
        """        
        UserIDfromCombobx =[ item for item in Users if item[2] == self.PhnBookcomboBox.currentText() ][0][0]
        #print(UserIDfromCombobx)
        data = self.sqlQery.searchShow(self.MDBconn,self.fnamebx.text(),self.lnamebx.text(),UserIDfromCombobx)
        if rc==0:
            self.tableWidget.setRowCount(len(data))
        else:
            self.tableWidget.setRowCount(rc)
        tableRow = 0
        for row in data :
            self.tableWidget.setItem(tableRow, 0 , QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tableRow, 1 , QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tableRow, 2 , QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tableRow, 3 , QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(tableRow, 4 , QtWidgets.QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(tableRow, 5 , QtWidgets.QTableWidgetItem(row[6]))
            self.tableWidget.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(row[10]))
            self.tableWidget.setItem(tableRow, 7 , QtWidgets.QTableWidgetItem(row[14]))
            tableRow+=1
            
    def gotoInsert(self):
        """Go to Insert section from mainWindow.
        """        
        #print('go to insert')
        global WhichWin #this varibale has been use to 'Insert' section to setting and detect to insert new or existed contact.  
        WhichWin = 'mainWin'
        self.MDBconn.close()
        InsertWD=Insert()
        widget.addWidget(InsertWD)
        widget.setCurrentIndex(widget.currentIndex()+1)
            
    def gotologin(self):
            loginW=Login()
            widget.addWidget(loginW)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoSignUp(self):
        if UserLevel == accessLevel['High']:
            newAccW=newAcc()
            widget.addWidget(newAccW)
            widget.setCurrentIndex(widget.currentIndex()+1)
            print('Go to SignUp')
        else:
            print('Level:{} users cant access to SignUp! '.format(UserLevel))
            self.msg.setWindowTitle("User conflict!")
            self.msg.setText('Level:{} users cant access to SignUp! '.format(UserLevel))
            self.msg.exec_()
            
    def gotoDelUser(self):
        if UserLevel == accessLevel['High']:
            DeleteUserW=DeleteUser()
            widget.addWidget(DeleteUserW)
            widget.setCurrentIndex(widget.currentIndex()+1)
            print('Go to DeleteUser')
        else:
            print('Level:{} users cant access to DeleteUserW! '.format(UserLevel))
            self.msg.setWindowTitle("User conflict!")
            self.msg.setText('Level:{} users cant access to DeleteUserW! '.format(UserLevel))
            self.msg.exec_()

class searchshow(QDialog):
    def __init__(self):
        super(searchshow,self).__init__()
        loadUi("searchshow.ui",self)
        
        #set messageBox to getting question. 
        self.UDmsg = QMessageBox()
        self.UDmsg.setIcon(QMessageBox.Question)
        self.UDmsg.setText("Update or Delete?")
        self.UDmsg.setWindowTitle("Update or Delete!")
        self.UDmsg.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
        self.UDmsgUpdateBtb = self.UDmsg.button(QMessageBox.Yes)
        self.UDmsgDeleteBtb = self.UDmsg.button(QMessageBox.No)
        self.UDmsgUpdateBtb.setText('Update')
        self.UDmsgDeleteBtb.setText('Delete')
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        # initilize sql object and a connection for query#####################################################
        self.sqlQery = sql_mssql_class(db,driver,server,port,username,password,LoginDatabase) 
        self.MDBconn = db.connect(cnctStringMdb)
        ###################################################################################
        #self.gomwinBtn = self.findChild(QPushButton,'gomwinBtn')
        #self.InsertBtn = self.findChild(QPushButton,'InsertBtn')
        #self.deleteAllBtn = self.findChild(QPushButton,'deleteAllBtn')
        #self.lblNameFL = self.findChild(QLabel,'lblNameFL')
        #self.tableWPHn = self.findChild(QTabWidget, "tableWPHn")
        #self.tableWemail = self.findChild(QTabWidget, "tableWemail")
        #self.tableWaddr = self.findChild(QTabWidget, "tableWaddr")
        
        self.gomwinBtn.clicked.connect(self.gotomainwin)
        self.InsertBtn.clicked.connect(self.gotoInsert)
        self.deleteAllBtn.clicked.connect(self.deleteContact_all)
        
        #Action of three tables(PhoneN,email,Address)
        self.tableWPHn.doubleClicked.connect(self.UpdateOrDeletePh)
        self.tableWemail.doubleClicked.connect(self.UpdateOrDeleteEm)
        self.tableWaddr.doubleClicked.connect(self.UpdateOrDeleteAddr)
        self.tableWPHn.setColumnWidth(0,220)
        self.tableWemail.setColumnWidth(0,220)
        self.tableWaddr.setColumnWidth(0,220)
        
        self.currentdataPh = []
        self.currentdataEm = []
        self.currentdataAddr=[]
        

        self.let = True # without limitations. False -> dont let some intering like create user and delete user.
        self.loadData()
        self.SetUserlimitation()
        
    def SetUserlimitation(self):
        #limitation for this User if the name related to the name_id belong to another user and this user level is medium or low.
        # name_idData[0][4] is UsserID of name with the name_id. 
        # thisUser[0] is UserID of this user logedIn. 
        # Users[0][0] is UserID of Commoun user.
        name_idData =self.sqlQery.searchby_name_id_flname(self.MDBconn,name_id)
        if UserLevel!=accessLevel['High'] and name_idData[0][4]!= thisUser[0] and name_idData[0][4]!=Users[0][0]: # user dont become level 2 and user contact become another execept Common user.
            self.let =False
        
    def loadData(self):
        """Load data (name,phone numbers, emails and addresses from  database related th name_id)
        """        
        data = self.sqlQery.searchby_name_id_flname(self.MDBconn,name_id)
        self.currentdataPh = self.sqlQery.searchby_name_id_phoneN(self.MDBconn,name_id)
        self.currentdataEm = self.sqlQery.searchby_name_id_email(self.MDBconn,name_id)
        self.currentdataAddr=self.sqlQery.searchby_name_id_Addr(self.MDBconn,name_id)
        print('data of this name_id : {}'.format(name_id) )
        print(self.currentdataPh)
        print(self.currentdataEm)
        print(self.currentdataAddr)
        # data[0][1] is first name.
        # data[0][2] is last name.
        self.lblNameFL.setText(data[0][1]+' '+ data[0][2])
        
        self.tableWPHn.setRowCount(len(self.currentdataPh))
        tableRow = 0
        for row in self.currentdataPh :
            self.tableWPHn.setItem(tableRow, 0 , QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow+=1

        self.tableWemail.setRowCount(len(self.currentdataEm))
        tableRow = 0
        for row in self.currentdataEm :
            self.tableWemail.setItem(tableRow, 0 , QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow+=1

        self.tableWaddr.setRowCount(len(self.currentdataAddr))
        tableRow = 0
        for row in self.currentdataAddr :
            self.tableWaddr.setItem(tableRow, 0 , QtWidgets.QTableWidgetItem(str(row[1])))
            tableRow+=1

    def getRowid(self,TableW:object,currentContactData):
        """get first column of a table base of selection in a tableWisget(phoneN,email or address tableWidget).

        Args:
            TableW (object): A tableWidget object.
            currentContactData (list od tuple): phone numbers or email or address related name_id.
                it must returned from Phonebook database like this methode -> searchby_name_id_.

        Returns:
            return True , int(tableIDRow) , P_E_A -> tableIDRow is ID of selection(row in tableWidget) base on
                its table from phoneBook database.
                P_E_A is Phone number or Email or Address.
            return False , 0 ,''
        """        
        current_row = TableW.currentRow()
        #current_column = TableW.currentColumn()
        P_E_A = TableW.item(current_row,0).text()
        if P_E_A != '':
            tableIDRow = [item for item in currentContactData if item[1]==P_E_A][0][0]
            print('PhoneN or email or Address of row selected: ',P_E_A)
            print('ID of the table related the row: ', tableIDRow)
            print('Data of current contact: ',currentContactData)
            return True , int(tableIDRow) , P_E_A
        else:
            return False , 0 ,''


    def deleteContact_all(self):
        """Delete a contact with all phone numbers , emails and addresses.
        """        
        if self.let: # this user let or not base on its level. 
            ret = QMessageBox.warning(self, 'Delete?', "Are you sure to delete this contact?", QMessageBox.Yes | QMessageBox.No )
            if ret == QMessageBox.Yes:
                delmessage = self.sqlQery.delete_row(self.MDBconn,name_id)
                if delmessage[0]:
                    print('Delete message: ', delmessage[1])
                    self.msg.setText("Contact deleted!")
                    self.msg.setWindowTitle("Delete!")
                    self.msg.exec_()
                    self.gotomainwin()
                else:
                    self.msg.setWindowTitle("Delete!")
                    self.msg.setText("Exist problem in contact deleting process!")
                    print("Exist problem in contact deleting process!")
                    print('Delete problem message: ',delmessage[1])
                    self.msg.exec_()
        else:
            self.msg.setText(" You dont let insert, delete or update to onother users execept yourself or Common contacts!")
            self.msg.setWindowTitle("User conflict!")
            self.msg.exec_()

    def UpdateOrDeletePh(self):
        """Update or Delete by selection of a row in phoneN tableW. 
        """        
        if self.let:
            self.UDmsg.exec_()
            if self.UDmsg.clickedButton() == self.UDmsgUpdateBtb:
                Rowresult = self.getRowid(self.tableWPHn,self.currentdataPh)
                if Rowresult[0]: #True
                    phoneN_ID = Rowresult[1]
                    print(' go to updating  for this id {}'.format(phoneN_ID))
                    NewPhoneN, ok = QInputDialog.getText(self, 'Update', 'Inser new Phone Number')
                    if ok:
                        state = self.sqlQery.update_phoneN_byID(self.MDBconn,phoneN_ID,NewPhoneN)
                        if state[0]:#True
                            print(' phoneN Updated for this id {}'.format(phoneN_ID))
                            print(' phoneN Updating state: ', state)
                            self.loadData()
                            self.msg.setWindowTitle("Update!")
                            self.msg.setText("{}".format(state[1]))
                            self.msg.exec_()
                        else: # flase -> not updating
                            print(' phoneN Updating state: ', state)
                            self.msg.setWindowTitle("Update!")
                            self.msg.setText("{}".format(state[1]))
                            self.msg.exec_()  
                    
                    
            elif self.UDmsg.clickedButton() == self.UDmsgDeleteBtb:
                Rowresult = self.getRowid(self.tableWPHn,self.currentdataPh)
                if Rowresult[0]: #True
                    phoneN_ID = Rowresult[1]
                    state = self.sqlQery.delete_phoneN_byID(self.MDBconn,phoneN_ID)
                    if state[0]:#True
                        print(' phoneN deleted by this id {}'.format(phoneN_ID))
                        print(' phoneN deleting state: ', state)
                        self.loadData()
                        self.msg.setWindowTitle("Delete!")
                        self.msg.setText("{}".format(state[1]))
                        self.msg.exec_()
                    else: # flase -> not deleting
                        print(' phoneN deleting state: ', state)
                        self.msg.setWindowTitle("Delete!")
                        self.msg.setText("{}".format(state[1]))
                        self.msg.exec_()                   
        else:
            self.msg.setText(" You dont let insert, delete or update to onother users execept yourself or Common contacts!")
            self.msg.setWindowTitle("User conflict!")
            self.msg.exec_()

    def UpdateOrDeleteEm(self):
        """Update or Delete by selection of a row in email tableW. 
        """  
        if self.let:
            self.UDmsg.exec_()
            if self.UDmsg.clickedButton() == self.UDmsgUpdateBtb:
                Rowresult = self.getRowid(self.tableWemail,self.currentdataEm)
                if Rowresult[0]: #True
                    email_ID = Rowresult[1]
                    print(' go to updating  for this id {}'.format(email_ID))
                    NewEmail, ok = QInputDialog.getText(self, 'Update', 'Inser new Email')
                    if ok:
                        state = self.sqlQery.update_email_byID(self.MDBconn,email_ID,NewEmail)
                        if state[0]:#True
                            print(' Email Updated for this id {}'.format(email_ID))
                            print(' Email Updating state: ', state)
                            self.loadData()
                            self.msg.setWindowTitle("Update!")
                            self.msg.setText("{}".format(state[1]))
                            self.msg.exec_()
                        else: # flase -> not updating
                            print(' Email Updating state: ', state)
                            self.msg.setWindowTitle("Update!")
                            self.msg.setText("{}".format(state[1]))
                            self.msg.exec_() 
                    
            elif self.UDmsg.clickedButton() == self.UDmsgDeleteBtb:
                Rowresult = self.getRowid(self.tableWemail,self.currentdataEm)
                if Rowresult[0]: #True
                    email_ID = Rowresult[1]
                    state = self.sqlQery.delete_email_byID(self.MDBconn,email_ID)
                    if state[0]:#True
                        print(' Email deleted by this id {}'.format(email_ID))
                        print(' Email deleting state: ', state)
                        self.loadData()
                        self.msg.setWindowTitle("Delete!")
                        self.msg.setText("{}".format(state[1]))
                        self.msg.exec_()
                    else: # flase -> not deleting
                        print(' Email deleting state: ', state)
                        self.msg.setWindowTitle("Delete!")
                        self.msg.setText("{}".format(state[1]))
                        self.msg.exec_()  
        else:
            self.msg.setText(" You dont let insert, delete or update to onother users execept yourself or Common contacts!")
            self.msg.setWindowTitle("User conflict!")
            self.msg.exec_()

    def UpdateOrDeleteAddr(self):
        """Update or Delete by selection of a row in address tableW. 
        """  
        if self.let:
            self.UDmsg.exec_()
            if self.UDmsg.clickedButton() == self.UDmsgUpdateBtb:
                Rowresult = self.getRowid(self.tableWaddr,self.currentdataAddr)
                if Rowresult[0]: #True
                    addr_ID = Rowresult[1]
                    print(' go to updating  for this id {}'.format(addr_ID))
                    NewAddress, ok = QInputDialog.getText(self, 'Update', 'Inser new Phone Number')
                    if ok:
                        state = self.sqlQery.update_Address_byID(self.MDBconn,addr_ID,NewAddress)
                        if state[0]:#True
                            print(' Address Updated for this id {}'.format(addr_ID))
                            print(' Address Updating state: ', state)
                            self.loadData()
                            self.msg.setWindowTitle("Update!")
                            self.msg.setText("{}".format(state[1]))
                            self.msg.exec_()
                        else: # flase -> not updating
                            print(' Address Updating state: ', state)
                            self.msg.setWindowTitle("Update!")
                            self.msg.setText("{}".format(state[1]))
                            self.msg.exec_()  
                            
            elif self.UDmsg.clickedButton() == self.UDmsgDeleteBtb:
                Rowresult = self.getRowid(self.tableWaddr,self.currentdataAddr)
                if Rowresult[0]: #True
                    addr_ID = Rowresult[1]
                    state = self.sqlQery.delete_address_byID(self.MDBconn,addr_ID)
                    if state[0]:#True
                        print(' Address deleted by this id {}'.format(addr_ID))
                        print(' Address deleting state: ', state)
                        self.loadData()
                        self.msg.setWindowTitle("Delete!")
                        self.msg.setText("{}".format(state[1]))
                        self.msg.exec_()
                    else: # flase -> not deleting
                        print(' Address deleting state: ', state)
                        self.msg.setWindowTitle("Delete!")
                        self.msg.setText("{}".format(state[1]))
                        self.msg.exec_()  
        else:
            self.msg.setText(" You dont let insert, delete or update to onother users execept yourself or Common contacts!")
            self.msg.setWindowTitle("User conflict!")
            self.msg.exec_()
        
        
    def gotoInsert(self):
        if self.let:
            print('go to insert')
            global WhichWin
            WhichWin = 'searchshow'  # Insert section detect this is insert for exsited account. 
            self.MDBconn.close()
            InsertWD=Insert()
            widget.addWidget(InsertWD)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.msg.setText(" You dont let insert, delete or update to onother users execept yourself or Common contacts!")
            self.msg.setWindowTitle("User conflict!")
            self.msg.exec_()
        
    def gotomainwin(self):
            self.MDBconn.close()
            mainW=mainWin()
            widget.addWidget(mainW)
            widget.setCurrentIndex(widget.currentIndex()+1)

class Insert(QDialog):
    def __init__(self):
        super(Insert,self).__init__()
        loadUi("InsertDialog.ui",self)
        
        self.UDmsg = QMessageBox()
        self.UDmsg.setIcon(QMessageBox.Question)
        self.UDmsg.setText("Update or Delete?")
        self.UDmsg.setWindowTitle("Update or Delete!")
        self.UDmsg.setStandardButtons(QMessageBox.No|QMessageBox.Cancel)
        self.UDmsgDeleteBtb = self.UDmsg.button(QMessageBox.No)
        self.UDmsgDeleteBtb.setText('Delete')
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        
        # initilize sql object and database connection for query#####################################################
        self.sqlQery = sql_mssql_class(db,driver,server,port,username,password,LoginDatabase) 
        self.MDBconn = db.connect(cnctStringMdb)
        ###################################################################################        
        self.PhAddBtn.clicked.connect(self.addPhone)
        self.EmAddBtn.clicked.connect(self.addEmail)
        self.AddrAddBtn.clicked.connect(self.addAddress)
        self.BackBtn.clicked.connect(self.goto)
        self.InsertBtn.clicked.connect(self.insert)
        self.PhntableW.doubleClicked.connect(self.PhnRemoveTable)
        self.EmtableW.doubleClicked.connect(self.EmRemoveTable)
        self.AddrtableW.doubleClicked.connect(self.AddrRemoveTable)
        
        self.setting()
    
    def PhnRemoveTable(self):
        """this function can remove an item from Phone table by selecting on specific its row and column.
        """        
        row = self.PhntableW.currentRow()
        current_column = self.PhntableW.currentColumn()
        self.UDmsg.setText(self.PhntableW.item(row,current_column).text())
        self.UDmsg.exec_()
        if self.UDmsg.clickedButton() == self.UDmsgDeleteBtb:
            self.PhntableW.removeRow(row)
            print('DELETED row', row)
            
    def EmRemoveTable(self):
        """this function can remove an item from email table by selecting on specific its row and column.
        """        
        row = self.EmtableW.currentRow()
        current_column = self.EmtableW.currentColumn()
        self.UDmsg.setText(self.EmtableW.item(row,current_column).text())
        self.UDmsg.exec_()
        if self.UDmsg.clickedButton() == self.UDmsgDeleteBtb:
            self.EmtableW.removeRow(row)
            print('DELETED row', row)
            
    def AddrRemoveTable(self):
        """this function can remove an item from address table by selecting on specific its row and column.
        """        
        row = self.AddrtableW.currentRow()
        current_column = self.AddrtableW.currentColumn()
        self.UDmsg.setText(self.AddrtableW.item(row,current_column).text())
        self.UDmsg.exec_()
        if self.UDmsg.clickedButton() == self.UDmsgDeleteBtb:
            self.AddrtableW.removeRow(row)
            print('DELETED row', row)
            
    def loadDataAndAdd(self,tableW:object ,PEA_typ,tableNumRows=0):
        """Load and add a data to a tableWidget with phoneN or email or address with its type(it is a list).

        Args:
            tableW (object): tabaleWidget.
            PEA_typ (list): [P or E or A , its type]
            tableNumRows (int):it detemine which row of table. Defaults to 0.
        """        
        print('tableNumRows: ',tableNumRows)
        print('PEA_typ: ',PEA_typ)
        tableW.setRowCount(tableNumRows+1)
        if tableNumRows == 0:
            tableRow=0
        else:
            tableRow=tableNumRows
        
        tableW.setItem(tableRow, 0 , QtWidgets.QTableWidgetItem(PEA_typ[0])) # P or E or A
        tableW.setItem(tableRow, 1 , QtWidgets.QTableWidgetItem(PEA_typ[1])) # types
            
            
    def setItemsCombobox(self):
        """Set related data(User,group and type)  to comboboxes.
        """        
        groups = self.sqlQery.readGroups(self.MDBconn)
        types = self.sqlQery.readTypes(self.MDBconn)
        print('types: ',types)
        print('groups', groups)
        print('Users: ', Users)
        if len(types)>1 and len(groups)>1: #not error accured. beacuse legth of types and groups table always greater than 1.
            for item in groups:
                self.GrpcomboBox.addItem(item[1])
            for item in types:
                self.PhnTypcomboBox.addItem(item[1])
                self.EmTypcomboBox.addItem(item[1])
                self.AddrTypcomboBox.addItem(item[1])
                
            #limitations for Users
            if UserLevel==accessLevel['High']: # this is global variable
                for item in Users:
                    self.UsercomboBox.addItem(item[1])
            elif UserLevel==accessLevel['Medium']: 
                self.UsercomboBox.addItem(thisUser[1])
                self.UsercomboBox.addItem(Users[0][1]) #Common
            elif UserLevel==accessLevel['Low']: 
                self.UsercomboBox.addItem(thisUser[1])
                self.UsercomboBox.addItem(Users[0][1]) #Common
        else:
            print('Problem in retrieving groups and types data!')
    
    def setting(self):
        #setting some text and labels respect to which window come here.
        self.setItemsCombobox()
        self.Userlbl.setText(thisUser[1]) #username of this User(login username)
        global WhichWin
        if WhichWin == 'mainWin':
            # name_id is a global variable. we set it to zero that will use in iserting new contact.
            # if name_id!=0 insert to existed contact with this name_id. name_id setted in searchshow section.
            global name_id
            name_id = 0 
            self.statelbl.setText('Inserting new contact')
        elif WhichWin == 'searchshow':
            dataname = self.sqlQery.searchby_name_id_flname(self.MDBconn,name_id)
            groups = self.sqlQery.readGroups(self.MDBconn)
            print("name:  ",dataname)
            #extract group name and username of its name related name_id and set it to related combobox.
            GrpnameForname = [item for item in groups if item[0]==dataname[0][3]][0][1]
            usernameForname = [item for item in Users if item[0]==dataname[0][4]][0][1]
            print('GrpnameForname:  ',GrpnameForname)
            self.GrpcomboBox.setCurrentText(GrpnameForname)
            self.UsercomboBox.setCurrentText(usernameForname)
            self.statelbl.setText('Inserting existed contact')
            self.fnameLE.setText(dataname[0][1])
            self.lnameLE.setText(dataname[0][2])
            self.fnameLE.setReadOnly(True)
            self.lnameLE.setReadOnly(True)

    def addPhone(self):
        """Add phone number and its type to phone number table.
        """        
        if self.PhnLE.text().strip()!='':
            self.loadDataAndAdd(self.PhntableW,[self.PhnLE.text(),self.PhnTypcomboBox.currentText()],self.PhntableW.rowCount())
            
    def addEmail(self):
        """Add email and its type to email table.
        """        
        if self.EmLE.text().strip()!='':
            self.loadDataAndAdd(self.EmtableW,[self.EmLE.text(),self.EmTypcomboBox.currentText()],self.EmtableW.rowCount())

    def addAddress(self):
        """Add address and its type to address table.
        """        
        if self.AddrTxtE.toPlainText().strip()!='':
            self.loadDataAndAdd(self.AddrtableW,[self.AddrTxtE.toPlainText(),self.AddrTypcomboBox.currentText()],self.AddrtableW.rowCount()) 
            
    def goto(self):
        """Go to mainwindow or searchShow window base of which come to Insert.
        """        
        self.MDBconn.close()
        global WhichWin
        if WhichWin == 'mainWin':
            mainW=mainWin()
            widget.addWidget(mainW)
            widget.setCurrentIndex(widget.currentIndex()+1)
        elif WhichWin == 'searchshow':
            searchshowW=searchshow()
            widget.addWidget(searchshowW)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def insert(self):
        """Insert process. this function insert all items(name,phoneNUmbers,emails and addresses)
        """        
        print('Iserted')
        #ID of a user from usercombobox that use it in inserting name.
        userIDcombobox = [item for item in Users if item[1]==self.UsercomboBox.currentText()][0][0]
        print(userIDcombobox)
        
        groups = self.sqlQery.readGroups(self.MDBconn)
        types = self.sqlQery.readTypes(self.MDBconn)
        groupCombobox = [item for item in groups if item[1]==self.GrpcomboBox.currentText()][0][0]
        print('groupCombobox: ',groupCombobox)
        
        
        
        if self.fnameLE.text().strip()!='' :
            
            #insert new first name and last name if name_id=0(come from mainWindow) otherwise nothing
            # just return some data related name_id.
            nameData = self.sqlQery.insert_row(self.MDBconn, name_id,userIDcombobox,
                                                self.fnameLE.text(),self.lnameLE.text(),groupCombobox)
            print('nameData: ', nameData)
            
            if nameData[0] and (nameData[1][0].strip() == 'N' or nameData[1][0].strip() == 'N_EXIST'):# name inserted or name existed
                IDForName =int(nameData[1][1] )
                print('userForName: ',IDForName)
                
                #Inserting phone numbers from phone number tableWidget.
                for i in range(self.PhntableW.rowCount()):
                    PhntypeIDcombobox = [item for item in types if item[1]==self.PhntableW.item(i, 1).text()][0][0]
                    insertData = self.sqlQery.insert_row(self.MDBconn, name_ID = IDForName ,
                                                            phoneN=self.PhntableW.item(i, 0).text() ,
                                                            Pntyp_id=PhntypeIDcombobox)
                #Inserting emails from email tableWidget.
                for i in range(self.EmtableW.rowCount()):
                    EmtypeIDcombobox = [item for item in types if item[1]==self.EmtableW.item(i, 1).text()][0][0]
                    insertData = self.sqlQery.insert_row(self.MDBconn, name_ID = IDForName ,
                                                            email=self.EmtableW.item(i, 0).text() ,
                                                            Emtyp_id=EmtypeIDcombobox)
                #Inserting addresses from address tableWidget.
                for i in range(self.AddrtableW.rowCount()):
                    AddrtypeIDcombobox = [item for item in types if item[1]==self.AddrtableW.item(i, 1).text()][0][0]
                    insertData = self.sqlQery.insert_row(self.MDBconn, name_ID = IDForName ,
                                                            addr=self.AddrtableW.item(i, 0).text() ,
                                                            Addrtyp_id=AddrtypeIDcombobox)
                    
                self.msg.setWindowTitle("Inserting!")
                self.msg.setText("{}".format(insertData))
                self.msg.exec_()
        else:
            print('First name box in empty!_insertSection')
            self.msg.setText('First name box in empty!')
            self.msg.exec_()

class DeleteUser(QDialog):
    def __init__(self):
        super(DeleteUser,self).__init__()
        loadUi("DeleteUser.ui",self)
        self.DTmsg = QMessageBox()
        self.DTmsg.setIcon(QMessageBox.Question)
        self.DTmsg.setText("Are you sure?")
        self.DTmsg.setWindowTitle("Delete and Transfer data")
        self.DTmsg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        # initilize sql object and connection object for query#####################################################
        self.logsqlQery = sql_mssql_class(db,driver,server,port,username,password,LoginDatabase) 
        print('logConnection string: ', self.logsqlQery.cnctlog)
        self.logconn = db.connect(self.logsqlQery.cnctlog)
        self.sqlQery = sql_mssql_class(db,driver,server,port,username,password,LoginDatabase) 
        self.MDBconn = db.connect(cnctStringMdb)
        ###################################################################################

        self.logInbtn.clicked.connect(self.gotologin)
        self.RTbtn.clicked.connect(self.DelandTrans)
        self.setItemsCombobox()

    def gotologin(self):
            self.logconn.close()
            loginW=Login()
            widget.addWidget(loginW)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def setItemsCombobox(self):
        for item in Users:
            if item[1]!='Common': # Common user not removable then do not add to RmvcmbBox.
                self.RmvcmbBox.addItem(item[1])
                
            self.SubtcmbBox.addItem(item[1])

    
    def DelandTrans(self):
        """transfer data to another user and remove intended user.
        """        
        print("Deleting and transfering!")
        self.DTmsg.setText("Are you sure to Delete ({}) and transfer data to ({})?".format(self.RmvcmbBox.currentText(),self.SubtcmbBox.currentText()))
        result= self.DTmsg.exec_()
        if result == QMessageBox.Yes:
            #extract id of related users.
            DelUserID = [item for item in Users if item[1] ==self.RmvcmbBox.currentText() ][0][0]
            substitute_UserID = [item for item in Users if item[1] ==self.SubtcmbBox.currentText() ][0][0]
            print('DelUserID: ',DelUserID)
            print('substitute_UserID: ',substitute_UserID)
            state = self.sqlQery.deleteUser(DelUserID,substitute_UserID,self.logconn,self.MDBconn)

            self.msg.setWindowTitle("Delete and Transfer data!!")
            self.msg.setText("Deleting and data transfering!_{}".format(state))
            self.msg.exec_()



if __name__ == '__main__':
    app=QApplication(sys.argv)
    mainwindow=Login()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(980)
    widget.setFixedHeight(620)
    widget.show()
    app.exec_()
    
