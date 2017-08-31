import sys
import re
import lexer

lexemes = ["=", "+", "-", "*", "/", "^", "(", ")",
           "[", "]", ",", ":"]

unvariedLexemes = ["var", "function", "return", "print", "=", "+",
                   "-", "*", "/", "^", "(", ")", "{", "}", ",", ":"]

unvariedToken = ["VAR", "FUNCTION", "RETURN", "PRINT", "ASSIGN", "ADD",
                 "SUB", "MULT", "DIV", "EXP", "LPAREN", "RPAREN", "LBRACE",
                 "RBRACE", "COMMA", "COLON"]

'''
Splits the source list by element then uses regex
to put spaces before and after unvaried lexemes
'''
def SplitByUnvariedLexemes(source):
    allSplits = []
    for line in source:
        thisSplit = re.sub('([\\+\\-*/.,!?()\\{\\}])', r' \1 ', line)
        thisSplit = re.sub('\s{2,}', ' ', thisSplit)
        allSplits.append(thisSplit)
        return allSplits

'''
Takes formatted list from SplitByUnvariedLexemes
and splits it by whitespace.
'''
def SplitSourceByWhitespace(source):
    allSplits = []
    for line in source:
        thisSplit = line.split()
        allSplits.append(thisSplit)
    return allSplits

#Takes formatted list from SplitSourceByWhitespace and begins tokenizing.
def assignTokens(source):
    allSplits = []
    for x in source:
        for item in x:
            try:
                success = unvariedLexemes.index(item)
            except ValueError:
                success = -1
            #If success returned an index, fetches appropriate token. 
            if(success != -1):
                token = unvariedToken[success]
                allSplits.append(token)
            #Checks if type NUMBER, if not must be type IDENT.  
            if (success == -1):
                try:
                    float(item)
                    token = "NUMBER:" + item
                    allSplits.append(token)
                except ValueError:
                    token = "IDENT:" + item
                    allSplits.append(token)
        allSplits.append("EOF")
        print(allSplits)
        return allSplits


if __name__ == '__main__':
    print ("starting __main__")
    #while((line=sys.stdin.readlines() != null)){}
    assignTokens(SplitSourceByWhitespace(SplitByUnvariedLexemes(sys.stdin.readlines())))
    '''
    } On windows I found sys.stdin only takes one line, 
    the while loop fixes this
    '''