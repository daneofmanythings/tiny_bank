from abc import ABC, abstractclassmethod, abstractmethod

class Account(ABC) :
    @abstractmethod
    def transaction(self, enum, value) -> str :
        '''Takes an enum corresponding to an instance method
        that handes that specific transaction logic for the value.
        Returns a confirmation code as a string.'''
        pass

class Accounts(ABC) :
    ACCOUNT_LIST:list[Account]

    @abstractclassmethod
    def add_account(cls, account) -> None :
        '''Adds an account to the ACCOUNT_LIST.'''
        pass