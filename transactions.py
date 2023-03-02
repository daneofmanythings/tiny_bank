
from abc import ABC, abstractclassmethod
from datetime import datetime
from enum import Enum


class CustActions(Enum) :
    DEPOSIT = 'D'
    WITHDRAW = 'W'
    INTEREST = 'I'
    DECLINED = 'X'


class Transaction(ABC) :
    '''Contains relevant information to record a Transaction.'''
    pass


class Transactions(ABC) :
    transactions: dict[int:Transaction]

    @abstractclassmethod
    def process_transaction(cls, account, action, value) -> str :
        '''Entry point for executing and logging an action on an account.
        makes calls to _generate_transaction_id and _execute_transaction
        to get the ID and transaction object for logging in the ledger with
        _record transaction.'''
        pass

    @abstractclassmethod
    def deliver_transaction(cls, confirmation_code:str) -> Transaction :
        '''Takes a conformation code and returns the transaction object that
        corresponds to the code from the LEDGER.'''
        pass
    
    @abstractclassmethod
    def _generate_transaction_id(cls) -> int :
        '''Generates the confirmation id. Contains logic to avoid collisions'''

    @abstractclassmethod
    def _execute_transaction(cls, account, action, value) -> Transaction :
        '''Executes the transaction and returns the transaction object'''

    @abstractclassmethod
    def _record_transaction(cls, transaction_id:int, transaction:Transaction) -> str :
        '''Inserts the transaction object into the LEDGER at key transaction_id
        and returns a confirmation string as a record of completion'''
        pass


class CustomerTransaction(Transaction) :
    
    def __init__(self, transaction_code, amount, balance, account_number, time) -> None:
        self.transaction_code:str = transaction_code
        self.amount:float = amount
        self.balance:float = balance
        self.account_number:int = account_number
        self.time:datetime = time
        self.time_utc:datetime = datetime.utcnow()

    def __str__(self) -> str :
        boundary = '-----------------\n'
        acc_num = f'Account number: {self.account_number}\n'
        code = f'Code: {self.transaction_code}\n'
        amount = f'Amount: {self.amount}\n'
        up_bal = f'Updated Balance: {self.balance}\n'
        time = f'Time (UTC): {self.time_utc}\n'
        return boundary + acc_num + code + amount + up_bal + time


class CustomerTransactions(Transactions) :
    LEDGER:dict[int:Transaction] = dict()

    @classmethod
    def process_transaction(cls, account, action, value) -> str :
        '''Implementation follows the abstraction. Returns the
        confirmation_code string from _record_transaction to the caller
        of this process.'''
        transaction_id = cls._generate_transaction_id()
        receipt = cls._execute_transaction(account, action, value)
 
        return cls._record_transaction(transaction_id, receipt)

    @classmethod
    def deliver_transaction(cls, confirmation_code:str) -> CustomerTransaction: 
        '''Identifies which object to grab out of the LEDGER based soley on the
        confirmation id which was coded into the confirmation code.'''
        key = int(confirmation_code.split('-')[-1])
        return cls.LEDGER[key]

    @classmethod
    def _generate_transaction_id(cls) -> int :
        '''Uses the length of the LEDGER to as the starting point for the
        ID. Increments to avoid collisions.'''
        conf_id = len(cls.LEDGER)
        while True :
            try :
                cls.LEDGER[conf_id]
            except KeyError:
                break
            conf_id += 1
        return conf_id

    @classmethod
    def _execute_transaction(cls, account, action, value) -> Transaction :
        '''Generates the confirmation id and executes the transaction inline with
        generating the receipt. The action is being executed here to keep it as close 
        to the record keeping as possible to avoid errors which would cause an
        action to be executed but not recorded.'''
        return CustomerTransaction(
            action(value),  # <- Actual operation updating account happens here
            value,
            account.balance,
            account.account_num,
            datetime.now(account.timezone),
        )
        
    @classmethod
    def _record_transaction(cls, transaction_id, transaction:CustomerTransaction) -> str :
        '''Implementation of the confirmation string comes from the specs
        to build this object.'''
        cls.LEDGER[transaction_id] = transaction
        return '{}-{}-{}-{}'.format(
            transaction.transaction_code,
            transaction.account_number,
            date_to_str(transaction.time_utc),
            transaction_id,
        )
    
# HELPER FUNCTION

def date_to_str(date:datetime) -> str :
    chars = '- :'
    date_str = str(date).split('.')[0]
    for char in chars :
        date_str = date_str.replace(char, '')

    return date_str
