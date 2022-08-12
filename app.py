import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pickle
import matplotlib.pyplot as plt
import streamlit as st
import plotly
import plotly.express as px
import time
import datetime
from datetime import datetime

def dateToQTR(x):
    """
    dateToQTR - converts date to quarter.
    :param x: date given
    :return: quarter
    """
    QTR=(x.month-1)//3+1
    QTR="Q"+str(QTR)
    return QTR

def dateToYear(x):
    """
    dateToYear - converts date to year.
    :param x: date given
    :return: year
    """
    return x.year

@st.cache
def DCF(earnings, discount_rate, growth_rate1, growth_years ,growth_rate2, total_years):
    """
    DCF -
    :param earnings:
    :param discount_rate:
    :param growth_rate1:
    :param growth_years:
    :param growth_rate2:
    :param total_years:
    :return:
    """
    value = 0
    last_Earnings = earnings
    
    if growth_years == 0:
        if discount_rate <= growth_rate1:
            value = np.inf
        else:
            value = earnings / discount_rate-growth_rate1
            
    else:
        value = earnings
        for i in range(1, growth_years + 1):
            last_Earnings = last_Earnings * (1 + growth_rate1)
            value = value + last_Earnings / (1 + discount_rate) ** i
            
        if total_years == 0 or total_years <= growth_years:
            TV = last_Earnings * (1 + growth_rate1) / (discount_rate - growth_rate2)
            value = value + TV / (1 + discount_rate) ** (growth_years + 1)
            
        else:
            for i in range(growth_years + 1, total_years + 1):
                last_Earnings = last_Earnings * (1 + growth_rate2)
                value = value + last_Earnings / (1 + discount_rate) ** i
    return value

st.set_page_config(layout="wide")

companyDF = pd.read_csv(r'sample_data.csv')
company_list = companyDF.drop_duplicates(subset='Ticker')

company_list = company_list['Ticker'].values

cols = st.columns(2)
company_ticker = cols[0].selectbox('Ticker:',company_list)
financialDF = companyDF[companyDF['Ticker'] == company_ticker]

DCF_columns=["Ticker", "Year", "QTR", "Report Date", "Shares (Diluted)", "Revenue", "Pretax Income (Loss)", 'Net Income (Common)', 'Stock Price', 'Stock pct Increase',
                         'Op. Invested Capital', 'Fin. Invested Capital', 'Invested Capital', 'Owner Earnings', 'Free Cash Flow',
                         'Net Worth', 'Market Cap', 'PE', 'PB', 'PB (Tangible)', 'Faustmann Ratio', 'ROIC', 'Profit Margin',
                         'ROA', 'ROE']

financialDF = financialDF[DCF_columns]
annualDF = pd.DataFrame()
latest_columns = ["Ticker", "Year", "Report Date", "Shares (Diluted)", 'Stock Price', 'Net Worth', 'Market Cap']
add_columns = ["Revenue", "Pretax Income (Loss)", 'Net Income (Common)', 'Owner Earnings', 'Free Cash Flow']
average_columns = ['PE', 'PB', 'PB (Tangible)', 'Faustmann Ratio', 'ROIC', 'Profit Margin',
                         'ROA', 'ROE']

if len(financialDF) > 4:
    temp = financialDF.drop_duplicates(subset='Year')
    year_list = temp['Year']
    
    for year in year_list:
        temp = financialDF[financialDF['Year']==year]
        latestDF = temp[latest_columns]
        latestDF = latestDF.iloc[-1:]
        latestDF = latestDF.reset_index(drop=True)
        addDF = temp[add_columns]
        addDF = pd.DataFrame(addDF.sum(axis = 0) * 4 / len(temp))
        addDF = addDF.T
        averageDF = temp[average_columns]
        averageDF = pd.DataFrame(averageDF.sum(axis = 0) / len(temp))
        averageDF = averageDF.T

        if(annualDF.empty):
            annualDF = pd.concat([latestDF, addDF, averageDF], axis = 1)
        else:
            annualDF = annualDF.append(pd.concat([latestDF, addDF, averageDF], axis=1), ignore_index = True)
            
