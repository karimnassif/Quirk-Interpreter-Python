from __future__ import print_function
import sys
import pprint


pp = pprint.PrettyPrinter(indent=1, depth=100)

#start utilities

def eprint(msg):
    print(msg, file=sys.stderr)

def lookup_in_scope_stack(name, scope):

    if name in scope:
        return scope[name]
    else:
        if "__parent__" in scope:
            return lookup_in_scope_stack(name, scope["__parent__"])

def get_name_from_ident(tok):
    colon_index = tok.find(":")
    return tok[colon_index+1:]

def get_number_from_ident(tok):
    colon_index = tok.find(":")
    return float(tok[colon_index+1:])

def func_by_name(*args):
    name = args[0]
    pt = args[1]
    scope = args[2]

    returnval = globals()[name](pt, scope)
    #eprint("calfunc_by_name()) " + name + " " + str(returnval))
    return returnval
#end utilities

# <Program> -> <Statement> <Program> | <Statement>
def Program0(pt, scope):
    statement_run=func_by_name(pt[1][0],pt[1],scope)
    program_run=func_by_name(pt[2][0],pt[2],scope)

def Program1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

def Statement1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

def Statement2(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

# <FunctionDeclaration> -> FUNCTION <Name> PAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
def FunctionDeclaration0(pt, scope):
    function_name = func_by_name(pt[2][0],pt[2],scope)
    real_name = function_name[1]
    param_list = func_by_name(pt[4][0], pt[4], scope)
    function_body = pt[6]
    total_list = param_list + function_body
    scope[real_name]=total_list

# <FunctionParams> -> <NameList> RPAREN | RPAREN
# should return a list of values
def FunctionParams0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

def FunctionParams1(pt, scope):
    return []

# <FunctionBody> -> <Program> <Return> | <Return>
def FunctionBody0(pt, scope):
    func_by_name(pt[1][0],pt[1],scope)
    return func_by_name(pt[2][0],pt[2],scope)
    
def FunctionBody1(pt, scope):
    return func_by_name(pt[1][0],pt[1],scope)

# <Return> -> RETURN <ParameterList>
def Return0(pt, scope):
    scope[function_name] = func_by_name(pt[2][0],pt[2],scope)


# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(pt, scope):
    return func_by_name(pt[1][0],pt[1],scope)

def Assignment1(pt, scope):
    return func_by_name(pt[1][0],pt[1],scope)

# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment0(pt, scope):
    var_name=get_name_from_ident(pt[2])
    value=func_by_name(pt[4][0])
    if(name in scope):
        print(name +" is already defined.")
        return -1
    scope[var_name]=value

# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment0(pt, scope):
    name_list = NameList(pt[2], scope)
    values=FunctionCall(pt[4], scope)
    if(name_list.length()!=values.length()):
        print("Wrong number of values")
        return -1
    for name in name_list:
        if name in scope:
            print("Variable already defined")
            return -1
    #Second for statement to ensure no rebinding when there is an error.
    for x in xrange(name_list.length()):
        scope[name]=value[x]
    
# <Print> -> PRINT <Expression>
def Print0(pt, scope):
    print(str(func_by_name(pt[2][0], pt[2], scope)))

# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(pt, scope):
    param_name = func_by_name(pt[1][0], pt[1], scope)[1]
    return [param_name] + func_by_name(pt[3][0], pt[3], scope)

def NameList1(pt, scope):
    #getting the [1] of the return value for name as it returns a [val, name]
    return [func_by_name(pt[1][0], pt[1], scope)[1]]

# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
def ParameterList0(pt, scope):
    param=func_by_name(pt[1][0],pt[1],scope)
    return param+func_by_name(pt[3][0],pt[3],scope)

def ParameterList1(pt, scope):
    print("parameterlist1")
    return func_by_name(pt[1][0], pt[1], scope)

# <Parameter> -> <Expression> | <Name>
def Parameter0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

def Parameter1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)[0]

# VAR <Name> ASSIGN <Expression>
def SingleAssignment0(pt, scope):
    return_list = func_by_name(pt[2][0],pt[2],scope)
    return_list.pop(0)
    var_name=return_list.pop(0)
    value = func_by_name(pt[4][0],pt[4],scope)
    if(var_name in scope):
        print(var_name+" already a variable.")
        return -1
    scope[var_name]=value
    

#<Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
def Expression0(pt, scope):
    #<Term> ADD <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value + right_value

def Expression1(pt, scope):
    #<Term> SUB <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value - right_value

