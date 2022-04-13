#!/bin/bash

# convert REs to NFA
mkdir -p nfa_images
python convert_re_to_nfa.py
dot -Tpng test_nfa_1.gv -o nfa_images/test_1.png
dot -Tpng test_nfa_2.gv -o nfa_images/test_2.png

# convert NFA to DFA
mkdir -p dfa_images
python convert_nfa_to_dfa.py
dot -Tpng test_dfa_1.gv -o dfa_images/test_1.png
dot -Tpng test_dfa_2.gv -o dfa_images/test_2.png

# run scanner
# python run_table_driven_scanners.py

# run parser
python LL\(1\)_parsing_table_parser.py
dot -Tpng parsing_tree.gv -o parsing_tree.png
