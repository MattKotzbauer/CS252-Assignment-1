import ast
import math

class Term:
    def __init__(self, term_type, *args):
        self.term_type = term_type
        self.args = args

with open('input.txt', 'r') as f:
    lines = f.readlines()

# Initializing global variables
sample_inputs = None
output_data = None
available_ints = None
available_strings = None
defined_grammar = None

# Reading file and extracting data into lists
prefixes = ["Sample Inputs:", "Sample Outputs:", "Int Literals:", "String Literals:", "Defined Grammar:"]
for line in lines:
    line = line.strip()  
    for prefix in prefixes:
        if line.startswith(prefix):
            data = line[len(prefix):].strip()
            if prefix == "Sample Inputs:":
                sample_inputs = ast.literal_eval(data)
            elif prefix == "Sample Outputs:":
                sample_outputs = ast.literal_eval(data)
            elif prefix == "Int Literals:":
                available_ints = ast.literal_eval(data)
            elif prefix == "String Literals:":
                available_strings = ast.literal_eval(data)
            elif prefix == "Defined Grammar:":
                defined_grammar = set(ast.literal_eval(data))

existing_outputs = set([])
matching_fn = None
matching_fn_string = ""
complete = False

input_vars = [f"Input_{i + 1}" for i in range(len(sample_inputs[0]))]

INPUT = "Input"

# String Manipulation Grammar

LOWERCASE = "Lowercase"
UPPERCASE = "Uppercase"
PROPERCASE = "Propercase"
CONCAT = "Concat"
RIGHT = "Right"
LEFT = "Left"
SUBSTR = "Substr"
REPLACE = "Replace"
TRIM = "Trim"
string_grammar = [LOWERCASE, UPPERCASE, PROPERCASE, CONCAT, RIGHT, LEFT, SUBSTR, REPLACE, TRIM]

# Integer Manipulation Grammar

ADD = "Add"
SUB = "Sub"
MULT = "Mult"
DIV = "Div"
MOD = "Mod"
LOG = "Log"
POW = "Pow"
int_grammar = [ADD, SUB, MULT, DIV, MOD, LOG, POW]

# Bitwise Manipulation Grammar

AND = "And"
OR = "Or"
XOR = "Xor"
NOT = "Not"
LSHIFT = "LShift"
RSHIFT = "RShift"
bit_grammar = [AND, OR, XOR, NOT, LSHIFT, RSHIFT]

# Recursively prints terms by iterating through class structure
def print_term(term):
    def print_recursive(term, indent=0):
        if term.term_type in available_strings:
            print(f'"{term.term_type}"', end="")
        elif isinstance(term.term_type, int):
            print(f"{term.term_type}", end="")
        else:
            print(f"{term.term_type}", end = "")
        if not isinstance(term.term_type, int) and term.term_type[:5] != INPUT and not term.term_type in available_strings:
            print("(", end = "")
        if term.args:
            for i in range(len(term.args)):
                arg = term.args[i]
                if i > 0:
                    print(", ", end = "")
                if isinstance(arg, Term):
                    print_recursive(arg)
                elif isinstance(arg, int):
                    print(arg, end="")
                else:
                    print("unsupported type", end="")
            print(")", end = "")
    print_recursive(term)

class UnsupportedTermError(Exception):
    pass

