#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import csv
import IPython.display as ipd
import sys
import regex as re


import pandas as pd
import numpy as np

import os
import math


import seaborn as sns

from matplotlib import pyplot as plt
plt.style.use('seaborn')


# In[ ]:





# In[2]:


con = sqlite3.connect('LCS1.db')
cur = con.cursor()


# In[3]:


cur.execute("""CREATE TABLE IF NOT EXISTS Vehicle(
            VehicleID INTEGER PRIMARY KEY NOT NULL,
            [Transport Mode] TEXT,
            [Vehicle Type] TEXT,
            Make TEXT,
            Model TEXT,
            YearsServiced INTEGER,
            [Kms Traveled] REAL
            );""")



cur.execute("""CREATE TABLE IF NOT EXISTS Person(
                PersonID INTEGER PRIMARY KEY NOT NULL,
                Fname TEXT,
                Lname TEXT,
                [Street Address] TEXT,
                City TEXT,
                Province TEXT,
                [Postal Code] TEXT,
                Age INTEGER
                );""")



cur.execute("""CREATE TABLE IF NOT EXISTS Location(
            LocationID INTEGER PRIMARY KEY NOT NULL,
            Street TEXT,
            City TEXT,
            Province TEXT,
            [Postal Code] TEXT
            );""")



cur.execute("""CREATE TABLE IF NOT EXISTS Employee(
            EmployeeID INTEGER PRIMARY KEY NOT NULL,
            ManagerID INTEGER,
            EmployeeLogin TEXT,
            EmployeePWD TEXT,
            [Employee Role] TEXT,
            [Employee Dept] TEXT,
            [CanDeliver] TEXT,
            CONSTRAINT fk_eperson FOREIGN KEY (EmployeeID) REFERENCES Person(PersonID),
            CONSTRAINT fk_memployee FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
            );""")




cur.execute("""CREATE TABLE IF NOT EXISTS Customer(
            CustomerID INTEGER PRIMARY KEY NOT NULL,
            CustomerLogin TEXT,
            CustomerPWD TEXT,
            [Customer Balance] REAL,
            CONSTRAINT fk_cperson FOREIGN KEY (CustomerID) REFERENCES Person(PersonID)
            );""")



cur.execute("""CREATE TABLE IF NOT EXISTS Warehouse(
            WarehouseID INTEGER PRIMARY KEY NOT NULL,
            WareLocID INTEGER,
            [Storage Capacity] INT,
            [Remaining Capacity] INT,
            CONSTRAINT fk_wLocation FOREIGN KEY (WareLocID) REFERENCES Location(LocationID)
            );""")




cur.execute("""CREATE TABLE IF NOT EXISTS Product(
            ProductID INTEGER PRIMARY KEY NOT NULL,
            ProductName TEXT,
            ProductType TEXT,
            Cost REAL,
            StockInHand INTEGER,
            WarehouseID INTEGER,
            CONSTRAINT fk_pWarehouse FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID)
            );""")


cur.execute("""CREATE TABLE IF NOT EXISTS Route(
            RouteID INTEGER PRIMARY KEY NOT NULL,
            PackID INTEGER NOT NULL,
            DelivFromID INTEGER,
            DelivToID INTEGER,
            DelivEmpID INTEGER,
            DelivVehcID INTEGER,
            Status TEXT,
            [Last Updated] DATE,
            Active TEXT,
            CONSTRAINT fk_rWare FOREIGN KEY (DelivFromID) REFERENCES Warehouse(WarehouseID),
            CONSTRAINT fk_rLoc FOREIGN KEY (DelivToID) REFERENCES Location(LocationID),
            CONSTRAINT fk_rEmp FOREIGN KEY (DelivEmpID) REFERENCES Employee(EmployeeID),
            CONSTRAINT fk_rVehc FOREIGN KEY (DelivVehcID) REFERENCES Vehicle(VehicleID)
            );""")


cur.execute("""CREATE TABLE IF NOT EXISTS Pack(
            PackID INTEGER PRIMARY KEY NOT NULL,
            PackCustomerID INTEGER,
            [Total Cost] REAL,
            OrderDate DATE,
            DelivToStreet TEXT,
            DelivToCity TEXT,
            DelivToProvince TEXT,
            DelivToZip TEXT,
            Status TEXT,
            CONSTRAINT fk_pCust FOREIGN KEY (PackCustomerID) REFERENCES Customer(CustomerID)
            );""")


