# bank
import random

class Bank():

    no_of_banks = 0

    def __init__(self, name, location):
        self.id = Bank.no_of_banks + 1
        self.name = name
        self.location = location
        self.accounts = {}
        self.customers = {}
        self.tellers = {}
        self.loans = {}

        Bank.no_of_banks += 1


class Teller():

    no_of_tellers = 0

    def __init__(self, name, bank):
        self.id = Teller.no_of_tellers + 1
        self.name = name
        self.bank = bank
        self.bank.tellers.update({self.id:self})
        Teller.no_of_tellers += 1

    def collect_money(self, account_id, amount):
        current_amount = self.bank.accounts[account_id]
        self.bank.accounts[account_id] = current_amount + amount

    def open_account(self, customer, account_type, amount):
        if account_type.lower() in ["savings", "checking"]:
            if not customer.id in self.bank.customers:
                self.bank.customers.update({customer.id:customer})

            if account_type.lower() == "savings":
                account = SavingsAccount(customer.id, amount)
                self.bank.accounts.update({account.id:account})
                return account.id
            else:
                account = CheckingAccount(customer.id, amount)
                self.bank.accounts.update({account.id: account})
                return account.id

        else:
            raise Exception("Invalid Account type")

    def close_account(self, account_id):
        del self.bank.accounts[account_id]

    def loan_request(self, customer, loan_type, amount):
        if not loan_type.lower() in ["short", "long"]:
            raise Exception("Invalid Loan Type")
        message = None
        if loan_type.lower() == "short":
            if amount < 100_000:
                raise Exception("Minimum allowed short term loan is UGX 100,000.")
        if amount < 500_000:
            raise Exception("Minimum allowed long term loan is UGX 500,000.")

        current_balance = self.bank.accounts[customer.account_id].account_balace
        if current_balance > 0.25*amount:
            loan = Loan(loan_type.lower(), customer.id, amount)
            self.bank.loans.update({loan.id:loan})
            return loan.id
        else:
            raise Exception("You must have at least a quarter of the loan amount in your account")

    def provide_info(self, customer):
        return str("-"*40 + "\n{} Customer Information\n".format(self.bank.name)) +  \
            str(("="*40 + "\nName: {}\nAccount Type: {}\nAccount Number: {}\nAccount Balance: {}\n" + "-"*40 + "\n\n").format(customer.name,self.bank.accounts[customer.account_id].type, self.bank.accounts[customer.account_id].account_no, self.bank.accounts[customer.account_id].account_balance))

    def issue_card(self, customer):
        print("Issuing card to", customer.name)


class Customer():

    no_of_customers = 0

    def __init__(self, name, address, phone_no):
        self.id = Customer.no_of_customers + 1
        self.name = name
        self.address = address
        self.phone_no = phone_no
        self.account_id = None
        self.loan_id = None

        Customer.no_of_customers += 1

    def general_inquiry(self, teller):
        return teller.provide_info(self)

    def deposit_money(self, teller, account_id, amount):
        teller.collect_money(account_id, amount, "deposit")

    def withdraw_money(self, teller, account_id, amount):
        pass

    def open_account(self, teller, account_type, initial_amount):
        self.account_id = teller.open_account(self, account_type, initial_amount)

    def close_account(self, teller, account_id):
        teller.close_account(self.account_id)
        self.account_id = None

    def apply_for_loan(self, teller, loan_type, amount):
        teller.loan_request(self, loan_type, amount)

    def request_card(self, teller):
        print("Requesting Card...")
        teller.issue_card(self)

class Account():

    no_of_accounts = 0
    account_nos = []

    def __init__(self, customer_id, amount, acc_type):
        self.id = Account.no_of_accounts + 1
        self.customer_id = customer_id
        self.account_balance = amount
        self.account_no = None
        self.type = acc_type
        while True:
            x = random.randint(1000000000,9999999999)
            if not x in Account.account_nos:
                self.account_no = x
                Account.account_nos.append(self.account_no)
                break
        Account.no_of_accounts += 1


class CheckingAccount(Account):
    def __init__(self, customer_id, amount):
        super().__init__(customer_id, amount, "Checking")

class SavingsAccount(Account):
    def __init__(self, customer_id, amount):
        super().__init__(customer_id, amount, "Savings")

class Loan():

    no_of_loans = 0

    def __init__(self, loan_type, customer_id, amount):
        self.id = Loan.no_of_loans + 1
        self.loan_type = loan_type
        self.amount = amount
        self.customer_id = customer_id
        self.rate = None
        self.time_period = None
        self.frequency = None
        self.payment = None

        if loan_type.lower() == "short":
            self.rate = 0.2
            self.time_period = 1
            self.frequency = self.amount // 12
            self.payment = self.amount + (self.amount * self.rate * self.time_period)

        else:
            self.rate = 0.1
            self.time_period = 6
            self.frequency = self.amount // 6
            self.payment = self.amount + (self.amount * self.rate * self.time_period)

        Loan.no_of_loans += 1

        def __str__(self):
            return "="*40 + \
                self.loan_type.title()
