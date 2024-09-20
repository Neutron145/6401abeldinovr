import sys
import numpy as np

# Словарь, который хранит значения параметров в формате Ключ : значение
args = {}

# Названия параметров для использования в словаре
params=['n0', 'h', 'nk', 'a', 'b', 'c']


def parser() -> None:
	'''Парсер для чтения параметров вычисления функции из файла config.txt'''

	f = open('config.txt', 'r')
	
	for line, i in zip(f, range(6)):
		args[params[i]] = float(line.split()[2])


def calculate(n0 : float, h : float, nk : float, a : float, b : float, c : float) -> np.array:
	'''Функция вычисления f(x), согласно варианту'''
	
	# Вычисление количества точек на сетке
	n = int((nk -n0)/(h))

	# Создание сетки согласно полученным параметрам
	x = np.linspace(n0, nk, n)
	
	# Вычисление значений функции во всех точках x
	y = a * ((2 * x + np.pow(np.sin(b * x + c), 2)) / (3 + x))
	
	return y

def safe_result(arr):
	f = open('result.txt', 'w')

	for data in arr:
		f.write(str(data) + '\n')

if __name__ == "__main__":
	# Если аргументы не переданы при запуске .py из консоли, парсим config.txt для извлечения параметров
	# Иначе используем аргументы, переданные при запуске .py 
	if len(sys.argv) == 1:
		parser()
	elif len(sys.argv) == 7:
		for i in range(6):
			args[params[i]] = sys.argv[i+1]
	else:
		print("Error")
		exit()
	
	# После получения аргументов вычисляем значение функции y
	y = calculate(args['n0'], args['h'], args['nk'], args['a'], args['b'], args['c'])
	
	# Сохраняем значения функции y в файл result.txt
	safe_result(y)