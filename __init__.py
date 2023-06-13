from lark import Lark, Transformer, v_args
from lark import UnexpectedToken, UnexpectedInput
from lark.tree import pydot__tree_to_png
from collections import Counter

header = """
    Subject:        Language Processing Technologies
    
    First assignment on parsers using lark library to define the parser/scanner. 
    Grammar and the Transformer class implementation to process the input.

"""
func_inst = """
    INSTRUCTION FOR FUNCTION DEFINITION:
     The functions should be defined as follows:
    
      function name(par1,par2,…) {
         return par1 op par2 op par3…;
      }
    
     - Where name is the function name with the usual restrictions (an alphanumeric string
       beginning with a letter).
     - par1.. are the function parameters whose names follow the same rules as variables names.
     - op is + or * (sum or product). 
     - The function body contains only the return instruction that involves all the parameters.
     - Only one function can be defined.
"""

call_inst = """
    INSTRUCTION FOR FUNCTION CALLING:
     Function call syntax:
    
      name(cost1,cost2,…);
    
     - Where name is the name of a defined function.
     - cost1,… are numeric constants in the same
       number as the function arguments.
"""


grammar_func = """
    start: (function_def)+
    
    function_def: "function" CNAME "(" param_list ")" "{" WS* "return" expr WS* ";" "}"
    
    param_list: CNAME ("," CNAME)*
        
    //? if only one child then not reported/present in the tree!
    // Divide recursively the expresion by + into multiply
    ?expr: expr "+" multiply -> add
        |  multiply

    ?multiply: multiply "*" atom -> mul
        |  atom
    
    atom: CNAME -> variable
    
    SIGNED_NUMBER: "-"? NUMBER
    
    %import common.CNAME
    %import common.ESCAPED_STRING
    %import common.NUMBER
    %import common.WS
    %ignore WS
    %ignore /#[^\\n]*/
"""

grammar_call_1 = """
    start: call?
        
    ?call: f_name "(" param_list ")" ";"
    
    param_list: SIGNED_NUMBER ("," SIGNED_NUMBER)"""

grammar_call_2 = """   
    SIGNED_NUMBER: "-"? NUMBER
    
    %import common.CNAME
    %import common.ESCAPED_STRING
    %import common.SIGNED_INT
    %import common.NUMBER
    %import common.WS
    %ignore WS
    %ignore /#[^\\n]*/
"""


class FunctionTransformer(Transformer):
    def __init__(self, num_const=None , param=None):
        if num_const is not None:
            # Parameter was passed
            self.num_const = num_const
            self.param = param
            #print(self.num_const, type(self.num_const))
            
        else:
            # Parameter was not passed
            print("No parameter was passed")

    @v_args(inline=True)
    def function_def(self, name, params, expr):
        
        if(False):
            print("\t\t ==> Name of function:", name)
            print("\t\t ==> Length(params):",   len(params.children) )
            print("\t\t ==> Params.children: ", params.children, type(params.children))
            print("\t\t ==> Value:\n", expr)
            
                
        return expr
    @v_args(inline=True)
    def variable(self, value):
        #print( self.num_const[ self.param.index(value) ] )
        return float( self.num_const[ self.param.index(value) ] )

    def int_value(self, value):
        return int(value)

    def add(self, values): 
        return values[0] + values[1]   
    
    def mul(self, values):
        return values[0] * values[1]


def parse_function(code, type_op , grammar=grammar_func):
    if (type_op == "definition"):
        parser_def  = Lark(grammar, parser='lalr' , transformer=Transformer())
        return parser_def.parse(code)
    elif(type_op == "call"):
        parser_call = Lark(grammar, parser='lalr' , transformer=Transformer())
        return parser_call.parse(code)