def Expression2(pt, scope):
    #<Term>
    return func_by_name(pt[1][0], pt[1], scope)

#<Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(pt, scope):
    left_value=func_by_name(pt[1][0], pt[1], scope)
    right_value=func_by_name(pt[3][0], pt[3], scope)
    return left_value*right_value

def Term1(pt, scope):
    left_value=func_by_name(pt[1][0], pt[1], scope)
    right_value=func_by_name(pt[3][0], pt[3], scope)
    return left_value/right_value

def Term2(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

#<Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
def Factor0(pt, scope):
    left_value=func_by_name(pt[1][0], pt[1], scope)
    right_value=func_by_name(pt[3][0], pt[3], scope)
    return left_value^right_value

def Factor1(pt, scope):
    return func_by_name(pt[1][0],pt[1],scope)

def Factor2(pt, scope):
    #returns multiple values -- use the first by default.
    return func_by_name(pt[1][0],pt[1],scope)[1]

def Factor3(pt, scope):
    left_value=func_by_name(pt[1][0],pt[1],scope)
    return left_value^func_by_name(pt[3][0],pt[3],scope)

def Factor4(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


#<FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(pt, scope):
    #Retrieves function name and scope, adds old scope as parent.
    func_name = pt[1]
    new_scope={}
    local_info=scope[func_name]
    new_scope[__parent__] = scope
    #Retrieves param list and values
    param_list=local_info[0]
    param_values = func_by_name(pt[3][0],pt[3],scope)
    #Binds params and values
    for x in xrange(param_list.length()):
        new_scope[param_list[x]] = param_values[x]  
    return_list = func_by_name(local_info[1][0],local_info[1], new_scope)
    #Checks for index overload then returns index of returned value list.
    if(pt[5]>return_list.length()):
        print("Return index too large. (Gave "+p[5]+", limit is "+return_list.lenght())
        return -1
    return return_list[pt[5]]

def FunctionCall1(pt, scope):
    #Exact same procedure as above function, without the index steps. 
    func_name = pt[1]
    new_scope={}
    new_scope[__parent__] = scope
    param_list=scope[func_name][0]
    param_values = func_by_name(pt[3][0],pt[3],scope)
    for x in xrange(param_list.length()):
        new_scope[param_list[x]] = param_values[x]  
    return func_by_name(scope[function_name[1][0]],scope[function_name[1]], new_scope)

#<FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
def FunctionCallParams0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

def FunctionCallParams1(pt, scope):
    return[]

#<SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression0(pt, scope):
    return -1

#<Value> -> <Name> | <Number>
def Value0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)[0]

def Value1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)

#<Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(pt, scope):
    name = get_name_from_ident(pt[1])
    return [lookup_in_scope_stack(name, scope), name]

def Name1(pt, scope):
    name = get_name_from_ident(pt[2])
    return [-lookup_in_scope_stack(name, scope), name]

def Name2(pt, scope):
    name = get_name_from_ident(pt[2])
    return [lookup_in_scope_stack(name, scope), name]

#<Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(pt, scope):
    return get_number_from_ident(pt[1])

def Number1(pt, scope):
    return -get_number_from_ident(pt[2])

def Number2(pt, scope):
    return get_number_from_ident(pt[2])

#var x =5, var y=10, print x*y
e1tree = ['Program0', ['Statement1', ['Assignment0', ['SingleAssignment0', 
'VAR', ['Name0', 'IDENT:X'], 'ASSIGN', ['Expression2', ['Term2', ['Factor4',
 ['Value1', ['Number0', 'NUMBER:5']]]]]]]], ['Program0', ['Statement1', 
 ['Assignment0', ['SingleAssignment0', 'VAR', ['Name0', 'IDENT:Y'], 
 'ASSIGN', ['Expression2', ['Term2', ['Factor4', ['Value1', 
 ['Number0', 'NUMBER:10']]]]]]]], ['Program1', ['Statement2', 
 ['Print0', 'PRINT', ['Expression2', ['Term0', ['Factor4', ['Value0', 
 ['Name0', 'IDENT:X']]], 'MULT', ['Term2', ['Factor4', ['Value0', ['Name0', 'IDENT:Y']]]]]]]]]]]

if __name__ == '__main__':
    #choose a parse tree and initial scope
    tree = e1tree
    scope = {}
    #execute the program starting at the top of the tree
    func_by_name(tree[0], tree, scope)
    #Uncomment to see the final scope after the program has executed.
    pp.pprint(scope)