# Evaluates terms to a numerical or string value by recursively using class system
def evaluate(term, input):
    
    if isinstance(term.term_type, int):
        return term.term_type
    elif term.term_type[:5] == INPUT:
        index = term.term_type[6:]
        return input[int(index) - 1]
    elif term.term_type in available_strings:
        return term.term_type    
    
    # String Manipulation Operations
    
    def lowercase_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        return eval_term.lower()
    def uppercase_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        return eval_term.upper()      
    def propercase_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        return eval_term.title()      
    def concat_eval(term, input):
        eval_term1 = evaluate(term.args[0], input)
        eval_term2 = evaluate(term.args[1], input)
        return eval_term1 + eval_term2
    def right_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        n = term.args[1]
        return eval_term[-n:]   
    def left_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        n = term.args[1]
        return eval_term[:n]
    def substr_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        start = term.args[1]
        end = term.args[2]
        return eval_term[start:end]
    def replace_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        old = evaluate(term.args[1], input)
        new = evaluate(term.args[2], input)
        return eval_term.replace(old, new)
    def trim_eval(term, input):
        eval_term = evaluate(term.args[0], input)
        return ''.join(eval_term.split())
    
    # Integer Manipulation Operations
    
    def add_eval(term, input):
        return int(evaluate(term.args[0], input)) + int(evaluate(term.args[1], input))
    def sub_eval(term, input):
        return int(evaluate(term.args[0], input)) - int(evaluate(term.args[1], input))
    def mult_eval(term, input):
        return int(evaluate(term.args[0], input)) * int(evaluate(term.args[1], input))
    def div_eval(term, input):
        term1, term2 = int(evaluate(term.args[0], input)), int(evaluate(term.args[1], input))
        if term2 == 0:
            return term1
        return term1 / term2
    def mod_eval(term, input):
        term1, term2 = int(evaluate(term.args[0], input)), int(evaluate(term.args[1], input))
        if term2 == 0:
            return term1
        return term1 % term2
    def log_eval(term, input):
        term1, term2 = int(evaluate(term.args[0], input)), int(evaluate(term.args[1], input))
        if (term1 == 1 or term1 <= 0) or (term2 <= 0):
            return term1
        return int(math.log(term2, term1))
    def pow_eval(term, input):
        return int(evaluate(term.args[0], input)) ** int(evaluate(term.args[1], input))

    # Bitwise Manipulation Operations
    
    def and_eval(term, input):
        return int(evaluate(term.args[0], input)) & int(evaluate(term.args[1], input))
    def or_eval(term, input):
        return int(evaluate(term.args[0], input)) | int(evaluate(term.args[1], input))
    def xor_eval(term, input):
        return int(evaluate(term.args[0], input)) ^ int(evaluate(term.args[1], input))
    def not_eval(term, input):
        return ~(int(evaluate(term.args[0], input)))
    def lshift_eval(term, input):
        return int((evaluate(term.args[0], input))) << int(term.args[1])
    def rshift_eval(term, input):
        return int((evaluate(term.args[0], input))) >> int(term.args[1])

    switch = {
        LOWERCASE: lowercase_eval,
        UPPERCASE: uppercase_eval,
        PROPERCASE: propercase_eval,
        CONCAT: concat_eval,
        RIGHT: right_eval,
        LEFT: left_eval,
        SUBSTR: substr_eval,
        REPLACE: replace_eval,
        TRIM: trim_eval,
        
        ADD: add_eval,
        SUB: sub_eval,
        MULT: mult_eval,
        DIV: div_eval,
        MOD: mod_eval,
        LOG: log_eval,
        POW: pow_eval,
        
        AND: and_eval,
        OR: or_eval,
        XOR: xor_eval,
        NOT: not_eval,
        LSHIFT: lshift_eval,
        RSHIFT: rshift_eval,
    }
    handler = switch.get(term.term_type)
    if handler:
        return handler(term, input)
    else:
        raise UnsupportedTermError(f"Unsupported term type: {term.term_type}")

