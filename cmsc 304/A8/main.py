import sys

def main():
    if len(sys.argv) != 3:
        print("usage: python tokenizer.py <input> <output>")
        sys.exit(0)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r") as f:
        text = f.read()

    # ... process text into tokens ...

    with open(output_path, "w") as f:
        for token, lexeme in tokens:
            f.write(f"{token} {lexeme}\n")

if __name__ == "__main__":
    main()