cur.execute("""CREATE TABLE IF NOT EXISTS Packline(
            PackID INTEGER NOT NULL,
            PacklineID INTEGER NOT NULL,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER,
            Cost INTEGER,
            PRIMARY KEY (PackID, PacklineID),
            CONSTRAINT fk_plPack FOREIGN KEY (PackID) REFERENCES Pack(PackID),
            CONSTRAINT fk_plProd FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            );""")



con.commit()


# In[ ]:





# In[4]:


# cur.execute("""INSERT INTO Person VALUES (1, 'Mark', 'Twain', 'Street-1', 'Kitchener', 'ON', 'N2K2K1', 20),
#                                          (2, 'John', 'Green', 'Street-2', 'Kitchener', 'ON', 'N334O7', 32),
#                                          (3, 'Ben', 'Wallace', 'Street-3', 'Waterloo', 'ON', 'M225A1', 32),
#                                          (4, 'Trae', 'Young', 'Street-4', 'Hamilton', 'ON', 'M225A7', 27),
#                                          (5, 'Joe', 'Rogan', 'Street-5', 'Waterloo', 'ON', 'N2K5B2', 29),
#                                          (6, 'Fred', 'Albert', 'Street-6', 'Toronto', 'ON', 'A3C6C2', 35),
#                                          (7, 'Tom', 'Cruise', 'Street-7', 'Cambridge', 'ON', 'N7A5B7', 45),
#                                          (8, 'Adam', 'Legend', 'Street-8', 'Kitchener', 'ON', 'B6C3D7', 22);
#                                          """)
# con.commit()




# cur.execute("""INSERT INTO Employee VALUES (3, 8, 'FLYERHIGH', 'NVLD74', 'Driver', 'Dept-1', 'Yes'),
#                                            (4, 8, 'CODERED', 'XLWVI206', 'Driver', 'Dept-1', 'No'),
#                                            (5, 8, 'OFFENSEBALL', 'WVUVMW65', 'Driver', 'Dept-2', 'Yes'),
#                                            (6, 8, 'RAPIDASHER', 'KLMBGZ52', 'Admin', 'Dept-2', 'No'),
#                                            (8, 0, 'FINALITY', 'KBGSLM99', 'CEO', 'Dept-0', 'No');
#                                            """)
# con.commit()



# cur.execute("""INSERT INTO Customer VALUES (1, 'MECHAMAN', 'KIZWZ09', 8000),
#                                            (2, 'ROBOTBOY', 'YZIP987', 1000),
#                                            (7, 'MAGIC91', 'NZTRX20', '4000');
#                                            """)
# con.commit()



# cur.execute("""INSERT INTO Location VALUES (1, 'Street-1', 'Kitchener', 'ON', 'N2K2K1'),
#                                            (2, 'Street-2', 'Kitchener', 'ON', 'N334O7'),
#                                            (3, 'Street-3', 'Waterloo', 'ON', 'M225A1'),
#                                            (4, 'Street-4', 'Hamilton', 'ON', 'M225A7'),
#                                            (5, 'Street-5', 'Waterloo', 'ON', 'N2K5B2'),
#                                            (6, 'Street-6', 'Toronto', 'ON', 'A3C6C2'),
#                                            (7, 'Street-7', 'Cambridge', 'ON', 'N7A5B7'),
#                                            (8, 'Street-8', 'Kitchener', 'ON', 'B6C3D7'),
#                                            (9, 'Street-9', 'Waterloo', 'ON', 'A7B4Q9'),
#                                            (10, 'Street-10', 'Kitchener', 'ON', 'C8D5B1'),
#                                            (11, 'Street-11', 'Toronto', 'ON', 'D9C3A5'),
#                                            (12, 'Street-12', 'Hamilton', 'ON', 'E2K7C9'),
#                                            (13, 'Street-13', 'Cambridge', 'ON', 'B4E8Q7');
#                                            """)
# con.commit()



# cur.execute("""INSERT INTO Warehouse VALUES (1, 9, 10, 2),
#                                             (2, 10, 25, 5),
#                                             (3, 11, 25, 2),
#                                             (4, 12, 31, 20),
#                                             (5, 13, 20, 10);
#                                             """)
# con.commit()



