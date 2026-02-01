"""
CMSC 437 | PA1
ELIZA (psychotherapist machine)

Rin Pereira
Due Date: 2/2/26

Problem: Conversating with a human patient in a psychotherapy setting.
ie. How are you feeling?
ie. I'm feeling sad.
ie. Why are you feeling sad?
etc etc.

Algorithm:
* basically read in what the user says
* match it with any keywords in a while True loop
* if it matches, output that value
* ^ if it doesn't match, have a placeholder phrase like "can you say that in a different way" or refer back to a previous conversation [ELIZA goal in
the past]
* keep going and let the user be able to quit anytime by saying bye or quit
"""

# import in reader from python
import re
# for randomized responses
import random

# little translation thing like ELIZA where you flip I'm into you are etc.
def reflect(text):
    # replacements
    swap = [
        (r"\bmy\b", "your"),
        (r"\byour\b", "my"),
        (r"\bme\b", "you"),
        (r"\byou\b", "me"),
        (r"\bi\b", "you"),
        (r"\bam\b", "are"),
        (r"\bare\b", "am")
    ]
    # take the original user input
    out = text
    # go through each pair of personal pronouns from swap list
    for pattern, repl in swap:
        # replace any matches [ie. my becomes your, me -> you, etc.]
        out = re.sub(pattern, repl, out, flags=re.IGNORECASE)
    # final sentence after swapping pronouns
    return out

