from accounts import CustomerAccount
from transactions import CustOpers


if __name__ == "__main__" :
    accounts = CustomerAccount.ACCOUNTS
    transactions = CustomerAccount.TRANSACTIONS

    dave = CustomerAccount(1, 'Dave', 'Bale', balance=100, tz=(0, 'UTC'))
    alan = CustomerAccount(2, 'Alan', 'Jerme', balance=1000, tz=(-8, 'PST'))
    judy = CustomerAccount(3, 'Judy', 'Kie', balance=10000, tz=(-7, 'MST'))
    kate = CustomerAccount(4, 'Kate', 'Blep', balance=100000, tz=(-5, 'EST'))

    accounts.apply_interest()

    # for account in accounts._accounts :
    #     print(account.balance)
    
    confirmation_code = dave.transaction(CustOpers.WITHDRAW,100)
    print(confirmation_code)

    for transaction in transactions.LEDGER.values() :
        print(transaction)

    withdrawl_receipt = transactions.deliver_transaction(confirmation_code)

    print(withdrawl_receipt)