# cur.execute("""INSERT INTO Vehicle VALUES (1000, 'Road', '2-Wheeler', 'Make-1', 'Model-1', 5, 20000),
#                                           (1001, 'Water', 'Boat', 'Make-2', 'Model-2', 7, 160000),
#                                           (1002, 'Road', '4-Wheeler', 'Make-3', 'Model-3', 8, 1000),
#                                           (1003, 'Road', '4-Wheeler', 'Make-3', 'Model-4', 9, 8000),
#                                           (1004, 'Road', '8-Wheeler', 'Make-4', 'Model-5', 11, 20000);
#                                           """)

# con.commit()



# cur.execute("""INSERT INTO Product VALUES (1, 'Bottle', 'NP', 20, 2000, 3),
#                                           (2, 'Box', 'NP', 45, 1000, 3),
#                                           (3, 'Apple Tray', 'P', 7, 600, 1),
#                                           (4, 'Egg carton', 'P', 8, 800, 2),
#                                           (5, 'Steel Pipe', 'NP', 20, 1250, 5),
#                                           (6, 'Chair', 'NP', 45, 900, 4),
#                                           (7, 'Action Figure', 'NP', 10, 1500, 4);
#                                           """)

# con.commit()



# cur.execute("""INSERT INTO Pack VALUES (1, 1, 255, '2021-08-10', 'Street-1', 'Kitchener', 'ON', 'N2K2K1', 'Delivered'),
#                                        (2, 7, 230, '2021-08-14', 'Street-7', 'Cambridge', 'ON', 'N7A5B7', 'Delivered'),
#                                        (3, 2, 64, '2021-08-16', 'Street-14', 'Mississauga', 'ON', 'A3B9K5', 'Shipped'),
#                                        (4, 2, 140, '2021-08-17', 'Street-2', 'Kitchener', 'ON', 'N334O7', 'Paid');
#                                        """)
# con.commit()



# cur.execute("""INSERT INTO Packline VALUES (4, 1, 6, 1, 45),
#                                            (4, 2, 1, 1, 20),
#                                            (4, 3, 2, 1, 45),
#                                            (3, 1, 3, 4, 28),
#                                            (3, 2, 4, 2, 16),
#                                            (2, 1, 5, 10, 200),
#                                            (1, 1, 2, 5, 225);
#                                            """)
# con.commit()





# cur.execute("""INSERT INTO Route VALUES (1, 1, 3, 1, 4, 1003, 'Delivered', '2021-08-13', 'No'),
#                                         (2, 2, 5, 7, 3, 1002, 'Delivered', '2021-08-15', 'No'),
#                                         (3, 3, 1, 15, 4, 1000, 'Shipped', '2021-08-16', 'Yes');
#                                         """)
# con.commit()



# cur.close()
# con.close()


# In[ ]:





# In[ ]:





# In[ ]:





# In[5]:


decoder = [chr(num) for num in list(range(ord('A'), ord('Z')+1))] + [str(gh) for gh in list(range(0,10))]


# In[6]:


encoder = ['Z', 'Y', 'X', 'W', 'V','U','T','S','R','Q','P','O','N','M','L','K','J','I','H','G','F','E','D','C','B','A'] + ['1','0','9','8','7','6','5','4','3','2']


# In[7]:


def decoding(string):
    decoded = ''
    for i in string:
        decoded = decoded + decoder[encoder.index(i)]
    return decoded


# In[8]:


def encoding(string):
    encoded = ''
    for i in string:
        encoded = encoded + encoder[decoder.index(i)]
    return encoded


# In[9]:


def spl_check(string):
    
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    assert regex.search(string) == None


# In[ ]:





# In[ ]:





# In[10]:


def customers():
    con = sqlite3.connect('LCS1.db')
    cur = con.cursor()
    
    cur.execute('SELECT CustomerLogin FROM Customer;')
    customers = [obj[0] for obj in cur.fetchall()]
    
    cur.close()
    con.close()
    
    return customers


# In[11]:


def employees():
    con = sqlite3.connect('LCS1.db')
    cur = con.cursor()
    
    cur.execute('SELECT EmployeeLogin FROM Employee;')
    employees = [obj[0] for obj in cur.fetchall()]
    
    cur.close()
    con.close()
    
    return employees


# In[12]:


def check_valid_pack(customer_id):
    con = sqlite3.connect('LCS1.db')
    cur = con.cursor()
    
    cur.execute('SELECT PackID FROM Pack WHERE PackCustomerID = ?;', (customer_id,))
    packs = [onj[0] for onj in cur.fetchall()]
    
    cur.close()
    con.close()
    
    return packs


