from enum import Enum

class CustActions(Enum) :
    DEPOSIT = 'D'
    WITHDRAW = 'W'
    INTEREST = 'I'
    DECLINED = 'X'