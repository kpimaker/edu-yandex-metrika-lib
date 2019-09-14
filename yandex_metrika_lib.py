# coding: utf-8

import yaml
import requests
import json
import time

from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

from error_handler import YMetrikaInvalidJson
from error_handler import YMetrikaResponseHandler
from error_handler import YMetrikaMaxRetriesExceed

API_HOST = 'https://api-metrika.yandex.net'
API_URL = '/stat/v1/data'


def make_token(token=None):
    """
    Возвращает токен для запросов к API Яндекс.Метрики из файла config.yaml в папке скрипта.
    Если токен передан как аргумент, то возвращается это же значение.

    config.yaml имеет вид:
    # токен для доступов статистики моего аккаунта в Я.Метрике
	metrika:
	  token: AgAA...
    """
    if not token:
        with open('config.yaml', encoding='utf-8') as f:
            config = yaml.load(f)
            
        token = config['metrika']['token']
    
    return token


def net_request(url, params, headers, max_retries=5, timeout=30):
    for i in range(1, max_retries+1):
        try:
            return requests.get(url, params=params, headers=headers, timeout=timeout)

        except ConnectionError as e:
            error = e
            print('Timeout, waiting and trying one more time')
            time.sleep(i**2)
    
    raise YMetrikaMaxRetriesExceed(error)


def response_is_correct(r):
    """Проверка валидности JSON от API Метрики"""
    try:
        json.loads(r.text)
        return True

    except ValueError:
        raise YMetrikaInvalidJson(r)


class MetrikaReports:
    def __init__(self, token=None):
        self.token = make_token(token)
    
    def _receive_metrika_report(self, **kwargs):
        """
        Возвращает данные запроса к API Яндекс.Метрики. Весь процесс запроса и обработки ответа API должен прописываться в этом методе.
        """
        url = API_HOST + API_URL

        r = net_request(url, params=kwargs, headers={'Authorization': 'OAuth {0}'.format(self.token)})

        if response_is_correct(r):
            if r.status_code == 200:
                return r.json()
            else:
                raise YMetrikaResponseHandler(r)

    def social_networks(self, date1, date2, id_):
    	"""Отчет по социальным сетям"""
    	dimensions = ['ym:s:<attribution>SocialNetwork']
    	metrics = ['ym:s:users', 'ym:s:visits' ,'ym:s:pageviews']

    	return self._receive_metrika_report(dimensions=dimensions, metrics=metrics, date1=date1, date2=date2, id=id_)

    def tech_monitoring(self, date1, date2, id_):
    	"""
    	Технический мониторинг для устройств и браузеров. Проверяем показатель отказов и долю роботов.
    	"""
    	dimensions = ['ym:s:deviceCategory', 'ym:s:browser']
    	metrics = ['ym:s:bounceRate', 'ym:s:robotPercentage']

    	return self._receive_metrika_report(dimensions=dimensions, metrics=metrics, date1=date1, date2=date2, id=id_)


if __name__ == '__main__':
    # mr = MetrikaReports(token=123)
    # print(mr.token)

    mr = MetrikaReports()
    # print(mr.token[:5])

    # print(mr._receive_metrika_report(preset='sources_summary', id='21075004'))
    print(mr.social_networks('2019-09-01', '2019-09-07', '21075004'))
    # print(mr.tech_monitoring('2019-09-01', '2019-09-07', '21075004'))
