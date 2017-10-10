generator_rules = {
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
