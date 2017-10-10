import re
import string
import random

_wrong_parameters_creators = []
_wrong_type_parameter_creators = {}


def wrong_parameters_creator(parameters_table):
    """ Generates invalid parameters """
    output_list = list()
    parsed_parameters_table = _parse_parameters_table(parameters_table)
    [creator(parsed_parameters_table, output_list) for creator in _wrong_parameters_creators]
    return output_list


def _parse_parameters_table(parameters_table):
    """ Parsing the table of values for convenience of further use """
    parsed_parameters_table = dict()
    for parameter_name, rules_list in parameters_table.items():
        rules_dict = _parse_rules_list(rules_list)
        parsed_parameters_table[parameter_name] = rules_dict
    return parsed_parameters_table


def _parse_rules_list(rules_list):
    """ Parsing the rules list """
    rules_dict = dict()
    rules_dict['minlength'] = _find_dict_value_in_rules_list(rules_list, 'minlength', int)
    rules_dict['maxlength'] = _find_dict_value_in_rules_list(rules_list, 'maxlength', int)
    rules_dict['allowed_values'] = _find_dict_value_in_rules_list(rules_list, 'allowed_values', list)
    rules_dict['default_value'] = _find_dict_value_in_rules_list(rules_list, 'default_value', str)
    rules_dict['necessity'] = list(filter(lambda var: var == 'required' or var == 'optional', rules_list))[0]
    rules_dict['parameter_type'] = rules_list[0]
    return rules_dict


def _find_dict_value_in_rules_list(rules_list, rule_str, value_type):
    """ Function to find a specific dictionary in the list """
    rule_value_generator = (rule[rule_str] for rule in rules_list if rule_str in rule)
    try:
        rule_value = value_type(*rule_value_generator)
    except TypeError as e:
        # adding information to an exception
        raise TypeError("{}; '{}' doesn't fit to '{}'".format(str(e), value_type, rule_str))
    return rule_value if rule_value else None


def _random_string_gen(size=None, chars=string.ascii_letters + string.digits, additional_chars_str=''):
    """ Random string generator of length 'size' from the character string """
    if not size:
        size = random.randrange(1, 20)
    chars = chars + additional_chars_str
    return ''.join(random.choices(chars, k=size))


def _wrong_parameters_creator_for_rule(func):
    """
    A decorator is used for identifying functions, which generates dict with wrong parameters
    and dict with errors.
    This is used for easy extensibility.
    """
    _wrong_parameters_creators.append(func)
    return func


def _create_output_parameters_dict():
    """ Creating dictionaries embedded in the dictionary to reuse the code """
    output_dict = dict()
    output_dict['params'] = {}
    output_dict['errors'] = {}
    return output_dict


@_wrong_parameters_creator_for_rule
def _wrong_necessity_parameter_creator(parsed_parameters_table, output_list):
    """
    A function that checks necessity of parameter, and if it is required, adds error to an error dict.
    If it is optional or required parameter, assigns a None value.
    """
    output_dict = _create_output_parameters_dict()
    for parameter_name, rules_dict in parsed_parameters_table.items():
        if rules_dict['necessity'] == 'required':
            output_dict['errors'][parameter_name] = 'required'
        output_dict['params'][parameter_name] = None
    output_list.append(output_dict)


@_wrong_parameters_creator_for_rule
def _wrong_type_parameter_creator(parsed_parameters_table, output_list):
    """
    A function that creates an invalid parameters for specific custom types.

    Subfunctions for each type are stored in the registration dictionary,
    in which they are added by a special decorator

    Subfunctions return 'True' if a custom type error is used
    """
    output_dict = _create_output_parameters_dict()
    for parameter_name, rules_dict in parsed_parameters_table.items():
        if rules_dict['parameter_type'] in _wrong_type_parameter_creators:
            custom_error = _wrong_type_parameter_creators[rules_dict['parameter_type']](parameter_name, output_dict)
            if not custom_error:
                output_dict['errors'][parameter_name] = "not '{}' custom type".format(rules_dict['parameter_type'])
        else:
            output_dict['params'][parameter_name] = rules_dict['default_value']
    output_list.append(output_dict)


@_wrong_parameters_creator_for_rule
def _wrong_length_parameter_creator(parsed_parameters_table, output_list):
    """ A function that generates values greater than the maximum value and less than the minimum value """
    output_minlength_dict = _create_output_parameters_dict()
    output_maxlength_dict = _create_output_parameters_dict()
    for parameter_name, rules_dict in parsed_parameters_table.items():
        if rules_dict['minlength']:
            wrong_parameter = _random_string_gen(random.randrange(1, rules_dict['minlength']))
            output_minlength_dict['params'][parameter_name] = wrong_parameter
            output_minlength_dict['errors'][parameter_name] = 'too short, minlength = ' + str(rules_dict['minlength'])
        else:
            output_minlength_dict['params'][parameter_name] = rules_dict['default_value']
        if rules_dict['maxlength']:
            wrong_parameter = _random_string_gen(rules_dict['maxlength'] + random.randrange(1, 100))
            output_maxlength_dict['params'][parameter_name] = wrong_parameter
            output_maxlength_dict['errors'][parameter_name] = 'too long, maxlength = ' + str(rules_dict['maxlength'])
        else:
            output_maxlength_dict['params'][parameter_name] = rules_dict['default_value']
    output_list += output_minlength_dict, output_maxlength_dict


