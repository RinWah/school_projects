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
        return RESERVED[lexeme]

    # for the decently harder cases
    # like numbers
    if lexeme[0].isdigit() and all(ch.isdigit() for ch in lexeme):
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
                # if the character is space, then clear the placeholder
                # and move onto the next character
                if ch.isspace():
                    placeholder = flush_placeholder(placeholder, lexemes)
                    i+=1
                    continue
                # if the char is a letter or digit, then just simply add
                # that letter/digit to the placeholder value and continue on
                # to the next character in the string.
                if ch.isalpha() or ch.isdigit():
                    placeholder += ch
                    i+=1
                    continue
                # clear any preexisting strings in our placeholder variable
                placeholder = flush_placeholder(placeholder, lexemes)
                # catches any multi piece symbol like == or !=
                if ch == "=":
                    # check next char
                    if i + 1 < n and line[i + 1] == "=":
                        lexemes.append("==")
                        i+=2
                    else:
                        lexemes.append("=")
                        i+=1
                    continue
                if ch == "!":
                    if i+1<n and line[i+1] == "=":
                        lexemes.append("!=")
                        i+=2
                    else:
                        # if it is actually by itself, then just treat it like
                        # it's singular, doesn't really make sense for ! 
                        # but consistency makes sense, right? 
                        # cause like = is asssignment lol
                        lexemes.append("!")
                        i+=1
                    continue
                # all the other simple symbols like * or modulo
                if ch in "(){}+*%,;":
                    lexemes.append(ch)
                    i+=1
                    continue
                # other cases, just in case i missed one of them
                # no chars left behind!
                # glory to the chars
                lexemes.append(ch)
                i+=1

    # clear any remaining placeholder text when we reach the end of the 
    # preexisting line of code
    placeholder = flush_placeholder(placeholder, lexemes)
    return lexemes

def main():
    # make sure user inputted the three necessary files
    if len(sys.argv) != 3:
        print("you need: tokenizer file, input file, and output file")
        # don't actually run it lol
        sys.exit(0)
# new names b/c it's easier
    input_path = sys.argv[1]
    output_path = sys.argv[2]
#run the tokenize file function on the input file
    lexemes=tokenize_file(input_path)
# write into the output file the results of the categorized values
    with open(output_path, "w") as out:
        for lexeme in lexemes:
            token=classifier(lexeme)
            out.write(f"{token} {lexeme}\n")

# if only one file is inputted, aka the main file, then just run what's in that
if __name__ == "__main__":
    main()

