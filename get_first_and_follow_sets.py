# Ta Dang Khoa - VNU - 21025077
# Get First set and Follow set for Top-Down Parser


import json


def print_rules(rules):
    print("Rules are:")
    print("="*50)
    for key in rules.keys():
        for i, derives in enumerate(rules[key]):
            if i == 0:
                print("{:<12}->    {}".format(key, " ".join(derives)))
            else:
                print("            |     {}".format(" ".join(derives)))
        print()


def is_non_terminal(rules, symbol):
    if symbol in rules.keys():  # all keys of rules are Non terminals
        return True
    return False


def first(rules, first_set, key):
    for rule in rules[key]:  # for every rule of that Non-terminal
        symbol = rule[0]
        if not is_non_terminal(rules, symbol):  # for terminals (not False => True)
            first_set[key].add(symbol)
        else:  # for terminal 
            first_set[key] = first_set[key].union(first(rules, first_set, symbol))
    return first_set[key]


def get_first_set(rules):
    first_set = {}
    for key in rules.keys():
        first_set[key] = set()
    for key in rules.keys():  # for all rules
        first(rules, first_set, key)
    return first_set


def follow(rules, first_set, follow_set, key):
    for new_key, rule in rules.items():  # for all productions, 1-1 production
        for sub_rule in rule:  # for one production_rules, 1-1 rule
            for i in range(len(sub_rule)):  # for one rule_symbols, 1-1 symbol
                if sub_rule[i] == key:
                    if i+1 < len(sub_rule):  # checking next symbol beta 
                        beta = sub_rule[i+1]  # when beta is present
                        if is_non_terminal(rules, beta):  # add first_set(beta) into follow_set(non_ter)
                            follow_set[key] = follow_set[key].union(first_set[beta])
                            follow_set[key].discard("ϵ")  # trying to remove epsilon, if there is
                        else:
                            follow_set[key].add(beta)
                        if beta in first_set.keys() and 'ϵ' in first_set[beta] and new_key != beta:
                              follow_set[key] = follow_set[key].union(follow(rules, first_set, follow_set, new_key))
                    elif i+1 == len(sub_rule) and new_key!=key: # when beta is not there & != for avoiding infinite loop
                        if is_non_terminal(rules, sub_rule[i]):
                            follow_set[key] = follow_set[key].union(follow(rules, first_set, follow_set, new_key))
    return follow_set[key]


def get_follow_set(rules, first_set):
    follow_set = {}
    for key in rules.keys():
        follow_set[key] = set()
    for key in rules.keys():
        follow(rules, first_set, follow_set, key)
    return follow_set


if __name__ == "__main__":
    # get rules
    with open("rule.json", "r") as f:
        rules = json.load(f)
    start_state = "Program"

    # get first set
    first_set = get_first_set(rules)

    # get follow set
    follow_set = get_follow_set(rules, first_set)

    # print rule
    print_rules(rules)

    # print first set
    print("First sets are:")
    print("="*50)
    for key, value in first_set.items():
        print(key, "=", value)
    print()

    # print follow set
    print("Follow sets are:")
    print("="*50)
    for key, value in follow_set.items():
        print(key, "=", value)
    print()
