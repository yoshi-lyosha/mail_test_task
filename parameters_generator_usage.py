import json
from parameters_generator import wrong_parameters_creator
from config import generator_rules


def use_parameters_generator(rules):
    output_dict = wrong_parameters_creator(rules)
    return output_dict


if __name__ == '__main__':
    parameters_dict = use_parameters_generator(generator_rules)
    print(json.dumps(parameters_dict, indent=4))
