# lark_parser-scanner
A parser/scanner implementation for the definition of functions using Lark library in Python.
Includes Grammar and the Transformer class implementation to process the input.

Libraries to be installed:
- Lark
- Pydot

Files handed in this email:
- __init__.py (main)
- Function.png (example: graphical representation of the function definition tree)
- Function2.png (example: graphical representation of the function calling tree)
- Execution_example.txt (Example of a run of the script)

    INSTRUCTION FOR FUNCTION DEFINITION:
     The functions should be defined as follows:
   
      function name(par1,par2,…) {
         return par1 op par2 op par3…;
      }
   
     - Where name is the function name with the usual restrictions (an alphanumeric string beginning with a letter).
     - par1.. are the function parameters whose names follow the same rules as variable names.
     - op is + or * (sum or product).
     - The function body contains only the return instruction that involves all the parameters.
     - Only one function can be defined.
     - The program is implemented in a do-while-like way, breaking when the function is well-defined.
     - Exception handling has been implemented.

==> Example of the function definition:        
    function F1( a, b , c , d , e ) { return b * a + e * d + c ; }     

    INSTRUCTION FOR FUNCTION CALLING:
     Function call syntax:    
      name(cost1,cost2,…);
   
     - Where name is the name of a defined function.
     - cost1,… are numeric constants in the same
       number as the function arguments.

==> Example:
>>> Please enter the function calling: F1( -1.6 , 0 , 1 , 2 , 3 );
==> Result of function call: 7.0

- The program is implemented in a do-while-like way, breaking when the word "stop" is entered.
- Exception handling has been implemented.
- A Transformer object is created.
- The transform() method is called on the tree resulting from parsing [parse_tree].
- The Transformer object is provided as a parameter to the LALR parser.
   * The parse tree is not generated.
   * The transformer methods are applied when generating the nodes.
   * The most efficient solution since the methods are called instead of generating the tree nodes (actions are executed when reductions are applied).
 - An additional tree is generated with a second grammar [call_tree] for the function calls.
 - Numeric constants are passed from [call_tree] as an additional parameter to the transformer class called on the tree resulting from parsing [parse_tree].
 - The decorator should be used to specify the number of arguments expected by the methods, including the 'self' parameter.
 - In the case of methods with a 'self' parameter, you need to account for it when specifying the arguments for the decorator.
