from accounts import CustomerAccount, CustomerAccounts
from transactions import CustomerTransactions
from constants import CustActions

WITHDRAW = CustActions.WITHDRAW
DEPOSIT = CustActions.DEPOSIT


if __name__ == "__main__" :

    dave = CustomerAccount(1, 'Dave', 'Bale', balance=100, tz=(0, 'UTC'))
    alan = CustomerAccount(2, 'Alan', 'Jerme', balance=1000, tz=(-8, 'PST'))
    judy = CustomerAccount(3, 'Judy', 'Kie', balance=10000, tz=(-7, 'MST'))
    kate = CustomerAccount(4, 'Kate', 'Blep', balance=100000, tz=(-5, 'EST'))

    CustomerAccounts.apply_interest()

    # for account in accounts._accounts :
    #     print(account.balance)
    
    confirmation_code = dave.transaction(WITHDRAW,100)
    print(confirmation_code)

    for transaction in CustomerTransactions.LEDGER.values() :
        print(transaction)

    withdrawl_receipt = CustomerTransactions.retrieve_transaction(confirmation_code)

    print(withdrawl_receipt)
