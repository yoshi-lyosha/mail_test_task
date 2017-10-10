# Ошибочное понимание задачи

Сделан скрипт, проверяющий входные данные на соответствиям правилам.

## Решение

Чтобы увидеть скрипт в работе, необходимо запустить parameters_generator_usage.py

## Описание

Так как я поторопился, то неправильно понял условие изложенной задачи и решил совершенно противоположную задачу.

Решённая задача проверяет словарь с входными данными, например:
```
{
        'login': 'yoshi',
        'domain': 'mail.ru',
        'password': 'Qwe_121_ewQ',
        'first_name': 'Alexey',
        'last_name': 'Atanov',
        'lang': 'ru_RU',
        'sex': 'male',
        'phone': '89060936571',
        'birthday': '04-10-1994'
    }
```

и выводит два словаря, один с обработанными входными данными 
(в случаях если подан None, заменяется на default_value и добавляется в errors если required)
и ошибками, выявленными после проверки на соответствие правилам, например:

```
{
    "params": {
        "login": "abc",
        "domain": "abc",
        "password": "abc",
        "first_name": "ab",
        "last_name": "ab",
        "lang": "abc",
        "sex": "abc",
        "phone": "abc",
        "birthday": "abc"
    },
    "errors": {
        "login": [
            "too short"
        ],
        "domain": [
            "not 'domain' custom type",
            "'abc' is not allowed value"
        ],
        "password": [
            "weak",
            "too short"
        ],
        "first_name": [
            "too short"
        ],
        "last_name": [
            "too short"
        ],
        "sex": [
            "'abc' is not allowed value"
        ],
        "phone": [
            "not 'phone' custom type"
        ],
        "birthday": [
            "not 'birthday' custom type"
        ]
    }
}
```

