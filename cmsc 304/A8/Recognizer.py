import sys

# keep track of the tokens within a list
TOKENS: list[tuple[str, str]] = []
# counter for index of string
CURRENT_INDEX: int = 0
# output placeholder
OUTPUT_PATH: str = ""

# denotes whether or not placement of code is legal or illegal
FIRST_HEADER = {"VARTYPE"}
FIRST_BODY = {"LEFT_BRACKET"}
FIRST_STATEMENT = {"WHILE_KEYWORD", "RETURN_KEYWORD", "IDENTIFIER"}
FIRST_ARG_DECL = {"VARTYPE"}
FIRST_TERM = {"IDENTIFIER", "NUMBER"}

# detect if current token type is a string or not
def current_token_type() -> str | None:
    # conditional to make sure index is within number of tokens, not out of bounds
    if CURRENT_INDEX < len(TOKENS):
        # returns current index of TOKENS we are on if it is a string
        return TOKENS[CURRENT_INDEX][0]
    # return nothing if it's not a string
    return None

# function to tell the user the expected anad actual result error of tokenizing
def error_token(rule_name: str, expected: str, actual: str | None) -> None:
    # if the actual token exists, use it, otherwise just assume it's ;
    actual_name = actual if actual is not None else "EOF"
    # start counting by one so it makes sense to the user so they don't have to 
    # start counting from 0
    token_number = CURRENT_INDEX + 1
    # let the user know what happened
    msg = (
        f"Error: In grammar rule {rule_name}, expected token #{token_number} "
        f"to be {expected} but was {actual_name}"
    )
    # open the output file
    with open(OUTPUT_PATH, "w") as out:
        # reiterate error message into output file
        out.write(msg + "\n")
    # stop the program since the error must be resolved first.
    sys.exit(0)

# error message to user when the grammar rule is too short
def error_nonterminal(rule_name: str, nonterminal: str) -> None:
    # give user feedback
    msg = (
        f"Error: In grammar rule {rule_name}, expected a valid {nonterminal} "
        f"non-terminal to be present but was not"
    )
    # write into output file
    with open(OUTPUT_PATH, "w") as out:
        # write error message into output
        out.write(msg + "\n")
    # stop the program since the error must be resolved first. 
    sys.exit(0)

# error message if all the tokens are not used, aka the grammar is way too long
# to be valid
def error_unconsumed_tokens() -> None:
    # consumed stores the amount of tokens that are already eaten
    consumed = CURRENT_INDEX
    # stores the number of tokens given to the program
    total = len(TOKENS)
    # tell the user how many were used and how many were in total given
    msg = f"Error: Only consumed {consumed} of the {total} given tokens"
    # write to output file 
    with open(OUTPUT_PATH, "w") as out:
        out.write(msg + "\n")
    # stop the program since the error must be resolved first. 
    sys.exit(0)

# helper function that verifies grammar validity
def expect(expected_token: str, rule_name: str) -> None:
    # reassign current index
    global CURRENT_INDEX
    # what token we are looking at
    actual = current_token_type()
    # compare what should be there and what isn't, almost like autocorrect
    if actual != expected_token:
        # if the wrong token is there, stop the program
        error_token(rule_name, expected_token, actual) 
    # if everything is gud, continue to the next token
    CURRENT_INDEX += 1
    
# read entire function and verify validity
def parse_function() -> None:
    # look at first token and verify it's a header
    if current_token_type() not in FIRST_HEADER:
        # if it isn't, then run the error and tell the user
        error_nonterminal("function", "header")
    # otherwise parse the header and continue on
    parse_header()
    # after the header, make sure the next token is the start of body code
    if current_token_type() not in FIRST_BODY:
        # if it isn't, then run the error and tell the user
        error_nonterminal("function", "body")
    # otherwise parse the body and continue on
    parse_body()

# function that validates function header is formatted right
def parse_header() -> None:
    # expect vartype, identifier, parenthesis and then an argument (maybe) and 
    # then another parenthesis
    # ie. int foo() would be vartype, identifier and then parenthesis
    # ^ does not include args, but could also be int foo(int num)
    expect("VARTYPE", "header")
    expect("IDENTIFIER", "header")
    expect("LEFT_PARENTHESIS", "header")

    if current_token_type() in FIRST_ARG_DECL:
        # for arguments if there are any
        parse_arg_decl()
    expect("RIGHT_PARENTHESIS", "header")

# helperish function to help read function header declarations
# like temp variables and whatnot
# ie from above, int foo(int num, int frequency)
# would ofc keep looping as long as there are more than one, otherwise
# would just run once
def parse_arg_decl() -> None:
    expect("VARTYPE", "arg-decl")
    expect("IDENTIFIER", "arg-decl")

    while current_token_type() == "COMMA":
        expect("COMMA", "arg-decl")
        expect("VARTYPE", "arg-decl")
        expect("IDENTIFIER", "arg-decl")

