import re
from datetime import datetime
from collections import defaultdict

_custom_types_checkers = dict()


def parameters_validator(input_dict, rules):
    """ Validates the input parameters for compliance with the rules """
    output_dict = dict()
    output_dict['params'] = {}
    # for easy-using .append method
    output_dict['errors'] = defaultdict(list)
    for parameter_name, rules_list in rules.items():
        minlength, maxlength, parameter_type, allowed_values, necessity, default_value = _parse_rules_list(rules_list)
        parameter_value = input_dict[parameter_name]
        if parameter_value:
            output_dict['params'][parameter_name] = parameter_value
            _validate_type(parameter_value, parameter_name, parameter_type, allowed_values, output_dict)
            _validate_allowed_values(parameter_value, parameter_name, allowed_values, output_dict)
            _validate_length(parameter_value, parameter_name, minlength, maxlength, output_dict)
        else:
            _validate_necessity(parameter_name, necessity, default_value, output_dict)
    output_dict['errors'] = dict(output_dict['errors'])
    return output_dict


def _parse_rules_list(rules_list):
    """ Parsing the rules list """
    minlength = _find_dict_value_in_rules_list(rules_list, 'minlength', int)
    maxlength = _find_dict_value_in_rules_list(rules_list, 'maxlength', int)
    allowed_values = _find_dict_value_in_rules_list(rules_list, 'allowed_values', list)
    default_value = _find_dict_value_in_rules_list(rules_list, 'default_value', str)
    necessity = list(filter(lambda var: var == 'required' or var == 'optional', rules_list))[0]
    parameter_type = rules_list[0]
    return minlength, maxlength, parameter_type, allowed_values, necessity, default_value


def _find_dict_value_in_rules_list(rules_list, rule_str, value_type):
    """ Function to find a specific dictionary in the list """
    rule_value_generator = (rule[rule_str] for rule in rules_list if rule_str in rule)
    try:
        rule_value = value_type(*rule_value_generator)
    except TypeError as e:
        # adding information to an exception
        raise TypeError("{}; '{}' doesn't fit to '{}'".format(str(e), value_type, rule_str))
    return rule_value if rule_value else None


def _validate_necessity(parameter_name, necessity, default_value, output_dict):
    """
    A function that checks necessity of parameter, and if it is required, tries to substitute a default value.
    If it is optional parameter, assigns a None value.
    """
    if default_value:
        output_dict['params'][parameter_name] = default_value
    elif necessity == 'required':
        output_dict['errors'][parameter_name].append('required')
    else:
        output_dict['params'][parameter_name] = None


def _validate_type(parameter_value, parameter_name, parameter_type, allowed_values, output_dict):
    """ A function that checks for a match to a custom type """
    # functions that check custom types are stored in the dictionary by the names of these types
    custom_type_check = _custom_types_checkers[parameter_type](parameter_value=parameter_value,
                                                               parameter_name=parameter_name,
                                                               parameter_type=parameter_type,
                                                               allowed_values=allowed_values,
                                                               output_dict=output_dict)
    if not custom_type_check:
        output_dict['errors'][parameter_name].append("not '{}' custom type".format(parameter_type))


def _type_checker(custom_type):
    """
    A decorator is used for identifying functions, which check custom data types.
    This is used for easy extensibility.
    """
    def inner_decorator(func):
        _custom_types_checkers[custom_type] = func
        return func
    return inner_decorator


@_type_checker('string')
def _string_type_checker(**kwargs):
    """ Checking for a 'string' type """
    parameter_str_instance = isinstance(kwargs['parameter_value'], str)
    return True if parameter_str_instance else False


@_type_checker('birthday')
def _birthday_type_checker(**kwargs):
    """ Checking for a 'birthday' type """
    if isinstance(kwargs['parameter_value'], str):
        try:
            datetime.strptime(kwargs['parameter_value'], '%d-%m-%Y')
            return True
        except ValueError:
            pass
    return False


@_type_checker('phone')
def _phone_type_checker(**kwargs):
    """ Checking for a 'phone' type """
    if isinstance(kwargs['parameter_value'], str):
        phone_pattern = r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{2}-?\d{2})(?: *x(\d+))?\s*$'
        return True if re.match(phone_pattern, kwargs['parameter_value']) else False


@_type_checker('password')
def _password_type_checker(**kwargs):
    """ Checking for a 'password' type and counting its complexity """
    if isinstance(kwargs['parameter_value'], str):
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

        result_strength = \
            calculate_strength_for(upper_case_count_in(kwargs['parameter_value'])) + \
            calculate_strength_for(lower_case_count_in(kwargs['parameter_value'])) + \
            calculate_strength_for(special_characters_count_in(kwargs['parameter_value'])) + \
            check_password_length(kwargs['parameter_value'])

        if result_strength <= 4:
            kwargs['output_dict']['errors'][kwargs['parameter_name']].append('weak')
        return True
    return False


@_type_checker('domain')
def _domain_type_checker(**kwargs):
    """ Checking for a 'phone' type """
    domain_pattern = r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|' \
                     r'([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$'
    if isinstance(kwargs['parameter_value'], str):
        return True if re.match(domain_pattern, kwargs['parameter_value']) else False
    return False


def _validate_allowed_values(parameter_value, parameter_name, allowed_values, output_dict):
    """ Validating for compliance with acceptable values """
    if allowed_values:
        if parameter_value not in allowed_values:
            output_dict['errors'][parameter_name].append("'{}' is not allowed value".format(parameter_value))


def _validate_length(parameter_value, parameter_name, minlength, maxlength, output_dict):
    """ Validation of admissible length """
    if isinstance(parameter_value, str):
        if minlength:
            if len(parameter_value) <= minlength:
                output_dict['errors'][parameter_name].append('too short')
        if maxlength:
            if len(parameter_value) >= maxlength:
                output_dict['errors'][parameter_name].append('too long')
    else:
        output_dict['errors'][parameter_name].append('has no length')