def function_check(name, params, expr):
        
    leaves = get_leaves(expr)

    var_leaves = list(filter(lambda x: x != '+' ,
                                 filter(lambda x: x != '*' , leaves))) #remove('+') remove('*')
        
    if(compare_lists(params.children, var_leaves)):
        print("\t\t ==> Function Received!")
        if(True):
            print("\t           Name of function:",   name)
            print("\t             Length(params):",   len(params.children) )
            print("\t            Params.children:",   params.children, type(params.children))
            #print("\t Tree generated in the form:\n", expr.pretty())
        return True
    
    else:
        print("\t\t ==> Incorrect Function Definition! Function incongruent with arguments.")
        return False

    
def get_leaves(tree):
    if isinstance(tree, str):  # Base case: leaf node
        return [tree]
        
    leaves = []
        
    for child in tree.children:
        leaves.extend(get_leaves(child))
            
    return leaves
    
def compare_lists(list1, list2):
    counter1 = Counter(list1)   # creates Counter objects for each list, 
    counter2 = Counter(list2)   # which count the occurrences of each element in the list.
    
    return counter1 == counter2 # determine if the two lists contain the same elements, regardless of the order.

def main():
    
    print(header)
    print(func_inst)
    #print("*** Grammar for the function definition:\n", grammar_func)
    example = """        
    function F1( a, b , c , d , e ) { return b * a + e * d + c ; }    
    """
    print("\t\t ==> Example:\t", example)
    
    while(True):
        try:
            code = input("\t\t >>> Please enter the funtion definition:\t")
            parse_tree = parse_function(code, "definition")
            func_def = parse_tree.children[0]  # For one function definition
            #print("func_def.children:\t", func_def.children)
            if (function_check(*func_def.children)):
                break
        except UnexpectedToken as error:
            print("\t### ERROR: Unexpected token %s" % error.token)
            print(error.get_context(code))  
        except UnexpectedInput as error:
            print("\t### ERROR: Parser error!")
            print(error.get_context(code))
        except Exception as error:
            print(error)
    
    #print(parse_tree)
    #print("\t\t ==> Whole tree:\n", parse_tree.pretty())    
    pydot__tree_to_png(parse_tree, 'Function.png')
    print(call_inst)
    
    # Forging grammar for call:
    n_arg  = '~' + str(len(func_def.children[1].children)-1)+'\n'
    f_name = "\tf_name : \"" + func_def.children[0]+"\"\n"    
    grammar_call = grammar_call_1 + n_arg + f_name + grammar_call_2 
    #print("*** Grammar for the function calling:\n", grammar_call)
    
    example2 = func_def.children[0] + "( -1.6"
    for num in range (len(func_def.children[1].children)-1):
        example2 = example2 + " , " + str(num)
    example2 = example2 + " );"
    print("\t\t ==> Example:\t", example2)
    
    while(True):
        
        try:                  
            code2 = input("\n\t\t >>> Please enter the function calling:\t")
            if(code2 == "stop"):
                break
            call_tree = parse_function( code2 , "call" , grammar_call)            
            pydot__tree_to_png(call_tree, 'Function2.png')
            
            '''A Transformer object is created'''
            # -The transform() method is called on the tree resulting from parsing [parse_tree]
            # -The Transformer object is provided as parameter to the LALR parser
            #   * The parse tree is not generated
            #   * The transformer methods are applied when generating the nodes
            #   * The most efficient solution since the methods are called instead of
            #     generating the tree nodes (actions are excuted when reductions are applied)
            '''Numeric constants are passed from [call_tree] as an additional parameters to the transformer class'''
            Numeric_constants = call_tree.children[0].children[1].children
            param = func_def.children[1].children
            eval_tree = FunctionTransformer( Numeric_constants , param).transform(parse_tree)
        
            print("\t\t ==> Result of function call:\t",eval_tree.children[0])           

        except UnexpectedToken as error:
            print("\t### ERROR: Unexpected token %s" % error.token)
            print(error.get_context(code2))  
        except UnexpectedInput as error:
            print("\t### ERROR: Parser error!")
            print(error.get_context(code2))
        except Exception as error:
            print(error)
    print("\t\t ==> Program Finished!")

if __name__ == '__main__':
    main()

  
  