# parse body statement
def parse_body() -> None:
    # expect { for opening part
    expect("LEFT_BRACKET", "body")
    # if it is, parse the statement
    if current_token_type() in FIRST_STATEMENT:
        parse_statement_list()
    # if not expect the end of the body }
    expect("RIGHT_BRACKET", "body")

# ensures there is at least one statement in a list of statements to parse
def parse_statement_list() -> None:
    # read one statement
    parse_statement()
    # if there are more, continue parsing those as well
    while current_token_type() in FIRST_STATEMENT:
        parse_statement()
    
# parses the statement as either a while, return, or identifier, otherwise
# maybe it's a statement list or one singular statement and not
# otherwise return error message
def parse_statement() -> None:
    # check if it's a while
    t = current_token_type()
    if t == "WHILE_KEYWORD":
        parse_while_loop()
    # check if it's a return
    elif t == "RETURN_KEYWORD":
        parse_return()
    # check if it's an identifier
    elif t == "IDENTIFIER":
        parse_assignment()
    else:
        # run that error message to the user
        error_nonterminal("statement-list", "statement")

# basically parse a while loop
def parse_while_loop() -> None:
    # start with while keyword
    expect("WHILE_KEYWORD", "while-loop")
    # then open parenthesis
    expect("LEFT_PARENTHESIS", "while-loop")
    # then your expression with it's args and everything
    parse_expression()
    # then close your opening parenthesis
    expect("RIGHT_PARENTHESIS", "while-loop")
    # check to make sure next part looks like the body statement
    if current_token_type() not in FIRST_BODY:
        # if it's not, run an error
        error_nonterminal("while-loop", "body")
    # if it's fine, then parse it as usual
    parse_body()

# parse return statement
def parse_return() -> None:
    # we expect a return keyword
    expect("RETURN_KEYWORD", "return")
    # parse it
    parse_expression()
    # we also expect a ;
    expect("EOL", "return")

# parse asignment statements
def parse_assignment() -> None:
    # we expect the name of the variable
    expect("IDENTIFIER", "assignment")
    # followeed by an equal sign
    expect("EQUAL", "assignment")
    # parse the expression
    parse_expression()
    # after that we expect the ;
    expect("EOL", "assignment")

# parse expressions [mainly mathematical]
def parse_expression() -> None:
    # see what next word is
    t = current_token_type()
    # check for left parenthesis
    if t == "LEFT_PARENTHESIS":
        expect("LEFT_PARENTHESIS", "expression")
        # if it has () parse it
        parse_expression()
        expect("RIGHT_PARENTHESIS", "expression")
        return
    if t not in FIRST_TERM:
        # if it didn't begin with ( give error
        error_nonterminal("expression", "term")
    # otherwise continue as usual
    parse_term()
    # if it's a binary operation
    while current_token_type() == "BINOP":
        # we expect it 
        expect("BINOP", "expression")
        # if it's not
        if current_token_type() not in FIRST_TERM:
                # return error to user
                error_nonterminal("expression", "term")
        parse_term()

# parse variable name and number
def parse_term() -> None:
    # look at next char
    t = current_token_type()
    # if it's a variable name
    if t == "IDENTIFIER":
        expect("IDENTIFIER", "term")
    # if it's a number
    elif t == "NUMBER":
        expect("NUMBER", "term")
    # otherwise just run error, should have been caught earlier
    else:
        # just in case it wasn't caught earlier, less likely tho
        error_nonterminal("term", "term")

# main func
def main(): 
    global TOKENS, CURRENT_INDEX, OUTPUT_PATH
    # should get input and output
    if len(sys.argv) != 3:
        # explains to user how to input stuff in order
        print("usage: python recognizer.py <input_file> <output_file")
        # stop the program if the user didn't put enough files in
        sys.exit(0)
        # get input file
    input_path = sys.argv[1]
    # set output file
    OUTPUT_PATH = sys.argv[2]
    # restart token list in case it isn't empty already
    TOKENS=[]
    # open input file to read it
    with open(input_path, "r") as f:
        # read file
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 1)
            token = parts[0]
            lexeme = parts[1] if len(parts) > 1 else ""
            TOKENS.append((token, lexeme))
    # read tokens from beginning of index list
    CURRENT_INDEX = 0
    # if there are nothing to read
    if not TOKENS:
        # return error saying there's nothing there, not even a function
        error_nonterminal("function", "header")
    # parse function
    parse_function()
    # ensure everything inside the input file was used
    if CURRENT_INDEX != len(TOKENS):
        # if there are still ones left, return an error to the user
        error_unconsumed_tokens()
    # open the output file
    with open(OUTPUT_PATH, "w") as out:
        # since we successfully read the input file, return the good news to the 
        # user
        out.write("PARSED!!!\n")
# just in case the file is just run by itself like run main onlly, we have
# that written in just in case. 
if __name__ == "__main__":
    main()