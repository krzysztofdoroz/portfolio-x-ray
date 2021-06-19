import yfinance as yf
import pandas as pd
from typing import List, DefaultDict, Tuple
import csv


Stock = Tuple[str, int]
Etf = Tuple[str, int, str]


def gbp_to_usd() -> float:
    return yf.Ticker("GBPUSD=X").info['regularMarketPrice']


def eur_to_usd() -> float:
    return yf.Ticker("EURUSD=X").info['regularMarketPrice']


GBP_to_USD = gbp_to_usd()
EUR_to_USD = eur_to_usd()


def load_etfs_from_file(path: str) -> List[Etf]:
    with open(path, newline='') as csvfile:
        result = []
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for ticker, amount, ccy in reader:
            result.append((ticker, int(amount), ccy))
        return result


def load_stocks_from_file(path: str) -> List[Stock]:
    with open(path, newline='') as csvfile:
        result = []
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for ticker, amount in reader:
            result.append((ticker, int(amount)))
        return result


def process_stocks(stocks: List[Stock]) -> pd.DataFrame:
    result = []
    for ticker, amount in stocks:
        print(ticker)
        result.append(process_stock_info(get_stock_info(ticker), amount))

    return pd.DataFrame(result)


def process_etfs(etfs: List[Etf]) -> pd.DataFrame:
    result = []
    for ticker, amount, ccy in etfs:
        print(ticker)
        result.append(process_eur_etf(ticker, get_stock_price(ticker), amount, ccy))

    return pd.DataFrame(result)


def get_stock_info(ticker: str) -> DefaultDict:
    return yf.Ticker(ticker).info


def get_stock_price(ticker: str) -> float:
    return yf.Ticker(ticker).history(period="1d").iloc[0, 3]


def process_stock_info(info: dict, amount: int) -> DefaultDict:
    total_val = amount * info['regularMarketPrice']
    ccy = info['currency']
    if ccy == 'GBp':
        total_val = (total_val * GBP_to_USD) / 100

    return {"ticker": info['symbol'],
            "price": info['regularMarketPrice'],
            "amount": amount,
            "BV": info['bookValue'],
            "P/B": info['priceToBook'],
            "total_val": total_val,
            "dividend_rate": info['dividendRate'],
            "yield": info['dividendYield'],
            "industry": info.get('industry', ""),
            "currency": ccy}


def process_eur_etf(ticker: str, price: float, amount: int, ccy: str) -> DefaultDict:
    total_val = amount * price

    if ccy == 'GBp':
        total_val = (total_val * GBP_to_USD) / 100
    if ccy == 'EUR':
        total_val = total_val * EUR_to_USD
    if ccy == 'GBP':
        total_val = (total_val * GBP_to_USD)

    return {"ticker": ticker,
            "price": price,
            "amount": amount,
            "total_val": total_val,
            "currency": ccy}

