class Term:
    def __init__(self, term_type, *args):
        self.term_type = term_type
        self.args = args

#sample_inputs = [["cool", "thing"], ["ling", "er"], ["san", "San"]]
#sample_outputs = ["THINGCOOL", "ERLING", "SANSAN"] 
sample_inputs = [["cool", "thing"], ["chosen", "one"]]
sample_outputs = ["Cool thing", "Chosen one"]
existing_outputs = set([])
matching_fn = None
matching_fn_string = ""
complete = False

input_vars = [f"Input_{i + 1}" for i in range(len(sample_inputs[0]))]
available_ints = [0, 1, 2, 3, 99]
available_strings = [" ", ", ", "+"]

INPUT = "Input"
LOWERCASE = "Lowercase"
UPPERCASE = "Uppercase"
PROPERCASE = "Propercase"
CONCAT = "Concat"
RIGHT = "Right"
LEFT = "Left"
SUBSTR = "Substr"
REPLACE = "Replace"
TRIM = "Trim"

def print_term(term):
    def print_recursive(term, indent=0):
        if term.term_type in available_strings:
            print(f'"{term.term_type}"', end="")
        else:
            print(f"{term.term_type}", end = "")
        if term.term_type[:5] != INPUT and not term.term_type in available_strings:
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

def evaluate(term, input):
    
    if term.term_type[:5] == INPUT:
        index = term.term_type[6:]
        return input[int(index) - 1]
    elif term.term_type in available_strings:
        return term.term_type    
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
    switch = {
        LOWERCASE: lowercase_eval,
        UPPERCASE: uppercase_eval,
        PROPERCASE: propercase_eval,
        CONCAT: concat_eval,
        RIGHT: right_eval,
        LEFT: left_eval,
        SUBSTR: substr_eval,
        REPLACE: replace_eval,
        TRIM: trim_eval
    }
    handler = switch.get(term.term_type)
    if handler:
        return handler(term, input)
    else:
        raise UnsupportedTermError(f"Unsupported term type: {term.term_type}")

def expand(possible_fns):
    global available_ints
    possible_fns_length = len(possible_fns)
    for i in range(possible_fns_length):
        for j in range(i, possible_fns_length):
            possible_fns.append(Term(CONCAT, possible_fns[i], possible_fns[j]))
            possible_fns.append(Term(CONCAT, possible_fns[j], possible_fns[i]))
            for k in range(j+1, possible_fns_length):
                possible_fns.append(Term(REPLACE, possible_fns[i], possible_fns[j], possible_fns[k]))
                possible_fns.append(Term(REPLACE, possible_fns[i], possible_fns[k], possible_fns[j]))
        possible_fns.append(Term(LOWERCASE, possible_fns[i]))
        possible_fns.append(Term(UPPERCASE, possible_fns[i]))
        possible_fns.append(Term(PROPERCASE, possible_fns[i]))
        possible_fns.append(Term(TRIM, possible_fns[i]))
        for n in range(len(available_ints)):
            possible_fns.append(Term(RIGHT, possible_fns[i], available_ints[n]))
            possible_fns.append(Term(LEFT, possible_fns[i], available_ints[n]))
            for m in range(n+1, len(available_ints)):
                possible_fns.append(Term(SUBSTR, possible_fns[i], available_ints[n], available_ints[m]))
    return possible_fns

pruning_index = 0

def prune_equivalents(possible_fns):
    global pruning_index
    global matching_fn
    global complete
    i = 0
    while i < len(possible_fns):
        fn_outputs = []
        for j in range(len(sample_inputs)):
            fn_outputs.append(evaluate(possible_fns[i], sample_inputs[j]))
        fn_outputs_tuple = tuple(fn_outputs)  # Convert to tuple
        if fn_outputs_tuple in existing_outputs:
            del possible_fns[i]
        elif fn_outputs_tuple == tuple(sample_outputs) and not complete:
            #print("found fn")
            matching_fn = possible_fns[i]
            complete = True
            return None
        else:
            existing_outputs.add(fn_outputs_tuple)  # Add as a tuple
            i += 1
            pruning_index += 1
    return possible_fns


def synthesize(): 
    global available_strings
    possible_fns = []
    for s in available_strings:
        possible_fns.append(Term(s))
    for input_var in input_vars:
        possible_fns.append(Term(input_var))
    stepCount = 0
    while(True):
        possible_fns = expand(possible_fns)
        possible_fns = prune_equivalents(possible_fns)
        if matching_fn:
            return possible_fns
            #return matching_fn
        stepCount +=1
        if stepCount > 6: 
            return "whoops"

synth_fns = synthesize()
print("matching fn:")
print_term(matching_fn)
#print("possible fns:")
#for fn in synth_fns:
#    print_term(fn)

