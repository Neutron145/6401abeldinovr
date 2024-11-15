import stocks_analyzer
import time
import threading
import logging
from pandas import DataFrame
import yfinance as yf

class CancellationToken:
    '''
    Класс токена отмены выполнения задачи.
    '''

    def __init__(self):
        self.__is_canceled = False

    def is_canceled(self) -> bool:
        '''
        Метод проверки выполненной задачи.

        Возвращаемое значение:
            True - Если задача отменена
        '''

        return self.__is_canceled

    def cancel(self) -> None:
        '''
        Метод отмены выполнения задачи.
        '''

        self.__is_canceled = True


class ServiceThreads:
    '''
    Класс сервиса для выполнения анализа данных.
    '''

    def __init__(self, company: str, period: str):
        '''
        Конструктор сервиса.

        Входные параметры:
            company - название компании.
            period - период анализа акций
        '''

        self.__cancellation_token = None
        self.__analyzer = None
        self.__thread = None
        self.__company = company
        self.__period = period
        self.__logger = logging.getLogger(__name__)

    def start(self, columns: str | list, n: int, file_path = 'out.xlsx'):
        '''
        Метод запуска сервиса.

        Входные параметры: 
            columns - названия столбцов, которые необходимо проанализировать.
            file_path - путь к файлу записи результатов.
            file_path_log - путь к файлу записи логов.
        '''
        
        if self.__thread is not None:
            error = RuntimeError("Attempt to start running service")
            self.__logger.warning(error)
            raise error
        
        self.__cancellation_token = CancellationToken()
        self.__thread = threading.Thread(target=self.__run, 
                                         args=(columns, 
                                                n,
                                                file_path,  
                                                self.__cancellation_token))
        
        try:
            self.__thread.start()
            self.__logger.info("Service started")
        except:
            error = RuntimeError("Error of start service")
            self.__logger.error(error)
            raise error

    def stop(self):
        '''
        Метод остановки сервиса
        '''

        if self.__thread is None:
            error = RuntimeError("Attempt to stop service before start")
            self.__logger.warning(error)
            raise error

        self.__cancellation_token.cancel()
        
        self.__thread.join()
        self.__thread = None
        
        self.__logger.info("Service stopped")

    def __run(self, 
                columns: str | list,
                n: int, 
                file_path = 'out.xlsx', 
                cancellation_token: CancellationToken = CancellationToken()):

        ticker = yf.Ticker(self.__company)
        historical_data = ticker.history(period=self.__period, interval='1m')
        historical_data.index = historical_data.index.tz_localize(None)

        self.__analyzer = stocks_analyzer.Analyzer(historical_data)

        while(not cancellation_token.is_canceled()):
            self.__analyzer.SMA(columns, n)
            self.__analyzer.diff(columns, n)
            self.__analyzer.extreme_points(columns, n)
            self.__analyzer.ACF(columns, n)

            self.__analyzer.save_data_frame(file_path)
            
            self.__logger.info(f"Succefull calculation of data. Saved to the file {file_path}")
            
            time.sleep(60)