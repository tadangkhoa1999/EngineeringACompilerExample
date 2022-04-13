# Ta Dang Khoa - VNU - 21025077
# LL(1) Parsing-table Parser (Top-Down Parser)


import json
from finite_automaton import FiniteAutomaton

from run_table_driven_scanners import table_driven_scanners
from get_first_and_follow_sets import is_non_terminal, get_first_set, get_follow_set


def get_parsing_table(rules, first_set, follow_set):
    parsing_table = {}
    for key, rule in rules.items():
        for sub_rule in rule:
            symbol = sub_rule[0]
            if is_non_terminal(rules, symbol): 
                for ter in first_set[symbol] - {"ϵ"}:
                    parsing_table[key, ter] = {key: sub_rule}
            elif symbol == "ϵ" or (symbol in first_set.keys() and symbol in first_set[symbol]):
                for ter in follow_set[key]:
                    parsing_table[key, ter] = {key: ["ϵ"]}
            else:
                parsing_table[key, symbol] = {key: sub_rule}
    return parsing_table


def get_name(s):
    convert_dict = {
        ';': 'cham_phay',
        '=': 'bang',
        '-': 'tru',
        '*': 'nhan',
        '^': 'mu',
        '(': 'mo_ngoac',
        ')': 'dong_ngoac'
    }
    if s in convert_dict.keys():
        return convert_dict[s]
    else:
        return s


def parser(parsing_table, start_state, words):
    draw_info = 'digraph G {\n'
    states = {start_state: 1}
    draw_info += '\t{}_1 [label="{}"];\n'.format(start_state, start_state)
    stack_state_idx = [1]

    stack = []
    stack.append(start_state)

    inp = 0
    while(stack and words[inp]):
        print("{:<10} {}".format(words[inp], stack))
        popped = stack.pop()
        popped_state_idx = stack_state_idx.pop()
        while (popped == 'ϵ'):  # when popped is epsilon then again pop
            popped = stack.pop()
            popped_state_idx = stack_state_idx.pop()
        if popped != words[inp]:
            if parsing_table.get((popped, words[inp])):  # for checking, this entry is in table or not ?
                rule = parsing_table.get((popped, words[inp])).get(popped)  # 2D dict table is again 1D dict with that rule

                from_state = '{}_{}'.format(get_name(popped), popped_state_idx)
                for s in rule:
                    if s not in states.keys():
                        states[s] = 1
                    else:
                        states[s] += 1
                    draw_info += '\t{}_{} [label="{}"];\n'.format(get_name(s), states[s], s)
                    to_state = '{}_{}'.format(get_name(s), states[s])
                    draw_info += '\t{} -> {};\n'.format(from_state, to_state)

                for x in range(len(rule)):
                    stack_state_idx.append(states[rule[-x-1]])
                    stack.append(rule[-x-1])  # minus for reversing
            else:
                print("\nWrong with word index {} - '{}'".format(inp, words[inp]))
                return
        else:
            inp += 1

    draw_info += '}'
    with open('parsing_tree.gv', 'w') as f:
        f.write(draw_info)


if __name__ == '__main__':
    print('Running Scanner...')
    dfa = FiniteAutomaton()
    dfa.readGVFile('dfa.gv')
    alphabet, transition_table = dfa.getTransitionTable()
    accepting_states = [state.label for state in dfa.accepting_states]

    all_words = []
    with open('input_code.txt', 'r') as f:
        for line in f.readlines():
            all_words.extend(line.split())

    output_words = []
    for word in all_words:
        output_words.extend(table_driven_scanners(alphabet, transition_table, accepting_states, word + ' '))  # add space to confirm that it always contain error state
        if 'error' in output_words:
            output_words = ['error']
            break

    output_word_types = []
    for word in output_words:
        if word in ['begin', 'end', 'EOF', 'print', 'int', 'while', 'do', ';', '=', '-', '*', '^', '(', ')']:
            output_word_types.append(word)
        else:
            try:
                int(word)
                output_word_types.append('num')
            except:
                output_word_types.append('name')

    print("Words:", output_words)
    print("Types:", output_word_types)

    print('\nRunning Parser...')
    # get rules
    with open("rule.json", "r") as f:
        rules = json.load(f)
    start_state = "Program"

    # get first set
    first_set = get_first_set(rules)

    # get follow set
    follow_set = get_follow_set(rules, first_set)

    # get parsing table
    parsing_table = get_parsing_table(rules, first_set, follow_set)

    parser(parsing_table, start_state, output_word_types)
