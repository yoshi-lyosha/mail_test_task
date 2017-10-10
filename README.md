# Задача 

Генератор неправильных параметров

## Решение

Для того, чтобы увидеть скрипт в работе, необходимо запустить parameters_generator_usage.py

На данный момент скрипт выводит список с пятью словарями, в которых значения сгенерированны по какому-то общему правилу

Сперва идёт анализ на пустые значения, затем на соответствия типам, затем на максимальную/минимальную длину, и, наконец,
на допустимые значения. Если для параметра не задано одно из правил - подставляется дефолтное значение

## Описание

есть таблица значений (параметр - правила):
```
{
    'login': [
        'string',
        'required',
        {'minlength': 4},
        {'maxlength': 32},
        {'default_value': 'not_exists_login'}
    ],
    'domain': [
        'domain',
        'required',
        {'allowed_values': ['mail.ru', 'list.ru', 'inbox.ru']},
        {'default_value': 'mail.ru'}
    ],
    'password': [
        'password',
        'required',
        {'minlength': 5},
        {'default_value': 'AS_(78hf>32+/zX'}
    ],
    'first_name': [
        'string',
        {'minlength': 3},
        {'maxlength': 64},
        'required',
        {'default_value': 'fname'}
    ],
    'last_name': [
        'string',
        {'minlength': 3},
        {'maxlength': 64},
        'required',
        {'default_value': 'lname'}
    ],
    'lang': [
        'string', 
        'optional',
        {'default_value': 'ru_RU'}
    ],
    'sex': [
        'string',
        'optional',
        {'allowed_values': ['male', 'female']},
        {'default_value': 'male'}
    ],
    'phone': [
        'phone',
        'required',
        {'default_value': '89124567890'}
    ],
    'birthday': [
        'birthday',
        'optional',
        {'default_value': '12-10-1991'}
    ]
} 
```
правила включают 
- ограничения на длину(minlength, maxlength)
- ограничения на тип (при этом есть и нестандартные типы - domain, email, для которых по факту нужно регулярное выражение)
- ограничения на значения (allowed_values)
- обязательный параметр или нет (значит если его не передавать, то ошибки не будет)
- дефолтное значение

функция должна генерировать наборы значений параметров, которые бы НЕ удовлетворяли правилам, а также ожидаемые ошибки

пример самых обычных вариантов для поля 'phone' - phone=None ; phone='+8' ; phone='phone' ; phone=89124567890 и тд

на выходе функции должна быть комбинация всех параметров и ожидаемые ошибки в виде
```
[
	{
		'params':
			{'phone': None, 'password': 'abc', ....},
	 	'errors':
	 		{'phone': 'required', 'password': 'weak', ....}
	},
	{
		'params':
			{'phone': None, 'password': None, ....},
	 	'errors':
	 		{'phone': 'required', 'password': 'required', ....},
	},
	.....
]
```
