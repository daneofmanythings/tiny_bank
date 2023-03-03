from abc import ABC, abstractclassmethod, abstractmethod

__all__ = ['Account', 'Accounts']


class Account(ABC) :
    @abstractmethod
    def transaction(self, enum, value) -> str :
        '''Takes an enum corresponding to an instance method
        that handes that specific transaction logic for the value.
        Returns a confirmation code as a string. Should hand off
        responsibilty to whatever is responsible for handling transactions.
        In the current implementation, that is transactions.process_transaction().'''
        pass


class Accounts(ABC) :
    ACCOUNT_LIST:list[Account]

    @abstractclassmethod
    def add_account(cls, account) -> None :
        '''Adds an account to the ACCOUNT_LIST.'''
        pass