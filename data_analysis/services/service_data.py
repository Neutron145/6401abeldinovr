import yfinance as yf
from pandas import DataFrame
from datetime import datetime, timedelta
import logging


__logger = logging.getLogger(__name__)

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

        try:
                ticker = yf.Ticker(company)
                historical_data = ticker.history(start=start, end=end, interval=interval)
                
        except: 
                error = RuntimeError(f"Не удалось получить данные компании {company}.")
                __logger.error(error)
                raise error

        __logger.info(f"Успешное получение данных {company}")
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
        
        try: 
                ticker = yf.Ticker(company)
                historical_data = ticker.history(start=datetime.now() - period, end=datetime.now(), interval=interval)
        except: 
                error = RuntimeError(f"Не удалось получить данные компании {company}.")
                __logger.error(error)
                raise error

        __logger.info(f"Успешное получение данных {company}")
        historical_data.index = historical_data.index.tz_localize(None)
        return historical_data