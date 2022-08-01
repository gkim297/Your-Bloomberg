import argparse, traceback
from decimal import Decimal
from API_Request import *

def enterpriseValueCalculator(incomeStatement, cashflowStatement, balanceSheet, period, discountRate,
                              earningsGrowthRate, capExGrowthRate, perpetualGrowthRate):
    """
    enterpriseValueCalculator -
    :param incomeStatement:
    :param cashflowStatement:
    :param balanceSheet:
    :param period:
    :param discountRate:
    :param earningsGrowthRate:
    :param capExGrowthRate:
    :param perpetualGrowthRate:
    :return:
    """
    if incomeStatement[0]['EBIT']:
        ebit = float(incomeStatement[0]['EBIT'])
    else:
        ebit = float(input(f'EBIT is missing, please enter EBIT on {incomeStatement[0]["date"]} or skip: '))

    taxRate = float(incomeStatement[0]['Income Tax Expense']) / float(incomeStatement[0]['Earnings before Tax'])
    nonCashCharges = float(cashflowStatement[0]['Depreciation & Amortization'])
    currentWorkingCapital = (float(balanceSheet[0]['Total assets']) - float(balanceSheet[0]['Total non-current assets'])) - \
          (float(balanceSheet[1]['Total assets']) - float(balanceSheet[1]['Total non-current assets']))
    capEx = float(cashflowStatement[0]['Capital Expenditure'])
    discount = discountRate

    flows = []
    #we're using manual printing instead of pandas dataframe because it's an expensive process.
    print()

#TODO: finish https://github.com/halessi/DCF/blob/master/modeling/dcf.py
#TODO: https://site.financialmodelingprep.com/developer/docs/#Financial-Statements-List chart API.
#TODO: https://www.alphaspread.com/security/nasdaq/msft/dcf-valuation/base-case benchmark model



def DCF(ticker, enterpriseValueStatement, incomeStatement, balanceSheet, cashFlowStatement, discountRate, \
    forecast, earningGrowthRate, capitalExpenditureGrowthRate, perpetualGrowthRate):
    """
    DCF -
    :param ticker:
    :param enterpriseValueStatement:
    :param incomeStatement:
    :param balanceSheet:
    :param cashFlowStatement:
    :param discountRate:
    :param forecast:
    :param earningGrowthRate:
    :param capitalExpenditureGrowthRate:
    :param perpetualGrowthRate:
    :return:
    """