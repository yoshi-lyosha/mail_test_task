import json
from parameters_validator import parameters_validator
from config import checking_rules_list, test_parameters_dicts_list


def use_parameters_validator(jsons_list):
    output_list = list()
    for rules_json in jsons_list:
        output_dict = parameters_validator(rules_json, checking_rules_list)
        output_list.append(output_dict)
    return output_list


if __name__ == '__main__':
    validated_parameters_list = use_parameters_validator(test_parameters_dicts_list)
    print(json.dumps(validated_parameters_list, indent=4))