# Expands range of functions along specified grammar
def expand(possible_fns):
    global available_ints
    possible_fns_length = len(possible_fns)
    # Apply selected grammar to all applicable functions
    for i in range(possible_fns_length):
        
        '''
        Iterates through current list of functions, applying defined grammar to each element.
        For functions with multiple arguments, such as Concat, we iterate 
        through each possible combination of arguments.
        '''
        
        # String Manipulation Operations
        
        for j in range(i, possible_fns_length):
            possible_fns.extend([Term(CONCAT, possible_fns[i], possible_fns[j]), Term(CONCAT, possible_fns[j], possible_fns[i])]) if CONCAT in defined_grammar else None
            if REPLACE in defined_grammar:
                for k in range(j+1, possible_fns_length):
                    possible_fns.append(Term(REPLACE, possible_fns[i], possible_fns[j], possible_fns[k]))
                    possible_fns.append(Term(REPLACE, possible_fns[i], possible_fns[k], possible_fns[j]))
        for s in [LOWERCASE, UPPERCASE, PROPERCASE, TRIM]:
            possible_fns.append(Term(s, possible_fns[i])) if s in defined_grammar else None
        for n in range(len(available_ints)):
            possible_fns.append(Term(RIGHT, possible_fns[i], available_ints[n])) if RIGHT in defined_grammar else None
            possible_fns.append(Term(LEFT, possible_fns[i], available_ints[n])) if LEFT in defined_grammar else None
            if SUBSTR in defined_grammar:
                for m in range(n+1, len(available_ints)):
                    possible_fns.append(Term(SUBSTR, possible_fns[i], available_ints[n], available_ints[m]))
        
        # Integer Manipulation Operations
        
        for j in range(i, possible_fns_length):
            # (As Add and Mult are commutative, we need only apply them in one order)
            possible_fns.append(Term(ADD, possible_fns[i], possible_fns[j])) if ADD in defined_grammar else None
            possible_fns.append(Term(MULT, possible_fns[i], possible_fns[j])) if MULT in defined_grammar else None
            for s in [SUB, DIV, MOD, LOG, POW]:
                possible_fns.extend([Term(s, possible_fns[i], possible_fns[j]), Term(s, possible_fns[j], possible_fns[i])]) if s in defined_grammar else None
        
        # Bitwise Manipulation Operations
        
        for j in range(i, possible_fns_length):
            for s in [AND, OR, XOR]:
                possible_fns.append(Term(s, possible_fns[i], possible_fns[j])) if s in defined_grammar else None
        possible_fns.append(Term(NOT, possible_fns[i])) if NOT in defined_grammar else None
        for n in available_ints:
            possible_fns.append(Term(LSHIFT, possible_fns[i], n)) if LSHIFT in defined_grammar else None
            possible_fns.append(Term(RSHIFT, possible_fns[i], n)) if RSHIFT in defined_grammar else None            
        
    return possible_fns

pruning_index = 0

# Prunes obervationally equivalent functions
def prune_equivalents(possible_fns):
    global pruning_index
    global matching_fn
    global complete
    i = pruning_index
    while i < len(possible_fns):
        # Take outputs as a sequence of function results
        fn_outputs = []
        for j in range(len(sample_inputs)):
            # Append function result to list
            fn_outputs.append(evaluate(possible_fns[i], sample_inputs[j]))
            
        # Convert to tuple to allow for set hashing
        fn_outputs_tuple = tuple(fn_outputs)
        
        # If outputs already exist, prune function
        if fn_outputs_tuple in existing_outputs:
            del possible_fns[i]
        
        # If outputs match our target outputs, we've found our function!
        elif fn_outputs_tuple == tuple(sample_outputs) and not complete:
            matching_fn = possible_fns[i]
            complete = True
            return None
        
        # Otherwise, add as new existing output
        else:
            existing_outputs.add(fn_outputs_tuple) 
            i += 1
            pruning_index += 1
    return possible_fns

def synthesize(): 
    global available_strings
    global defined_grammar
    global int_grammar
    
    # Initialize possible functions to empty list
    possible_fns = []
    
    # Append literals and inputs as base values
    for s in available_strings:
        possible_fns.append(Term(s))
    if all(fn in int_grammar for fn in defined_grammar):
        for i in available_ints:
            possible_fns.append(Term(i))
    for input_var in input_vars:
        possible_fns.append(Term(input_var))
    
    stepCount = 0
    # Loop through process of expanding and pruning
    while(stepCount < 10):
        possible_fns = expand(possible_fns)
        possible_fns = prune_equivalents(possible_fns)
        # Return the matching function if it's been identified
        if matching_fn:
            return possible_fns
        stepCount +=1
    return "Term Limit Exceeded"

# Call synthesizer function and print matching function if we find one!
synth_fns = synthesize()
print("Matching Fn:")
print_term(matching_fn)