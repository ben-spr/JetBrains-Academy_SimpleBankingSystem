import random
import math
import sqlite3

iin = '400000'  # issuer identification number


class Account:
    balance: float
    cardNo: int
    accountNumber: str
    pin: str


    def __init__(self, accountNumber):
        if type(accountNumber) == int:
            self.accountNumber == '{:09d}'.format(accountNumber)
        elif type(accountNumber) == str:
            self.accountNumber = accountNumber
        self.checksum = luhn(iin + self.accountNumber)
        self.cardNo = (iin + self.accountNumber + self.checksum)
        # self.cardNo = (iin + '{:09d}'.format(accountNumber) + self.checksum)
        # self.checksum = luhn(iin + str(self.accountNumber))
        # self.cardNo = (iin + str(accountNumber) + self.checksum)
        self.pin = '{:04d}'.format(math.floor(random.randrange(0000, 10000)))
        self.balance = 0


class DB(object):

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.con = None


    def __enter__(self):
        self.con = sqlite3.connect(self.connection_string)
        self.cur = self.con.cursor()


    def __exit__(self):
        self.con.commit()
        self.con.close()
        self.con = None

def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def luhn(number):
    x = [int(x) for x in number[0:15]]
    for i in range(0, len(x), 2):
        x[i] = x[i] * 2
        if x[i] > 9:
            x[i] -= 9
    checksum = 10 - (sum(x) % 10)
    checksum = checksum % 10
    return str(checksum)


def startMenu():
    global currentAcc
    while True:
        print("1: Create an account\n2: Log into an account\n0: Exit")
        userInput = input()
        if userInput == '1':
            currentAcc = create_account()
        elif userInput == '2':
            login()
        elif userInput == '0':
            exitProgram()
        # else:
        #     userInput = input("\nInvalid input. Please choose a valid option:\n")


def accountMenu(selectedAcc):
    accNo, cardNo, pin, balance = selectedAcc
    accNo = '{:09d}'.format(accNo)
    currentAcc = Account(accNo)
    currentAcc.balance = balance
    currentAcc.pin = pin
    accountActions = dict()
    accountActions["1"] = ("Balance", showbalance)
    accountActions["2"] = ("Add income", add_income)
    accountActions["3"] = ("Do transfer", transfer)
    accountActions["4"] = ("Close account", close_account)
    accountActions["5"] = ("Log out", log_out)
    accountActions["0"] = ("Exit", exitProgram)
    while True:
        #print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        for x in accountActions.keys():
            print("{}. {}".format(x, accountActions.get(x)[0]))
        userInput = input()
        try:
            choice = accountActions[userInput]
            choice[1](currentAcc)
        except KeyError:
            print("Invalid choice!")
            continue

        #if userInput in accountActions.keys:
        #accountActions.get(userInput,[None,print("Invalid key")])[1]
        """if userInput == '1':
            print("\nBalance: {}\n".format(balance))
            continue
        elif userInput == '2':
            print("\nYou have successfully logged out!\n")
            startMenu()
        elif userInput == '0':
            exitProgram()"""
        # else:
        #     userInput = input("\nInvalid input. Please choose a valid option:\n")


def create_db_connection(db):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        return con, cur
    except:
        print("Error: couldn't connect to database")


def update_account_balance(account):
    with con:
        cur.execute("""UPDATE card
        SET balance=?
        WHERE id=?;""", (account.balance, account.accountNumber))
    pass


def initialize_db_table(con, cur):
    if con is not None:
        cur.execute("""CREATE TABLE IF NOT EXISTS card (
            id INTEGER NOT NULL, 
            number TEXT NOT NULL, 
            pin TEXT, 
            balance INTEGER DEFAULT 0
            );""")
        con.commit()
        # cur.execute("SELECT * FROM CARD")
    else:
        print("Error! Couldn't connect to database.")


def create_account():
    while True:
        accNo = '{:09d}'.format(round(random.randrange(0, 999999999)))
        # print("Looking up account number " + accNo + " in database:")
        cur.execute("SELECT * FROM card WHERE id=?", (accNo,))
        matches = cur.fetchall()
        if matches == []:
            currentAcc = Account(accNo)
            with con:
                cur.execute("INSERT INTO card (id, number, pin) VALUES (?, ?, ?);", (currentAcc.accountNumber, currentAcc.cardNo, currentAcc.pin))
            print('Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}'.format(currentAcc.cardNo, currentAcc.pin))
            return currentAcc