@_wrong_parameters_creator_for_rule
def _wrong_not_allowed_parameter_creator(parsed_parameters_table, output_list):
    """ A function that generates values that are not in the allowed list """
    output_dict = _create_output_parameters_dict()
    for parameter_name, rules_dict in parsed_parameters_table.items():
        if rules_dict['allowed_values']:
            wrong_parameter = _random_string_gen()
            if wrong_parameter not in rules_dict['allowed_values']:
                output_dict['params'][parameter_name] = wrong_parameter
                output_dict['errors'][parameter_name] = 'is not allowed value'
        else:
            output_dict['params'][parameter_name] = rules_dict['default_value']
    output_list.append(output_dict)


def _wrong_type_parameters_gen(custom_type):
    """
    A decorator is used for identifying functions, which generates wrong parameters for custom types.
    This is used for easy extensibility.
    """
    def inner_decorator(func):
        _wrong_type_parameter_creators[custom_type] = func
        return func
    return inner_decorator


@_wrong_type_parameters_gen('string')
def _string_type_wrong_parameter_gen(parameter_name, output_dict):
    """ Generates an invalid value for string custom type """
    output_dict['params'][parameter_name] = random.randrange(1, 100000)
    return False


@_wrong_type_parameters_gen('domain')
def _domain_type_wrong_parameter_gen(parameter_name, output_dict):
    """ Generates an invalid value for domain custom type """
    output_dict['params'][parameter_name] = _random_string_gen()
    return False


@_wrong_type_parameters_gen('birthday')
def _birthday_wrong_type_parameter_gen(parameter_name, output_dict):
    """ Generates an invalid value for birthday custom type """
    wrong_day_string = str(random.randrange(32, 100))
    wrong_month_string = str(random.randrange(13, 100))
    wrong_year_string = _random_string_gen()
    wrong_birthday_string = '{}-{}-{}'.format(wrong_day_string, wrong_month_string, wrong_year_string)
    output_dict['params'][parameter_name] = wrong_birthday_string
    return False


@_wrong_type_parameters_gen('phone')
def _phone_wrong_type_parameter_gen(parameter_name, output_dict):
    """ Generates an invalid value for phone custom type. Can be either a str or an int """
    if random.randint(0, 1):
        # generating wrong alpha-numeric string
        wrong_country_code = _random_string_gen(random.randint(1, 3))
        wrong_area_code = _random_string_gen(3)
        wrong_exchange_number = _random_string_gen(3)
        wrong_subscriber_number = _random_string_gen(4)
        wrong_phone = wrong_country_code + wrong_area_code + wrong_exchange_number + wrong_subscriber_number
    else:
        # generating int value
        wrong_phone = random.randint(10000000000, 1000000000000)
    output_dict['params'][parameter_name] = wrong_phone
    return False


@_wrong_type_parameters_gen('password')
def _password_wrong_type_parameter_gen(parameter_name, output_dict):
    """
    Generates an invalid value for password custom type.

    An incorrect value is a value with a complexity of less than or equal to 4
    """
    def upper_case_count_in(password):
        uppercase_letters = re.findall('[A-Z]', password)
        return uppercase_letters

    def lower_case_count_in(password):
        lowercase_letters = re.findall('[a-z]', password)
        return lowercase_letters

    def special_characters_count_in(password):
        special_characters = re.findall('[\W_]', password)
        return special_characters

    def check_password_length(password):
        if len(password) > 11:
            return 2
        elif len(password) > 5:
            return 1
        else:
            return 0

    def calculate_strength_for(criteria):
        if len(criteria) > 1:
            return 2
        if len(criteria) == 1:
            return 1
        else:
            return 0

    not_weak_password = True
    while not_weak_password:
        generated_password = _random_string_gen(size=random.randint(1, 4),
                                                chars=string.ascii_letters + string.digits + string.punctuation)
        result_strength = \
            calculate_strength_for(upper_case_count_in(generated_password)) + \
            calculate_strength_for(lower_case_count_in(generated_password)) + \
            calculate_strength_for(special_characters_count_in(generated_password)) + \
            check_password_length(generated_password)
        if result_strength <= 4:
            output_dict['params'][parameter_name] = generated_password
            output_dict['errors'][parameter_name] = 'weak'
            return True
