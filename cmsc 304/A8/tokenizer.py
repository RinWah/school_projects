import sys

# tokens to lexemes
RESERVED = {
    "(": "LEFT_PARENTHESIS",
    ")": "RIGHT_PARENTHESIS",
    "{": "LEFT_BRACKET",
    "}": "RIGHT_BRACKET",
    "while": "WHILE_KEYWORD",
    "return": "RETURN_KEYWORD",
    "=": "EQUAL",
    ",": "COMMA",
    ";": "EOL", # end of line
    "int": "VARTYPE",
    "void": "VARTYPE",
    "+": "BINOP",
    "*": "BINOP",
    "!=": "BINOP",
    "==": "BINOP",
    "%": "BINOP",
}

def classifier(lexeme: str) -> str:
    # take the given lexeme [str] & return it's token
    # aka taken a str value, return it's data type in this
    # use case
    # ie. input -> =
    # ie. output -> EQUAL
    if lexeme in RESERVED: # for the simple cases
        return RESERVERD[lexeme]

    # for the decently harder cases
    # like numbers
    if lexeme[0].isDigit() and all(ch.isDigit() for ch in lexeme):
        return "NUMBER"
    # if it's not a reserved word or a number, it's safe to 
    # assume it might be a variable name or something.
    return "IDENTIFIER"

#helper function for tokenize_file() aka right below this one
# function to hold strings while reading to the next space _
def flush_placeholder(placeholder, lexemes):
    if placeholder:
        lexemes.append(placeholder)
        return ""
    return placeholder

# function to convert input file into just a list of values
def tokenize_file(input_path: str) -> list[str]:
    # read input file & output list of values in order.
    lexemes: list[str] = []
    placeholder = ""

    # open file input_path when finding r and start reading there
    with open(input_path, "r") as f:
        # for this line in the file
        for line in f:
            # we set i to 0
            i = 0
            # n to the length of the line
            n = len(line)
            # while our place is less than the length of the line
            while i < n:
                # start our first element in the line
                ch = line[i]
                # BOOKMARKED!
                if ch.isspace():
                    flush_placeholder()
                    i+=1
                    continue