def main():
    # opening
    print("-> [eliza] hi, i'm a psychotherapist, what is your name?")
    user_input = input("=> [user] ").strip()

    # get user name from input
    m = re.match(r"^\s*my\s+name\s+is\s+([A-Za-z]+)\.?\s*$", user_input, re.IGNORECASE)
    a = re.match(r"^\s*([A-Za-z]+)\.?\s*$", user_input, re.IGNORECASE)
    # if it's just them saying their name, read it in or if they say something like my name is, read what's after that
    if m:
        name = m.group(1)
    elif a:
        name = a.group(1)
    else:
        # if you can't read in the name, just say like hey there lol
        name = "anonymous"

    # ask user what ELIZA can do for them
    print(f"-> [eliza] hi {name}. how can i help you today?")

    last_thing = None
    # adding this so there's variation in the code when ELIZA doesn't get what the user is trying to say
    incomprehension = [
        "i don't understand, can you try rephrasing that?",
        "can you tell me more about that?",
        "that's interesting, what are you thinking about in respect to this?",
        "how does that make you feel?",
        "hmm, let's dissect it. what part feels the most overwhelming?"
    ]

    while True:
        user_input = input(f"=> [{name}] ").strip()

        # backup thing for name in case you want to change your name later
        m = re.match(r"^\s*(?:my\s+name\s+is|call\s+me)\s+([A-Za-z]+)\.?\s*$", user_input, re.IGNORECASE)
        random_number = random.randint(1,2)
        if m:
            name = m.group(1)
            if random_number == 1:
                print(f"-> [eliza] {name} it is!")
                continue
            if random_number == 2:
                print(f"-> [eliza] i'll call you {name} from now on.")
                continue


        # idk, response in case the user doesn't know what to say, ELIZA will redirect and continue conversation
        # i made it full match so it doesn't identify a sentence like idk but maybe [like user thinking about something further]
        if re.fullmatch(r"\b(idk|i don't know)\b", user_input, re.IGNORECASE):
            if last_thing:
                print(f"-> [eliza] earlier you mentioned {last_thing}. let's talk about that more.")
            else:
                print(f"-> [eliza] hmm, it's alright then. what have you been thinking about lately?")
            continue

        # case for if the patient/human i guess says stuff like i always forget or something since that's like self detrimenting [not sure if that's the right word]
        if re.search(r"\b(always|never)\b", user_input, re.IGNORECASE):
            print("-> [eliza] hey. be more gentle on yourself. do you believe it's an issue?")
            continue

        # case for yes/no responses since she's not that sophisticated
        if re.fullmatch(r"\s*(yes|yeah)\s*", user_input, re.IGNORECASE):
            print("-> [eliza] what makes you say yes?")
            continue

        if re.fullmatch(r"\s*(no|nope)\s*", user_input, re.IGNORECASE):
            print("-> [eliza] why not?")
            continue

        # chats with dream in it
        if re.search(r"\b(dream|dreamed|nightmare)\b", user_input, re.IGNORECASE):
            responses = [
                "do you usually have dreams like that?",
                "do you think the dream had a deeper meaning?",
                "how did you feel about the dream?"
            ]
            # kinda realized i could just use random like this instead of just generating a number and choosing it, i'm going to change the other ones now
            print(f"-> [eliza] {random.choice(responses)}")
            continue

        # case for because
        m = re.search(r"\bbecause\b\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            reason = reflect(m.group(1))
            # i had it incorporate context before, but it was reflecting oddly so i changed it to just these generic responses instead
            responses = [
                "how long has that been bothering you?",
                "what about that feels most upsetting?",
                "how does that make you feel?",
                "why do you think that happened?"
            ]
            print(f"-> [eliza] {random.choice(responses)}")
            last_thing = reason
            continue

        # case for i need
        m = re.match(r"^\s*i\s+need\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(1)
            print(f"-> [eliza] why do you need {rest}?")
            last_thing = rest
            continue

        # case for i'm afraid of
        # forgot the \s after of and it was reading it in with weird spacing, adding \s to end of of\s makes sure it doesn't.
        m = re.match(r"^\s*i'm\s+afraid\s+of\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        n = re.match(r"^\s*i\s+am\s+afraid\s+of\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m or n:
            # set match to the matched keyword from the re.match ^
            match = m if m else n
            # set that value or whatever the user says they are scared of into rest variable
            rest = match.group(1)
            print(f"-> [eliza] why are you afraid of {rest}?")
            last_thing = rest
            continue

        # case for i'm afraid of part too but instead it's _ something scares me
        m = re.match(r"^\s*(.+?)\s+scares\s+me\.?\s*$", user_input, re.IGNORECASE)
        n = re.match(r"^\s*(.+?)\s+scare\s+me\.?\s*$", user_input, re.IGNORECASE)
        if m or n:
            match = m if m else n
            rest = match.group(1)
            print(f"-> [eliza] what about {rest} scares you?")
            last_thing = rest
            continue

        # case for i miss
        m = re.match(r"^\s*i\s+miss\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(1)
            print(f"-> [eliza] why do you miss {rest}?")
            last_thing = rest
            continue

        # case for when user asks ELIZA a question
        # \?\s*$ = looks for a question mark at end of input
        # ^\s*() = starts with one of those words [ie. why, what, how]
        if re.search(r"\?\s*$|^\s*(why|what|how|can|should|do|did|is|are|am)\b", user_input, re.IGNORECASE):
            # generate random number and then use that to choose a response?
            responses = ["what do you think?", "why do you ask?", "how would you answer that yourself?"]
            print(f"-> [eliza] {random.choice(responses)}")
            continue

        # case for when user is trying to actually get some help
        if re.search(r"^\s*help(\s+me)?\b", user_input, re.IGNORECASE):
            print(f"-> [eliza] i am only a mere chatbot with limited knowledge. please seek real human assistance.")
            continue

        # stop, when user wants to leave
        if re.search(r"\b(quit|exit|bye)\b", user_input, re.IGNORECASE):
            print(f"-> [eliza] Goodbye, {name}.")
            break

        # implementation for reflecting user projection lol part 1
        m = re.match(r"^\s*you\s+are\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(1)
            print(f"-> [eliza] what makes you think i am {rest}?")
            last_thing = rest
            continue

        # implementation for reflecting user project part 2
        m = re.match(r"^\s*you\s+make\s+me\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(1)
            print(f"-> [eliza] why do you think i make you {rest}?")
            last_thing = rest
            continue

        # implementation for i can't
        # i originally wrote this like if m and if random_number = # but then realized i could do it like this lol
        m = re.match(r"^\s*i\s+(can't|cannot|cant)\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(2)
            last_thing = rest
            responses = [
                f"what makes you think you can't {rest}?",
                f"why do you think you can't {rest}?"
            ]
            print(f"-> [eliza] {random.choice(responses)}")
            continue

        # base for rule the world
        m = re.match(r"^\s*i\s+want\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(1)
            print(f"-> [eliza] {name}, why do you want {rest}?")
            last_thing = rest
            continue

        # implementation for i like and i love and i hate
        m = re.match(r"^\s*i\s+(like|love|hate)\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            feeling = m.group(1)
            subject = m.group(2)
            last_thing = subject
            # i changed this to f strings so that it actually subs in what i wanted it to, oops
            responses = [
                f"what do you {feeling} about {subject}?",
                f"what makes you {feeling} {subject}?"
            ]
            print(f"-> [eliza] {random.choice(responses)}")
            continue

        # implementation for i think
        m = re.match(r"^\s*i\s+think\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = reflect(m.group(1))
            last_thing = rest
            print(f"-> [eliza] why do you think {rest}?")
            continue

        # implementation for i am statements
        # i'?m = i then optional ' and m
        # accepts im too
        # (?: ) = group but don't store
        m = re.match(r"^\s*(?:i\s+am|i'?m)\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(1)
            print(f"-> [eliza] how long have you been {rest}?")
            last_thing = rest
            continue

        # implementation for i feel
        m = re.match(r"^\s*i\s+feel\s+(.+?)\.?\s*$", user_input, re.IGNORECASE)
        if m:
            rest = m.group(1)
            print(f"-> [eliza] why do you feel {rest}?")
            last_thing = rest
            continue

        # implementation for talking about school
        if re.search(r"\b(school|class|homework|exam|grade|grades)\b", user_input, re.IGNORECASE):
            responses = ["how has school been going lately?",
                         "what part of school makes you feel overwhelmed?",
                         "do you feel unhappy about your grades?"]
            print(f"-> [eliza] {random.choice(responses)}")
            continue

        # implementation for talking about anxiety or stress
        if re.search(r"\b(stress|stressed|anxious|anxiety|worried|nervous)\b", user_input, re.IGNORECASE):
            responses = ["what do you think causes your stress?",
                         "when did these feelings begin?",
                         "what do you do after you feel anxiety and stress?"]
            print(f"-> [eliza] {random.choice(responses)}")
            continue

        # base for crave for power
        if re.search(r"\bcrav(e|es|ed|ing)\b", user_input, re.IGNORECASE):
            print("-> [eliza] Why don't you tell me more about your cravings.")
            continue

        # if user input is gibberish
        # i need variation lol
        print(f"-> [eliza] {random.choice(incomprehension)}")

if __name__ == "__main__":
    main()
