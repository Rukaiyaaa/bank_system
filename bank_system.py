from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    account_counter = 1000
    
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_no = Account.account_counter
        self.account_type = account_type
        self.balance = 0
        self.transactions = []
        self.loans_taken = 0
        Account.accounts.append(self)
        Account.account_counter += 1

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount}")
            print(f"\n--> Deposited {amount}. New balance: ${self.balance}")
        else:
            print("\n--> Invalid deposit amount")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount}")
            print(f"\n--> Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Withdrawal amount exceeded")

    def check_balance(self):
        print(f"\n--> Current balance: ${self.balance}")

    def show_transaction_history(self):
        print("\n--> Transaction History:")
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self, amount):
        if self.loans_taken < 2:
            self.balance += amount
            self.transactions.append(f"Loan taken ${amount}")
            self.loans_taken += 1
            print(f"\n--> Loan taken {amount}. New balance: ${self.balance}")
        else:
            print("\n--> Loan limit reached (max 2 loans allowed)")

    def transfer(self, amount, target_account_no):
        target_account = None
        for account in Account.accounts:
            if account.account_no == target_account_no:
                target_account = account
                break
        if target_account:
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                target_account.balance += amount
                self.transactions.append(f"Transferred ${amount} to account {target_account_no}")
                target_account.transactions.append(f"Received ${amount} from account {self.account_no}")
                print(f"\n--> Transferred {amount} to account {target_account_no}. New balance: ${self.balance}")
            else:
                print("\n--> Invalid transfer amount or insufficient funds")
        else:
            print("\n--> Account does not exist")

    @abstractmethod
    def show_info(self):
        pass


class SavingsAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "savings")

    def show_info(self):
        print(f"\nInfos of {self.account_type} account of {self.name}:")
        print(f'\tAccount No : {self.account_no}')
        print(f'\tEmail : {self.email}')
        print(f'\tAddress : {self.address}')
        print(f'\tCurrent Balance : ${self.balance}')


class CurrentAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "current")

    def show_info(self):
        print(f"\nInfos of {self.account_type} account of {self.name}:")
        print(f'\tAccount No : {self.account_no}')
        print(f'\tEmail : {self.email}')
        print(f'\tAddress : {self.address}')
        print(f'\tCurrent Balance : ${self.balance}')


class Bank:
    def __init__(self):
        self.total_balance = 0
        self.total_loan = 0
        self.loan_status = True
        self.accounts = Account.accounts

    def create_account(self, name, email, address, account_type):
        if account_type == "savings":
            new_account = SavingsAccount(name, email, address)
        else:
            new_account = CurrentAccount(name, email, address)
        print(f"\n--> Account created with Account Number: {new_account.account_no}")

    def delete_account(self, account_no):
        for account in self.accounts:
            if account.account_no == account_no:
                self.accounts.remove(account)
                print(f"\n--> Account {account_no} deleted")
                return
        print("\n--> Account not found")

    def show_users(self):
        print("\n--> List of all users:")
        for account in self.accounts:
            account.show_info()

    def check_total_balance(self):
        self.total_balance = sum(account.balance for account in self.accounts)
        print(f"\n--> Total available balance in the bank: ${self.total_balance}")

    def check_total_loan(self):
        self.total_loan = sum(account.loans_taken for account in self.accounts)
        print(f"\n--> Total loan amount in the bank: ${self.total_loan}")

    def off_loan(self):
        self.loan_status = False
        print("\n--> Loan feature turned off")

    def on_loan(self):
        self.loan_status = True
        print("\n--> Loan feature turned on")


# Main program

bank = Bank()
current_user = None

while True:
    if current_user is None:
        print("\n--> No user logged in !")
        ch = input("\n--> Register/Login/Admin (R/L/A) : ")
        if ch == "R":
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            account_type = input("Account Type (savings/current): ")
            bank.create_account(name, email, address, account_type)
        elif ch == "L":
            account_no = int(input("Account Number: "))
            for account in Account.accounts:
                if account.account_no == account_no:
                    current_user = account
                    break
            if current_user is None:
                print("\n--> Account not found")
        elif ch == "A":
            while True:
                print("\nAdmin Menu:")
                print("1. Create Account")
                print("2. Delete Account")
                print("3. Show Users")
                print("4. Check Total Balance")
                print("5. Check Total Loan")
                print("6. Turn Off Loan Feature")
                print("7. Turn On Loan Feature")
                print("8. Logout")

                admin_choice = int(input("Choose Option: "))

                if admin_choice == 1:
                    name = input("Name: ")
                    email = input("Email: ")
                    address = input("Address: ")
                    account_type = input("Account Type (savings/current): ")
                    bank.create_account(name, email, address, account_type)
                elif admin_choice == 2:
                    account_no = int(input("Account Number to Delete: "))
                    bank.delete_account(account_no)
                elif admin_choice == 3:
                    bank.show_users()
                elif admin_choice == 4:
                    bank.check_total_balance()
                elif admin_choice == 5:
                    bank.check_total_loan()
                elif admin_choice == 6:
                    bank.off_loan()
                elif admin_choice == 7:
                    bank.on_loan()
                elif admin_choice == 8:
                    break
                else:
                    print("Invalid Option")
    else:
        print(f"\nWelcome {current_user.name} !")
        if current_user.account_type == "savings":
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Check Balance")
            print("4. Show Info")
            print("5. Show Transaction History")
            print("6. Take Loan")
            print("7. Transfer")
            print("8. Logout")

            user_choice = int(input("Choose Option: "))

            if user_choice == 1:
                amount = float(input("Enter withdraw amount: "))
                current_user.withdraw(amount)
            elif user_choice == 2:
                amount = float(input("Enter deposit amount: "))
                current_user.deposit(amount)
            elif user_choice == 3:
                current_user.check_balance()
            elif user_choice == 4:
                current_user.show_info()
            elif user_choice == 5:
                current_user.show_transaction_history()
            elif user_choice == 6:
                if bank.loan_status:
                    amount = float(input("Enter loan amount: "))
                    current_user.take_loan(amount)
                else:
                    print("\n--> Loan feature is currently off")
            elif user_choice == 7:
                amount = float(input("Enter transfer amount: "))
                target_account_no = int(input("Enter target account number: "))
                current_user.transfer(amount, target_account_no)
            elif user_choice == 8:
                current_user = None
            else:
                print("Invalid Option")
        else:
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Check Balance")
            print("4. Show Info")
            print("5. Show Transaction History")
            print("6. Take Loan")
            print("7. Transfer")
            print("8. Logout")

            user_choice = int(input("Choose Option: "))

            if user_choice == 1:
                amount = float(input("Enter withdraw amount: "))
                current_user.withdraw(amount)
            elif user_choice == 2:
                amount = float(input("Enter deposit amount: "))
                current_user.deposit(amount)
            elif user_choice == 3:
                current_user.check_balance()
            elif user_choice == 4:
                current_user.show_info()
            elif user_choice == 5:
                current_user.show_transaction_history()
            elif user_choice == 6:
                if bank.loan_status:
                    amount = float(input("Enter loan amount: "))
                    current_user.take_loan(amount)
                else:
                    print("\n--> Loan feature is currently off")
            elif user_choice == 7:
                amount = float(input("Enter transfer amount: "))
                target_account_no = int(input("Enter target account number: "))
                current_user.transfer(amount, target_account_no)
            elif user_choice == 8:
                current_user = None
            else:
                print("Invalid Option")
