checking_rules_list = {
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
        # {'default_value': 'male'}
    ],
    'phone': [
        'phone',
        'required',
        # {'default_value': '89124567890'}
    ],
    'birthday': [
        'birthday',
        'optional',
        {'default_value': '12-10-1991'}
    ]
}

test_parameters_dicts_list = [
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
    },
    {
        'login': 100,
        'domain': 100,
        'password': 100,
        'first_name': 100,
        'last_name': 100,
        'lang': 100,
        'sex': 100,
        'phone': 100,
        'birthday': 100
    },
    {
        'login': None,
        'domain': None,
        'password': None,
        'first_name': None,
        'last_name': None,
        'lang': None,
        'sex': None,
        'phone': None,
        'birthday': None
    },
    {
        'login': 'abc',
        'domain': 'abc',
        'password': 'abc',
        'first_name': 'ab',
        'last_name': 'ab',
        'lang': 'abc',
        'sex': 'abc',
        'phone': 'abc',
        'birthday': 'abc'
    }
]
