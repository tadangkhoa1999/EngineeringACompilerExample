# Ta Dang Khoa - VNU - 21025077
# REs to NFA - Thompson's Construction


from string import ascii_lowercase
from finite_automaton import FiniteAutomaton, run_operations


def shunt(infix):
    '''
    convert in-fix RE to po-fix RE

    Notes:
    -----
    We only support some basic operations (for example only)
    - * = 0 or more
    - | = or
    - . = concatenate
    '''
    specials = {'*': 50, '.': 40, '|': 30}
    pofix = ""
    stack = ""
    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]  # remove '(' from stack
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            pofix = pofix + c
    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]
    return pofix


def thompson_construction(RE, use_operation=True):
    '''
    convert RE to NFA

    Params:
    -----
    RE: Regular expression in post fix

    Notes:
    -----
    Only support for |, *, [0-9], [1-9], [a-z], [A-Z]
    '''
    nfa_stack = []
    idx = 0
    while True:
        if idx == len(RE):
            break
        c = RE[idx]
        if c == '*' and use_operation:
            fa = nfa_stack.pop()
            new_fa = run_operations(fa, None, 'closure')
            nfa_stack.append(new_fa)
        elif c == '.' and use_operation:
            fa2 = nfa_stack.pop() 
            fa1 = nfa_stack.pop()
            new_fa = run_operations(fa1, fa2, 'concatenation')
            nfa_stack.append(new_fa)
        elif c == '|' and use_operation:
            fa2 = nfa_stack.pop() 
            fa1 = nfa_stack.pop()
            new_fa = run_operations(fa1, fa2, 'alternation')
            nfa_stack.append(new_fa)
        elif c == '[' and use_operation:
            begin_idx = idx + 1
            while RE[idx] != ']':
                idx += 1
                end_idx = idx
            if RE[begin_idx:end_idx] == 'a-z':
                new_fa = FiniteAutomaton()
                end_state = new_fa.createState()
                new_fa.accepting_states.append(end_state)
                for i in ascii_lowercase:
                    mid_state = new_fa.createState()
                    new_fa.start_state.setNext(i, mid_state)
                    mid_state.setNext('ϵ', end_state)
                nfa_stack.append(new_fa)
            elif RE[begin_idx:end_idx] == 'A-Z':
                new_fa = FiniteAutomaton()
                end_state = new_fa.createState()
                new_fa.accepting_states.append(end_state)
                for i in ascii_lowercase.upper():
                    mid_state = new_fa.createState()
                    new_fa.start_state.setNext(i, mid_state)
                    mid_state.setNext('ϵ', end_state)
                nfa_stack.append(new_fa)
            elif RE[begin_idx:end_idx] == '0-9':
                new_fa = FiniteAutomaton()
                end_state = new_fa.createState()
                new_fa.accepting_states.append(end_state)
                for i in map(lambda x: str(x), range(10)):
                    mid_state = new_fa.createState()
                    new_fa.start_state.setNext(i, mid_state)
                    mid_state.setNext('ϵ', end_state)
                nfa_stack.append(new_fa)
            elif RE[begin_idx:end_idx] == '1-9':
                new_fa = FiniteAutomaton()
                end_state = new_fa.createState()
                new_fa.accepting_states.append(end_state)
                for i in map(lambda x: str(x), range(1, 10)):
                    mid_state = new_fa.createState()
                    new_fa.start_state.setNext(i, mid_state)
                    mid_state.setNext('ϵ', end_state)
                nfa_stack.append(new_fa)
        else:
            new_fa = FiniteAutomaton()
            end_state = new_fa.createState()
            new_fa.accepting_states.append(end_state)
            new_fa.start_state.setNext(c, end_state)
            nfa_stack.append(new_fa)
        idx += 1
    return nfa_stack.pop()


def thompson_construction_list_RE(REs):
    output_fa = FiniteAutomaton()
    end_state = output_fa.createState()
    output_fa.accepting_states.append(end_state)

    for RE in REs:
        if RE not in [';', '=', '-', '*', '^', '(', ')']:
            fa = thompson_construction(shunt(RE))
        else:
            fa = thompson_construction(RE, use_operation=False)
        for state in fa.states:
            output_fa.states.append(state)
        output_fa.start_state.setNext('ϵ', fa.start_state)
        fa.accepting_states[0].setNext('ϵ', end_state)
    output_fa.resetLabel()
    return output_fa


if __name__ == '__main__':
    # test one
    thompson_construction(shunt('0|([1-9].[0-9]*)')).getGVFile('test_nfa.gv')

    # run all
    REs = ['b.e.g.i.n', 'e.n.d', 'E.O.F', 'p.r.i.n.t', 'i.n.t', 'w.h.i.l.e', 'd.o', ';', '=', '-', '*', '^', '(', ')', '([a-z]|[A-Z]).([a-z]|[A-Z]|[0-9])*', '0|([1-9].[0-9]*)']
    thompson_construction_list_RE(REs).getGVFile('nfa.gv')
