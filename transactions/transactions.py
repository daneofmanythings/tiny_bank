from abc import ABC, abstractclassmethod

__all__ = ['Transaction', 'Transactions']


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
    def retrieve_transaction(cls, confirmation_code:str) -> Transaction :
        '''Takes a conformation code and returns the corresponding
         transaction object from the LEDGER.'''
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