def showbalance(currentAcc):
    with con:
        cur.execute("SELECT * FROM card WHERE id=?", (currentAcc.accountNumber,))
        currentAcc.balance = cur.fetchone()[3]
    # accNo, cardNo, pin, balance = selectedAcc
    # currentAcc = Account(accNo)
    # currentAcc.balance = balance
    # currentAcc.pin = pin        
    print("\nBalance: {}\n".format(currentAcc.balance))
    return currentAcc


def add_income(currentAcc):
    while True:
        income = input("\nEnter income:\n")
        if isfloat(income) == True and float(income) > 0:
            income = float(income)
            break
    currentAcc.balance += income
    update_account_balance(currentAcc)
    print("Income added!")


def close_account(currentAcc):
    with con:
        try:
            cur.execute("DELETE FROM card WHERE id=?", (str(currentAcc.accountNumber),))
            print("\nThe account has been closed!\n")
        except:
            print("An error occured while closing your account")
    startMenu()


def check_card_number(cardno):
    if len(cardno) == 16 and cardno.isdigit() == True:
        if luhn(cardno[0:15]) == cardno[-1]:
            return True
            """with con:
                try:
                    cur.execute("SELECT * FROM card WHERE number=?", (accountInput,))
                    transfer_account = cur.fetchone()
                    if transfer_account = []:
                        print("Such a card does not exist.")
                        return False
                    else:
                        return [True, transfer_account]"""
        else:
            print("Probably you made a mistake in the card number. Please try again!") # card number wrong
            return False
    else:
        print("Probably you made a mistake in the card number. Please try again!")
        return False


def transfer(currentAcc):
    print("\nTransfer\n")

    transfer_cardno = input("Enter card number:\n")
    # number_validity, transfer_account = check_card_number(transfer_cardno)
    if transfer_cardno == currentAcc.cardNo:
        print("You can't transfer money to the same account!")
    elif check_card_number(transfer_cardno) == True:
        with con:
            cur.execute("SELECT * FROM card WHERE number=?", (transfer_cardno,))
            transfer_account = cur.fetchone()
            if transfer_account == [] or transfer_account == None:
                    print("Such a card does not exist.")
            else:
                transferAcc = Account('{:09d}'.format(transfer_account[0]))   # accNo, cardNo, pin, balance
                transferAcc.balance = transfer_account[3]
                transfer_amount = input("\nEnter how much money you want to transfer:\n")
                # if transfer_amount.isdigit() == True:
                if isfloat(transfer_amount) == True:
                    transfer_amount = float(transfer_amount)
                    if transfer_amount > 0 and transfer_amount < currentAcc.balance:
                        # do the transfer and update database
                        currentAcc.balance -= transfer_amount
                        transferAcc.balance += transfer_amount
                        cur.execute("SELECT * FROM card WHERE number=? OR number=?", (currentAcc.accountNumber, transferAcc.accountNumber))
                        cur.execute("""UPDATE card SET balance=? WHERE id=?;""", (currentAcc.balance, currentAcc.accountNumber))
                        cur.execute("""UPDATE card SET balance=? WHERE id=?;""", (transferAcc.balance, transferAcc.accountNumber))
                        print("Success!")
                    elif transfer_amount > currentAcc.balance:
                        print("Not enough money!")
                    elif transfer_amount < 0:
                        print("Can't transfer a negative amount!")


def login():
    global selectedAcc
    cur.execute("SELECT count(*) FROM card")
    result = cur.fetchall()
    if result[0][0] == 0:
        print("There are no accounts to log into\n")
        startMenu()

    while True:
        selectedAcc = None
        print("\nEnter your card number:")
        try:
            accountInput = input()
            if accountInput == '0':
                exitProgram()
        except EOFError:
            pass
        print("Enter your PIN:")
        try:
            pinInput = input()
        except EOFError:
            print("Wrong card number or PIN!")
            pass
        # if accountInput==None or accountInput=='' or pinInput==None or pinInput=='':
        #     continue
        try:
            cur.execute("SELECT * FROM card WHERE number=?", (accountInput,))
            selectedAcc = cur.fetchone()
            # print(selectedAcc)
            # print(selectedAcc[2])
            if selectedAcc[2] == pinInput:
                print("You have successfully logged in!\n")
                break
        except:
            pass
        print("Wrong card number or PIN!")

    accountMenu(selectedAcc)

def log_out(currentAcc):
    selectedAcc = None
    print("\nYou have successfully logged out!\n")
    startMenu()


def exitProgram(*args):
    con.commit()
    con.close()
    exit(0)


def main():
    global con
    global cur
    con, cur = create_db_connection('card.s3db')
    initialize_db_table(con, cur)
    # bugtest()
    # print(acc.pin)
    # acc = create_account()
    startMenu()
    # con.commit()
    # con.close()


main()