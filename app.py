import streamlit as st
import requests
import config, json
from helpers import formatNumber
from datetime import datetime, timedelta
from FMP import FMP
import certifi
import json
from urllib.request import urlopen
import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

#
symbol = st.sidebar.text_input('Symbol', value='MSFT')
symbol = symbol.upper()
stock = FMP(config.FMP_TOKEN, symbol)
screen = st.sidebar.selectbox('View', ('Summary', 'Ticker', 'DCF Valuation', 'Relative Valuations', 'Profitability', 'Solvency'), index=1)

#
def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

#
st.title(screen)

#--------------------------------------Section 1: Summary-----------------------------------------#
if screen == 'Summary':

    print('Getting DCF valuation from FMP api.')
    DCF = stock.get_DCF()
    DCF = get_jsonparsed_data(DCF)
    discountedCashFlow = DCF['dcf']
    discountedCashFlow = round(discountedCashFlow, 2)

    print('Getting company information from FMP api.')
    companyProfile = stock.get_company_profile()
    companyProfile = get_jsonparsed_data(companyProfile)
    companyProfile = companyProfile[0]

    companyName = companyProfile['companyName']
    stockSymbol = companyProfile['symbol']
    price = companyProfile['price']
    price = round(price, 2)
    exchange = companyProfile['exchangeShortName']
    industry = companyProfile['industry']
    description = companyProfile['description']
    sector = companyProfile['sector']
    currency = companyProfile['currency']
    image = companyProfile['image']

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image(image)

    with col2:
        st.subheader(f'{companyName} ({exchange}: {stockSymbol})')
        st.subheader(f'{price} {currency}')
        st.write(f'Industry: {industry}')
        st.write(f'Sector: {sector}')
        #st.write(description)

    st.subheader('Intrinsic Value')
    #comparison: 2 bard (intrinsic value vs price)

    #put relative valuations into consideration, make average and compare it to the price!!!!!!
    if discountedCashFlow > price:
        valuation = 'undervalued'

    elif price > discountedCashFlow:
        valuation = 'overvalued'

    percentage = ((discountedCashFlow - price)/price) * 100
    percentage = abs(percentage)
    percentage = round(percentage, 2)

    #change text color by overvalued vs undervalued.
    st.write(f'The intrinsic value of one {stockSymbol} stock under our scenario is {discountedCashFlow} {currency}.')
    st.write(f'Compared to the current marker price of {price} {currency}, {companyName} is {valuation} by {percentage}%')

