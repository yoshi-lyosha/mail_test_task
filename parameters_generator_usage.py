import json
from parameters_generator import wrong_parameters_creator
from config import generator_rules


def use_parameters_generator(rules):
    output_dict = wrong_parameters_creator(rules)
    print(json.dumps(output_dict, indent=4))


if __name__ == '__main__':
    use_parameters_generator(generator_rules)
