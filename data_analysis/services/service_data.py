import yfinance as yf
from pandas import DataFrame
from datetime import datetime, timedelta


def get_data(company : str, start : str | datetime, end : str | datetime, interval : str) -> DataFrame:
        """
        Функция получения данных за указанный период

        Входные параметры:
                company - название компании, для которой анализируются акции
                start - начало указанного периода
                end - конец указанного периода
                interval - интервал между полученными данными
        
        Выходные параметры:
                historical_data - таблица с акциями компании 
        """
        ticker = yf.Ticker(company)
        historical_data = ticker.history(start=start, end=end, interval=interval)
        historical_data.index = historical_data.index.tz_localize(None)
        return historical_data

def get_last_data(company : str, period : timedelta, interval : str) -> DataFrame:
        """
        Функция получения данных за последний момент времени

        Входные параметры:
                company - название компании, для которой анализируются акции
                period - период анализируемых данных, начиная с текущего момента
                interval - интервал между полученными данными

        Выходные параметры:
                historical_data - таблица с акциями компании 
        """
        ticker = yf.Ticker(company)
        historical_data = ticker.history(start=datetime.now() - period, end=datetime.now(), interval=interval)
        historical_data.index = historical_data.index.tz_localize(None)
        return historical_data