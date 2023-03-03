from datetime import timezone, timedelta
from transactions import CustomerTransactions
from accounts.accounts import Account, Accounts
from constants import CustActions

__all__ = ['CustomerAccounts', 'CustomerAccount']

class CustomerAccounts :

    ACCOUNT_LIST = list()  # List of all accounts
    INTEREST = .05  # Interest rate

    @classmethod
    def add_account(cls, account) :
        cls.ACCOUNT_LIST.append(account)

    @classmethod
    def apply_interest(cls) :
        for account in cls.ACCOUNT_LIST :
            value = cls.INTEREST * account.balance
            account.transaction(CustActions.INTEREST, value)

    @classmethod
    def get_interest_rate(cls) :
        return cls.INTEREST
    
    @classmethod
    def set_interest_rate(cls, value) :
        if isinstance(value, float) and value >= 0 :
            cls.INTEREST = value
        else :
            raise ValueError('Interest must be a non-negative float')


class CustomerAccount :   
    
    def __init__(self, acc_num, first_name, last_name, balance=0, tz=(0, 'UTC')) :
        self._acc_num = acc_num
        self._balance = balance
        self.first_name = first_name
        self.last_name = last_name
        self.timezone = tz

        CustomerAccounts.add_account(self)

    @property
    def account_num(self) :
        return self._acc_num

    @property
    def balance(self) :
        return self._balance

    @property
    def first_name(self) :
        return self._first_name

    @first_name.setter
    def first_name(self, value) :
        if isinstance(value, str) and len(value.strip()) > 0:
            self._first_name = value
        else :
            raise ValueError('Must be non-empty of type \'str\'')
    
    @property
    def last_name(self) :
        return self._last_name

    @last_name.setter
    def last_name(self, value) :
        if isinstance(value, str) and len(value.strip()) > 0 :
            self._last_name = value
        else :
            raise ValueError('Must be non-empty of type \'str\'')
    
    @property
    def full_name(self) :
        return f'{self.last_name}, {self.first_name}'

    @property
    def timezone(self) :
        return self._timezone
    
    @timezone.setter
    def timezone(self, zoneinfo:tuple[int,str]) :
        delta, tzname = zoneinfo
        if -12 <= delta <= 14 :
            self._timezone =  timezone(timedelta(hours=delta), tzname)
        else :
            raise ValueError('Time offset needs to be between -12 and 14') 

    def _deposit(self, value) :
        if value > 0 :
            self._balance += value
            return CustActions.DEPOSIT.value
        else :
            return CustActions.DECLINED.value

    def _interest(self, value) :
        self._balance += value
        return CustActions.INTEREST.value
    
    def _withdraw(self, value) :
        if value > 0 and self.balance >= value:
            self._balance -= value
            return CustActions.WITHDRAW.value
        else :
            return CustActions.DECLINED.value
        
    def transaction(self, CustActions_enum, value) -> str:
        operations = {
            CustActions.DEPOSIT: self._deposit,
            CustActions.WITHDRAW: self._withdraw,
            CustActions.INTEREST: self._interest,
        }
        action = operations[CustActions_enum]
        return CustomerTransactions.process_transaction(self, action, value)