EPS = annualDF["Owner Earnings"].values / annualDF["Shares (Diluted)"].values
EPS_change = (EPS - np.roll(EPS, 1)) / np.roll(EPS, 1) * 100
EPS_change[0] = 0
EPSDF = pd.DataFrame(annualDF["Year"])
EPSDF["EPS"] = pd.DataFrame(EPS)
EPSDF["EPS %"] = pd.DataFrame(EPS_change)
EPSDF['Sales per Share'] = pd.DataFrame(annualDF['Revenue'].values / annualDF["Shares (Diluted)"].values)
annualDF["EPS"] = EPSDF["EPS"]
annualDF["EPS %"] = EPSDF["EPS %"]
annualDF['Sales per Share'] = EPSDF['Sales per Share']
displayDF = EPSDF.sort_values(by = ['Year'], ascending = False)

cols[0].dataframe(data = displayDF, height = 175)
LatestDF = EPSDF.iloc[-1:]

Earnings = cols[0].text_input("Year 1 Earnings", 0)
Drate = cols[0].text_input("Disconut Rate", value=0.07)
Growth1 = cols[0].text_input("Early Growth Rate", value=0.03)
GrowthYears = cols[0].text_input("Years of Growth (0 assumes perpetual Early Growth Rate)", value=0)
Growth2 = cols[0].text_input("Terminal Growth Rate", value=0.03)
TotalYears =  cols[0].text_input("Years of Growth (0 assumes Terminal Value from Terminal Growth Rate)", value=0)

headings = annualDF.columns
item1 = cols[1].selectbox('Plot1:', headings, index=21)
item2 = cols[1].selectbox('Plot2:', headings, index=1)

plot2DF = pd.DataFrame(annualDF[item1])
plot2DF['Year'] = annualDF['Year'].values

if item2 !='Year':
    plot_series = [item1, item2]
    plot2DF[item2] = annualDF[item2]
else:
    plot_series = [item1]
fig2 = px.line(plot2DF, x = "Year", y = plot_series)
cols[1].plotly_chart(fig2, use_container_width = True)

valuation = DCF(float(Earnings), float(Drate), float(Growth1), int(GrowthYears), float(Growth2), int(TotalYears))
current_price = yf.Ticker(company_ticker).history(period='1d')
current_price = current_price["Close"].values
current_price = current_price[0]
current_price_format = "{:.2f}".format(current_price)
valuation_format = "{:.2f}".format(valuation)
cols[1].subheader("Valuation: "+str(valuation_format)+ "\tCurrent Price: " +str(current_price_format))

MS_format = (valuation / current_price - 1) * 100
MS_format = "{:.2f}".format(MS_format)
cols[1].subheader("Margin of Safety: " +str(MS_format) +"%")

if len(EPSDF) > 3:
    eps = EPSDF['EPS'].values
    eps3Growth = ((eps[len(eps) - 1] / eps[len(eps) - 4]) ** (1 / 3) - 1)
else:
    eps3Growth = 0
    
if len(EPSDF) > 5:
    eps = EPSDF['EPS'].values
    eps5Growth = ((eps[len(eps) - 1] / eps[len(eps) - 6]) ** (1 / 5) - 1)
else:
    eps5Growth = 0

LatestDF = annualDF.iloc[-1:]
LatestDF["EPS 3Y Growth"] = eps3Growth
LatestDF["EPS 5Y Growth"] = eps5Growth
LatestDF = LatestDF[["EPS 3Y Growth", "EPS 5Y Growth", 'Faustmann Ratio', 'ROIC', 'ROE', 'PE', "PB"]]
LatestDF = LatestDF.style.format({"EPS 3Y Growth":'{:.2%}'})
LatestDF = LatestDF.format({"EPS 5Y Growth":'{:.2%}'})
LatestDF = LatestDF.format({"Faustmann Ratio":'{:.2f}'})
LatestDF = LatestDF.format({"ROIC":'{:.2%}'})
LatestDF = LatestDF.format({"ROE":'{:.2%}'})
LatestDF = LatestDF.format({"PE":'{:.2f}'})
LatestDF = LatestDF.format({"PB":'{:.2f}'})
cols[1].dataframe(data=LatestDF, height=100)