#--------------------------------Section 2: Ticker-----------------------------------------------
if screen == 'Ticker':
    snp500 = pd.read_csv("SP500.csv")
    symbols = snp500['Symbol'].sort_values().tolist()

    ticker = st.sidebar.selectbox(
        'Choose a S&P 500 Stock',
        symbols)

    i = st.sidebar.selectbox(
        "Interval in minutes",
        ("1m", "5m", "15m", "30m")
    )

    p = st.sidebar.number_input("How many days (1-30)", min_value=1, max_value=30, step=1)

    stock = yf.Ticker(ticker)
    history_data = stock.history(interval=i, period=str(p) + "d")

    prices = history_data['Close']
    volumes = history_data['Volume']

    lower = prices.min()
    upper = prices.max()

    prices_ax = np.linspace(lower, upper, num=20)

    vol_ax = np.zeros(20)

    for i in range(0, len(volumes)):
        if (prices[i] >= prices_ax[0] and prices[i] < prices_ax[1]):
            vol_ax[0] += volumes[i]

        elif (prices[i] >= prices_ax[1] and prices[i] < prices_ax[2]):
            vol_ax[1] += volumes[i]

        elif (prices[i] >= prices_ax[2] and prices[i] < prices_ax[3]):
            vol_ax[2] += volumes[i]

        elif (prices[i] >= prices_ax[3] and prices[i] < prices_ax[4]):
            vol_ax[3] += volumes[i]

        elif (prices[i] >= prices_ax[4] and prices[i] < prices_ax[5]):
            vol_ax[4] += volumes[i]

        elif (prices[i] >= prices_ax[5] and prices[i] < prices_ax[6]):
            vol_ax[5] += volumes[i]

        elif (prices[i] >= prices_ax[6] and prices[i] < prices_ax[7]):
            vol_ax[6] += volumes[i]

        elif (prices[i] >= prices_ax[7] and prices[i] < prices_ax[8]):
            vol_ax[7] += volumes[i]

        elif (prices[i] >= prices_ax[8] and prices[i] < prices_ax[9]):
            vol_ax[8] += volumes[i]

        elif (prices[i] >= prices_ax[9] and prices[i] < prices_ax[10]):
            vol_ax[9] += volumes[i]

        elif (prices[i] >= prices_ax[10] and prices[i] < prices_ax[11]):
            vol_ax[10] += volumes[i]

        elif (prices[i] >= prices_ax[11] and prices[i] < prices_ax[12]):
            vol_ax[11] += volumes[i]

        elif (prices[i] >= prices_ax[12] and prices[i] < prices_ax[13]):
            vol_ax[12] += volumes[i]

        elif (prices[i] >= prices_ax[13] and prices[i] < prices_ax[14]):
            vol_ax[13] += volumes[i]

        elif (prices[i] >= prices_ax[14] and prices[i] < prices_ax[15]):
            vol_ax[14] += volumes[i]

        elif (prices[i] >= prices_ax[15] and prices[i] < prices_ax[16]):
            vol_ax[15] += volumes[i]

        elif (prices[i] >= prices_ax[16] and prices[i] < prices_ax[17]):
            vol_ax[16] += volumes[i]

        elif (prices[i] >= prices_ax[17] and prices[i] < prices_ax[18]):
            vol_ax[17] += volumes[i]

        elif (prices[i] >= prices_ax[18] and prices[i] < prices_ax[19]):
            vol_ax[18] += volumes[i]

        else:
            vol_ax[19] += volumes[i]

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.2, 0.8],
        specs=[[{}, {}]],
        horizontal_spacing=0.01

    )

    fig.add_trace(
        go.Bar(
            x=vol_ax,
            y=prices_ax,
            text=np.around(prices_ax, 2),
            textposition='auto',
            orientation='h'
        ),

        row=1, col=1
    )

    dateStr = history_data.index.strftime("%d-%m-%Y %H:%M:%S")

    fig.add_trace(
        go.Candlestick(x=dateStr,
                       open=history_data['Open'],
                       high=history_data['High'],
                       low=history_data['Low'],
                       close=history_data['Close'],
                       yaxis="y2"
                       ),
        row=1, col=2
    )

    fig.update_layout(
        title_text='Market Profile Chart (US S&P 500)',  # title of plot
        bargap=0.01,  # gap between bars of adjacent location coordinates,
        showlegend=False,
        xaxis=dict(
            showticklabels=False
        ),
        yaxis=dict(
            showticklabels=False
        ),
        yaxis2=dict(
            title="Price (USD)",
            side="right"
        )
    )

    fig.update_yaxes(nticks=20)
    fig.update_yaxes(side="right")
    fig.update_layout(height=800)

    config = {
        'modeBarButtonsToAdd': ['drawline']
    }

    st.plotly_chart(fig, use_container_width=True, config=config)



#--------------------------------Section 3: DCF Valuation-----------------------------------------
if screen == 'DCF Valuation':

    #basic numbers straight out from FMP API.
    print('Getting DCF valuation from FMP api.')
    DCF = stock.get_DCF()
    DCF = get_jsonparsed_data(DCF)
    discountedCashFlow = DCF['dcf']
    stockPrice = DCF['Stock Price']

    st.subheader('DCF Value')
    st.write(discountedCashFlow)
    st.subheader('Stock Price')
    st.write(stockPrice)

#-------------------------------Section 3: Relative Valuation-----------------------------------------
if screen == 'Relative Valuations':

    #basic numbers straight out from FMP api.
    print('Getting fundamental ratios from FMP api.')
    financialFundamentals = stock.get_fundamental_ratios()
    financialFundamentals = get_jsonparsed_data(financialFundamentals)
    #P/S, P/E, P/OCF, P/FCFE, P/B
    mostRecent = financialFundamentals[0]

    PS = mostRecent['priceToSalesRatio']
    PS = round(PS, 1)
    PE = mostRecent['priceEarningsRatio']
    PE = round(PE, 1)
    POCF = mostRecent['priceToOperatingCashFlowsRatio']
    POCF = round(POCF, 1)
    PFCFE = mostRecent['priceToFreeCashFlowsRatio']
    PFCFE = round(PFCFE, 1)
    PB = mostRecent['priceBookValueRatio']
    PB = round(PB, 1)

    st.header('Valuation Multiples')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f'{PS}')
        st.write('P/S')
        st.subheader(f'{POCF}')
        st.write('P/OCF')
        st.subheader(f'{PB}')
        st.write('P/B')

    with col2:
        st.subheader(f'{PE}')
        st.write('P/E')
        st.subheader(f'{PFCFE}')
        st.write('P/FCFE')

if screen == 'Profitability':
    pass

if screen == 'Solvency':
    pass