# coding: utf-8


class YMetrikaMaxRetriesExceed(Exception):
	"""Слишком много попыток получения отчета"""
	def __init__(self, connection_error):
		print('Too many retries. Error from last retry:')
		print(connection_error)


class YMetrikaInvalidJson(Exception):
	"""Проверка корректности ответа API"""
	def __init__(self, response):
		print('Got invalid response from API:')
		print(self.response.text)


class YMetrikaResponseHandler(Exception):
	"""
	Описание ошибок на стороне API.
	Документация https://yandex.ru/dev/webmaster/doc/dg/reference/errors-docpage
	"""
	def __init__(self, response):
		print('Not good')

		if response.status_code == 400:
			print('Error in response. Check your metrics and dimension at first')
			print(response.json())

		if response.status_code == 403:
			print('Seems that counter number is wrong')
