import json
from parameters_validator import parameters_validator
from config import checking_rules_list, test_parameters_dicts_list


def use_parameters_validator(jsons_list):
    for rules_json in jsons_list:
        output_dict = parameters_validator(rules_json, checking_rules_list)
        print(json.dumps(output_dict, indent=4))


if __name__ == '__main__':
    use_parameters_validator(test_parameters_dicts_list)
