

CS252 Assignment 1: Bottom-Up Search

For my Assignment 1, I implemented a flexible-grammar BUS within numeric, string, and bitwise DSL's. Starting with the function inputs and base values, it builds its search space by plugging the arguments into all available specified functions. 

In input.txt, the user is prompted to configure five lists:

Sample Inputs: The list of sample inputs that are entered into the function (a two-dimensional list, even if dealing with single inputs: can handle an arbitrary number of inputs within any input sequence).

Sample Outputs: The expected outputs of the sample inputs being passed into the function. More specifically, if the list at index i of the sample input array is passed into the function, then the value at index i of the sample output array must be yielded by the synthesized function.

Int Literals (applicable over all DSL's): The list of base ints that will be fed into the program. Performs the following functions within each DSL:
	* Arithmetic: Fed as a base value into the list of functions, and will thus be applied with equal weights as the inputs themselves - for instance, if we pass an int literal 1 into the Add operation, our first round of generation will yield Add(1,1) (alongside Add(Input_1, 1) and Add(Input_1, Input_1))
	* String: Used as an auxiliary value within the Left, Right, and Substr operations. List of ints will not be modified (e.g. if the user specifies '1', it will not add to itself to feed '2' into the functions)
	* Bitwise: Used as an auxiliary value within the LShift and RShift operations

String Literals (applicable only within String DSL): A list of base strings that will be fed into the program and treated with equal weight as the input strings. For example, if we set the string "foo" to be a string literal, the Concat operation would yield the following values in first-round generation: Concat("foo", "foo"), concat(Input_1, "foo"), Concat("foo", Input_1), Concat(Input_1), Input_1)

Defined Grammar: Operations that are defined within the search space. The search space will only expand along these values, allowing the user to achieve more complex programs by limiting the grammar to necessary operations. The full grammar for each DSL is listed below: 
Numeric: ["Add", "Sub", "Mult", "Div", "Mod", "Log", "Pow"]
String: ["Lowercase", "Uppercase", "Propercase", "Concat", "Right", "Left", "Substr", "Replace", "Trim"]
Bitwise: ["And", "Or", "Xor", "Not", "RShift", "LShift"]

Note that, while you can do string synthesis without defining string literals, you cannot do arithmetic synthesis while defining them - a limitation of this program is that it can only parse 1 DSL at a time, and crossing the DSL's in this way introduces typing errors. Similarly, defining contradicting input / output examples and grammar (e.g. string input / output and the "Add" operation) will throw an error.

Another potential drawback of this program is that, while it models its creation of programs after an AST, it does not store the parents of the generated functions, only testing the functions themselves. To make this structure more condusive to such a representation, we could add an extra element to the 'Term' class that specifies its parent function or the parent's index within the storage. 

My code stores generated functions in a list for a couple of reasons: 
	* The operations needed to synthesize new functions are lookup and appending, both of which are O(1) within a list
	* When pruning, the deletion operation occurs closer to the end of the list, as we prune newly-generated elements
A potential way to save on time complexity could be to re-define the 'Term' class to be hashable and then store it in a set, saving time on the deletion operation.
  


Input / Output Examples (TODO): 

Input:
Sample Inputs: [[6, 3], [12, 9]]
Sample Outputs: [8, 32]
Int Literals: [1, 2]
String Literals: []
Defined Grammar: ["LShift", "And"]

Output:
LShift(And(Input_1, Input_2), 2)
(.1 second)

Input: 
Sample Inputs: [[6, 17], [19, 13], [12, 11]]
Sample Outputs: [-72, -62, -47]
Int Literals: [1, 2]
String Literals: []
Defined Grammar: ["RShift", "LShift", "And", "Xor", "Not"]

Output: 
And(RShift(Not(Input_1), 1), Not(LShift(Input_2, 2)))
(30 seconds)