# In[ ]:





# In[ ]:





# In[13]:


def create_pwd():
    print("\nPLEASE CREATE A NEW PASSWORD\n\nThe password can be of any length, but must not contain special characters\n\n***PASSWORDS ARE CASE INSENSITIVE***\n\nYou can enter 'take me back' to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        try:
            new_password = str(input())
            if new_password.lower() == 'take me back':
                ipd.clear_output()
                break
            spl_check(new_password)
        except:
            print('\n***INVALID PASSWORD***\n\nThe password can be of any length, but MUST NOT CONTAIN SPECIAL CHARACTERS\n\n')
            continue
        else:
            new_password = encoding(new_password.upper())
            break
    if new_password.lower() == 'take me back':
        return cust_intro()
    return new_password


# In[14]:


def store_fname():
    print("\nPLEASE ENTER YOUR FIRST NAME\n\nYou can enter 'take me back' to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        f_name = str(input())
        if f_name.lower() == 'take me back':
            ipd.clear_output()
            return cust_intro()
            break
        else:
            return f_name
            break


# In[15]:


def store_lname():
    print("\nPLEASE ENTER YOUR LAST NAME\n\nYou can enter 'take me back' to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        l_name = str(input())
        if l_name.lower() == 'take me back':
            ipd.clear_output()
            return cust_intro()
            break
        else:
            return l_name
            break


# In[16]:


def store_st_address():
    print("\nPLEASE ENTER YOUR STREET ADDRESS\n\nYou can enter 'take me back' to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        st_address = str(input())
        if st_address.lower() == 'take me back':
            ipd.clear_output()
            return cust_intro()
            break
        else:
            return st_address[0].upper()+st_address[1:].lower()
            break


# In[17]:


def store_city():
    print("\nPLEASE ENTER YOUR CITY\n\nYou can enter 'take me back' to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        city = str(input())
        if city.lower() == 'take me back':
            ipd.clear_output()
            return cust_intro()
            break
        else:
            return city[0].upper()+city[1:].lower()
            break


# In[18]:


def store_province():
    print("\nPLEASE ENTER YOUR PROVINCE CODE\n\n***MAKE SURE YOU ENTER THE PROVINCE CODE, AND NOT THE FULL PROVINCE***\n\nYou can enter 'take me back' to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        try:
            province = str(input())
            if province.lower() == 'take me back':
                ipd.clear_output()
                break
            assert len(province) == 2
            spl_check(province)
        except:
            print("\n***INVALID PROVINCE CODE***\n\nTHE PROVINCE CODE MUST CONTAIN ONLY 2 LETTERS AND MUST NOT CONTAIN SPECIAL CHARACTERS\n\nYou can enter 'take me back' to return to the previous menu")
            continue
        else:
            break
    if province.lower() == 'take me back':
        return cust_intro()
    return province.upper()


# In[19]:


def store_zipcode():
    print("\nPLEASE ENTER YOUR POSTAL CODE WITHOUT SPACES\n\n***MAKE SURE YOU ENTER THE POSTAL CODE WITHOUT ANY SPACES***\n\nYou can enter 'take me back' to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        try:
            zipcode = str(input())
            if zipcode.lower() == 'take me back':
                ipd.clear_output()
                break
            assert len(zipcode) == 6
            spl_check(zipcode)
        except:
            print("\n***INVALID POSTAL CODE***\n\nTHE POSTAL CODE MUST CONTAIN ONLY 6 CHARACTERS AND MUST NOT INCLUDE SPECIAL CHARACTERS (INCLUDING SPACES)\n\nYou can enter 'take me back' to return to the previous menu")
            continue
        else:
            break
    if zipcode.lower() == 'take me back':
        return cust_intro()
    return zipcode.upper()


# In[20]:


def store_age():
    print("\nPLEASE ENTER YOUR AGE IN NUMERALS\n\n***MAKE SURE YOU ENTER ONLY NUMBER OF YEARS IN NUMERALS***\n\nYou can enter 0 to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        try:
            age = int(input())
            if age == 0:
                ipd.clear_output()
                break
        except:
            print("\n***INVALID AGE***\n\nTHE AGE MUST CONTAIN ONLY NUMBERS (NUMBER OF YEARS)\n\nYou can enter 0 to return to the previous menu")
            continue
        else:
            break
    if age == 0:
        return cust_intro()
    return age


# In[ ]:





# In[ ]:





# In[21]:


def retrieve_new_cust():
    con = sqlite3.connect('LCS1.db')
    cur = con.cursor()
    
    cur.execute("""SELECT PersonID FROM Person
                    WHERE PersonID = (SELECT MAX(PersonID) FROM Person);""")
    latest_cust = [obj[0] for obj in cur.fetchall()]
    
    return latest_cust[0]


# In[ ]:





# # LOGIN PAGE

# In[ ]:





# In[ ]:





# In[22]:


def intro():
    print("\nWelcome! \n\nAre you \n\n1 - A Customer \n\n2 - An Employee? \n\nPlease enter the option NUMBER that applies to you most\n\nIf you would like to exit the interface, please enter '0'")
    while True:
        ipd.clear_output(wait = True)
        try:
            flag0 = int(input())
            assert flag0 in (0,1,2)
        except:
            print("\n***INVALID ENTRY. PLEASE ENTER A NUMBER FROM THE GIVEN OPTIONS.***\n\nIt has to be\n\n1 - if you are a Customer\n\n2 - if you are an Employee\n\n0 - if you would like to exit the interface\n")
        else:
            ipd.clear_output()
            break
    if flag0 == 0:
        print('\n\nHave a nice day!\n\n')
        return
    if flag0 == 1:
        cust_intro()
    if flag0 == 2:
        emp_intro()


# ## CUSTOMER LOGIN

# In[23]:


def cust_intro():
    print("\n\nThank you for choosing our services!\n\nAre you \n\n1 - An Existing Customer \n\n2 - A New Customer? \n\nPlease enter the option NUMBER that applies to you most\n\nIf you would like to return to the previous menu, please enter '0'")
    while True:
        ipd.clear_output(wait = True)
        try:
            flag1 = int(input())
            assert flag1 in (0,1,2)
        except:
            print("\n***INVALID ENTRY. PLEASE ENTER A NUMBER FROM THE GIVEN OPTIONS.***\n\nIt has to be\n\n1 - if you are An Existing Customer\n\n2 - if you are A New Customer\n\n0 - if you would like to return to the previous menu\n")
        else:
            ipd.clear_output()
            break
    if flag1 == 0:
        intro()
    if flag1 == 1:
        existing_cust()
    if flag1 == 2:
        new_cust()


# In[24]:


def new_cust():
    print("\n\n***PLEASE CREATE A NEW ACCOUNT TO PROCEED FURTHER***\n\nPLEASE ENTER YOUR DESIRED USERNAME. USERNAMES ARE CASE INSENSITIVE\n\nIf you would like to go back to the previous menu, enter 'take me back'\n\n")
    while True:
        ipd.clear_output(wait = True)
        try:
            new_username = str(input()).upper()
            if new_username == 'TAKE ME BACK':
                break
            assert new_username not in customers()
        except:
            print("\n***THIS USERNAME ALREADY EXISTS***\n\nPlease login using your existing credentials or try creating a different username\n\nYou can enter 'take me back' to return to the previous menu")
            continue
        else:
            pwd = create_pwd()
            fname = store_fname()
            lname = store_lname()
            st_address = store_st_address()
            city = store_city()
            province = store_province()
            zipcode = store_zipcode()
            age = store_age()
            
            con = sqlite3.connect('LCS1.db')
            cur = con.cursor()
                    
            cur.execute('INSERT INTO Person (Fname, Lname, [Street Address], City, Province, [Postal Code], Age) VALUES(?, ?, ?, ?, ?, ?, ?);', (fname, lname, st_address, city, province, zipcode, age))
            con.commit()
            
            Cust_ID = retrieve_new_cust()
            cur.execute('INSERT INTO Customer VALUES(?, ?, ?, ?);', (Cust_ID, new_username, pwd, 10000))
            con.commit()
            
            cur.close()
            con.close()
            ipd.clear_output()
            print("\n\nSuccessfully registered new customer!")
            break
            
#     if new_username == 'TAKE ME BACK':
#         return cust_intro()
    return cust_intro()


# In[ ]:





# In[37]:


def existing_cust():
    print("\nPlease enter your login credentials.\n\nIf you are not a registered customer, enter 'take me back' to return to the previous menu.\n\nUSERNAME")
    while True:
        ipd.clear_output(wait = True)
        
        try:
            username = str(input()).upper()
            if username == 'TAKE ME BACK':
                break
            assert username in customers()
            
        except:
            print("\n***INVALID USERNAME***\n\nThis Username does not exist. Please enter your registered Username\n\nIf you are not a registered customer, enter 'take me back' to return to the previous menu.\n\n")
            continue
            
        else:
            print("\n\nPASSWORD\n")
            while True:
                ipd.clear_output(wait = True)
                try:
                    password = str(input()).upper()
                    if password == 'TAKE ME BACK':
                        break
                    password = encoding(password)
                    con = sqlite3.connect('LCS1.db')
                    cur = con.cursor()
                    
                    cur.execute('SELECT CustomerPWD FROM Customer WHERE CustomerLogin = ?;', (username,))
                    stored_pwd = cur.fetchall()[0][0]
                    
                    assert password == stored_pwd
                    
                except:
                    print("\n***INVALID PASSWORD***\n\nPlease enter the correct password associated with your username\n\n")
                    
                    cur.close()
                    con.close()
                    
                    continue
                    
                else:
                    ipd.clear_output()
                    print("\nLOGIN SUCCESFUL!\n\n")
                    
                    cur.execute('SELECT CustomerID FROM Customer WHERE CustomerLogin = ?;', (username,))
                    customer_id = cur.fetchall()[0][0]
                    
                    cur.execute('SELECT Fname, Lname FROM Person WHERE PersonID = ?;', (customer_id,))
                    name = cur.fetchall()[0]
                    
                    
                    cur.close()
                    con.close()
                    
                    break
            if password == 'TAKE ME BACK':
                break
            return cust_login_options(name, customer_id)
            
    if username == 'TAKE ME BACK':
        return cust_intro()


# In[ ]:





# In[26]:


def cust_login_options(name, customer_id):
    print("\nWELCOME {} {}! HOW CAN WE ASSIST YOU TODAY? \n\n1 - Track package \n\n2 - View Dashboard\n\nPlease enter the option NUMBER that applies to you most\n\nIf you would like to quit the interface, please enter '0'".format(name[0], name[1]))
    while True:
        ipd.clear_output(wait = True)
        try:
            flag2 = int(input())
            assert flag2 in (0,1,2)
        except:
            print("\n***INVALID ENTRY. PLEASE ENTER A NUMBER FROM THE GIVEN OPTIONS.***\n\nIt has to be\n\n1 - if you want to Track a Package\n\n2 - if you want to view your Dashboard\n\n0 - if you want to quit the interface")
        else:
            ipd.clear_output()
            break
    if flag2 == 0:
        print('\n\nHave a nice day!\n\n')
    if flag2 == 1:
        track_package(name, customer_id)
    if flag2 == 2:
        return display_dash(name, customer_id)
    return


# In[27]:


def display_dash(name, customer_id):
    con = sqlite3.connect('LCS1.db')
    cur = con.cursor()

    query5 = """SELECT PackID, [Total Cost] AS Expenditure, Status
               FROM Pack
               WHERE PackCustomerID = {};""".format(2,)

    df_viz5 = pd.read_sql(query5, con=con)



    sns.barplot(x = df_viz5.PackID, y = df_viz5.Expenditure, hue = df_viz5.Status)

    plt.title('Bar chart for Expenditure on various packs')
    plt.show()
    
    print('\n\n\n')
    display(df_viz5)
    
    cur.close()
    con.close()
    
    cust_login_options(name, customer_id)


# In[28]:


def track_package(name, customer_id):
    print("\nPLEASE ENTER THE PACK ID OF THE PACKAGE YOU WANT TO TRACK\n\nYou can enter 0 to return to the previous menu")
    while True:
        ipd.clear_output(wait = True)
        try:
            pid = int(input())
            if pid == 0:
                break
            assert pid in check_valid_pack(customer_id)
        except:
            print("\n***ACCESS DENIED!***\n\nPLEASE ENTER A PACK ID ASSOCIATED WITH YOUR ACCOUNT\n\nYou can enter 0 to return to the previous menu")
        else:
            ipd.clear_output()
            
            con = sqlite3.connect('LCS1.db')
            cur = con.cursor()
            
            query = """SELECT DISTINCT A.PackID, [Total Cost], OrderDate, Status, [Last Updated], ProductName, Quantity, IsActive
                                FROM (SELECT P.PackID as PackID, P.[Total Cost] AS [Total Cost],
                                     P.OrderDate AS OrderDate, R.Status AS Status,
                                     R.[Last Updated] AS [Last Updated], R.Active AS IsActive
                                     FROM Pack P LEFT JOIN Route R
                                     ON P.PackID = R.PackID
                                     WHERE P.PackID = {}) A
                                INNER JOIN 
                                    (SELECT Pl.PackID AS PackID, Pr.ProductName AS ProductName,
                                     Pl.Quantity AS Quantity
                                     FROM Packline Pl INNER JOIN Product Pr ON Pl.ProductID = Pr.ProductID
                                     WHERE Pl.PackID = {}) B
                                ON A.PackID = B.PackID;""".format(pid, pid)
            
            
            df_ora = pd.read_sql(query, con=con)
            cur.close()
            con.close()
            
            display(df_ora)
            break
    if pid == 0:
        print('\n\nHave a nice day!\n\n')
        return
    return cust_login_options(name, customer_id)


# In[ ]:





# ## EMPLOYEE LOGIN

# In[29]:


def emp_intro():
    print("\nPlease enter your login credentials.\n\nIf you are not an employee, enter 'take me back' to return to the previous menu.\n\nUSERNAME")
    while True:
        ipd.clear_output(wait = True)
        
        try:
            username = str(input()).upper()
            if username == 'TAKE ME BACK':
                break
            assert username in employees()
            
        except:
            print("\n***INVALID USERNAME***\n\nThis Username does not exist. Please enter your registered Username\n\nIf you are not an employee, enter 'take me back' to return to the previous menu.\n\n")
            continue
            
        else:
            print("\n\nPASSWORD\n")
            while True:
                ipd.clear_output(wait = True)
                try:
                    password = str(input()).upper()
                    if password == 'TAKE ME BACK':
                        break
                    password = encoding(password)
                    con = sqlite3.connect('LCS1.db')
                    cur = con.cursor()
                    
                    cur.execute('SELECT EmployeePWD FROM Employee WHERE EmployeeLogin = ?;', (username,))
                    stored_pwd = cur.fetchall()[0][0]
                    
                    assert password == stored_pwd
                    
                except:
                    print("\n***INVALID PASSWORD***\n\nPlease enter the correct password associated with your username\n\n")
                    
                    cur.close()
                    con.close()
                    
                    continue
                    
                else:
                    ipd.clear_output()
                    print("\nLOGIN SUCCESFUL!\n\n")
                    
                    cur.execute('SELECT EmployeeID FROM Employee WHERE EmployeeLogin = ?;', (username,))
                    employee_id = cur.fetchall()[0][0]
                    
                    cur.execute('SELECT [Employee Role] FROM Employee WHERE EmployeeLogin = ?;', (username,))
                    emp_role = cur.fetchall()[0][0]
                    
                    cur.execute('SELECT Fname, Lname FROM Person WHERE PersonID = ?;', (employee_id,))
                    name = cur.fetchall()[0]
                    
                    
                    cur.close()
                    con.close()
                    
                    break
            if password == 'TAKE ME BACK':
                break
            return emp_login_options(name, employee_id, emp_role)
            
    if username == 'TAKE ME BACK':
        return intro()


# In[30]:


def emp_login_options(name, employee_id, emp_role):
    if emp_role in ['Admin', 'CEO']:
        print("\nWELCOME {} {}! HOW CAN WE ASSIST YOU TODAY? \n\n1 - View Customer Requests \n\n2 - Update other tables \n\n3 - View Dashboard\n\nPlease enter the option NUMBER that applies to you most\n\nIf you would like to quit the interface, please enter '0'".format(name[0], name[1]))
        while True:
            ipd.clear_output(wait = True)
            try:
                flag3 = int(input())
                assert flag3 in (0,1,2,3)
            except:
                print("\n***INVALID ENTRY. PLEASE ENTER A NUMBER FROM THE GIVEN OPTIONS.***\n\nIt has to be\n\n1 - if you want to view customer requests\n\n2 - if you want to Update tables\n\n3 - if you want to view Dashboard\n\n0 - if you want to quit the interface")
            else:
                ipd.clear_output()
                break
        if flag3 == 0:
            print('\n\nHave a nice day!\n\n')
        if flag3 == 1:
            view_requests(name, employee_id, emp_role)
        if flag3 == 2:
            update_tables(name, employee_id, emp_role)
        if flag3 == 3:
            display_emp_dash(name, employee_id, emp_role)
        return
    else:
        print("\nWELCOME {} {}! HOW CAN WE ASSIST YOU TODAY? \n\n1 - Check tasks \n\n2 - View Dashboard\n\nPlease enter the option NUMBER that applies to you most\n\nIf you would like to quit the interface, please enter '0'".format(name[0], name[1]))
        while True:
            ipd.clear_output(wait = True)
            try:
                flag4 = int(input())
                assert flag4 in (0,1,2)
            except:
                print("\n***INVALID ENTRY. PLEASE ENTER A NUMBER FROM THE GIVEN OPTIONS.***\n\nIt has to be\n\n1 - if you want to Check tasks\n\n2 - if you want to view Dashboard\n\n0 - if you want to quit the interface")
            else:
                ipd.clear_output()
                break
        if flag4 == 0:
            print('\n\nHave a nice day!\n\n')
        if flag4 == 1:
            check_tasks(name, employee_id, emp_role)
        if flag4 == 2:
            display_emp_dash(name, employee_id, emp_role)
        return


# In[ ]:





# In[31]:


def update_tables(name, employee_id, emp_role):
    print("\n\nENTER YOUR UPDATE QUERY HERE\n\nYou can also enter 0 to return to the previous menu\n\n")
    query = str(input())
    
    if query == '0':
        return emp_login_options(name, employee_id, emp_role)
    
    con = sqlite3.connect('LCS1.db')
    cur = con.cursor()
    
    cur.execute(query)
    con.commit()
    
    ipd.clear_output(wait = True)
    
    cur.close()
    con.close()
    
    print("\n\nUPDATES SUCCESSFULLY EXECUTED!\n\n")
    return emp_login_options(name, employee_id, emp_role)


# In[ ]:





# In[32]:


def display_emp_dash(name, employee_id, emp_role):
    if emp_role in ['Admin', 'CEO']:
        con = sqlite3.connect('LCS1.db')
        cur = con.cursor()

        query1 = """SELECT Pr.ProductName AS ProductName, SUM(Pl.Cost) AS Revenue
                   FROM Packline Pl INNER JOIN Product Pr ON
                                 Pl.ProductID = Pr.ProductID
                                 GROUP BY Pr.ProductName;"""

        df_viz1 = pd.read_sql(query1, con=con)



        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        Prods = df_viz1['ProductName']
        Revenue = df_viz1['Revenue']
        ax.pie(Revenue, labels = Prods ,autopct='%1.2f%%')

        plt.title('Pie chart for revenue generated by different products')
        plt.show()


        display(df_viz1)
        print('\n\n\n')



        query2 = """SELECT WarehouseID, [Storage Capacity], [Remaining Capacity]
                    FROM Warehouse;"""

        df_viz2 = pd.read_sql(query2, con=con)
        print('\n\n\n')


        df_viz2[["WarehouseID", "Storage Capacity", "Remaining Capacity"]].plot(x="WarehouseID", kind="bar")
        plt.title('Barchart for storage capacities of different Warehouses')
        plt.xticks(rotation=45)
        plt.show()


        display(df_viz2)

        cur.close()
        con.close()
        
        emp_login_options(name, employee_id, emp_role)
    
    else:
        con = sqlite3.connect('LCS1.db')
        cur = con.cursor()

        query3 = """SELECT VehicleID, Make, [Kms Traveled] AS Miles
                   FROM Vehicle;"""

        df_viz3 = pd.read_sql(query3, con=con)
        
        sns.barplot(x = df_viz3.VehicleID, y = df_viz3.Miles, hue = df_viz3.Make)
        plt.title('Miles Traveled by each vehicle segregated by Vehicle Make')
        plt.show()
        
        print('\n\n\n')
        display(df_viz3)
        
        cur.close()
        con.close()
        
        emp_login_options(name, employee_id, emp_role)


# In[33]:


def view_requests(name, employee_id, emp_role):
    print("\n\nNO CUSTOMER REQUESTS AVAILABLE, YOU'RE ALL CAUGHT UP. PLEASE CHECK LATER!")
    return emp_login_options(name, employee_id, emp_role)


# In[34]:


def check_tasks(name, employee_id, emp_role):
    print("\n\nNO TASKS CURRENTLY AVAILABLE! YOU WILL BE NOTIFIED WHEN NEW TASKS ARE ADDED\n\n")
    return emp_login_options(name, employee_id, emp_role)


# In[ ]:





# In[35]:


# %run LCS.py


# In[38]:


intro()

