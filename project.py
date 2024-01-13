
import re
import sys
from collections import Counter
from dateutil import parser
from email_validator import validate_email, EmailNotValidError


def main():
    find = input_test()
    with open(sys.argv[1], "r") as file:
        lines: list[str] = file.readlines()
        file.seek(0)  # moves caret at the beginning
        words: str = file.read()

    # count number of lines
    number_of_lines: int = count_lines(lines)

    # count number of words
    number_of_words: int = count_words(words)

    # count number of character
    number_of_car: int = count_car(words)

    # count blank lines
    blank_lines: int = count_blank_lines(lines)

    # extract more frequent words
    freq_words_list = frequent_words(words)

    # Extract dates found in txt
    dates = extract_dates(words)
    if type(dates) == list:
        dates = "\n".join(dates)
        dates = (f'''Dates found in file:
{dates}''')

    # Extract email found in txt
    email = extract_email(words)
    if type(email) == list:
        email = "\n".join(email)
        email = f'''Email address(es) found in file:
{email}'''

    # search how many times a specified words (1 or more) occurs
    if find:
        occurrences = search_word(words, find)
        out = f"The word '{find}' appears {occurrences} times in the file"
    else:
        out = ""

    # generate an output txt file with info
    output = (f"""
lines = {number_of_lines}
words = {number_of_words}
characters = {number_of_car}
blank lines = {blank_lines}
{freq_words_list}

{dates}

{email}

{out}
    """)

    output_name = f"{sys.argv[1].split('.')[0]}_info.txt"
    with open(output_name, "w") as file:
        file.write(output)

    print(f"File {output_name} successfully created!")


def input_test():
    # test input, specify a txt file as command-line input
    if not sys.argv[1].endswith(".txt"):
        sys.exit("Not a .txt file!")
    if len(sys.argv) > 4:
        print("Too many arguments")
        sys.exit()
    elif len(sys.argv) == 2:
        return None
    elif sys.argv[2] == "-f" or sys.argv[2] == "--find" and len(sys.argv) == 4:
        find: str = sys.argv[3]
        return find
    else:
        print("Specify the word to search after \'-f\' or \'--find\'")
        sys.exit()


def count_lines(txt):
    count = 1
    for line in txt:
        if line.endswith("\n"):
            count += 1
    return count


def count_words(txt):
    words = txt.split()
    return len(words)


def count_car(txt):
    return len(txt)


def count_blank_lines(txt):
    count = 0
    for line in txt:
        if line == "\n" or line == "\n\n":
            count += 1
    return count


def frequent_words(txt):
    words = txt.split()
    wordlist = []
    for w in words:
        if len(w) > 3:
            wordlist.append(w)

    word_counts = Counter(wordlist)
    most_common = word_counts.most_common(3)
    return_string = [f"The {len(most_common)} more frequent word(s) are: "]
    i = 0
    for word, count in most_common:
        if count != 1:
            return_string.append(f"  - '{word}' occurring {count} times")
            i += 1
    if i == 0:
        return "Not enough words"
    else:
        return_string = "\n".join(return_string)
        return return_string


def extract_dates(txt):
    date_matches = re.findall(r'\b\d{1,2}-\d{1,2}-\d{4}\b', txt)  # funziona solo con "-" in formato italiano

    parsed_dates = []
    for date_str in date_matches:
        parsed_date = parser.parse(date_str, dayfirst=True, fuzzy=True)
        parsed_date = parsed_date.strftime("%d-%m-%Y")
        parsed_dates.append(f"    {parsed_date}")
    if len(parsed_dates) == 0:
        return "No dates found"
    else:
        return parsed_dates


def extract_email(txt):
    match = re.findall(r"[\w._]+@[\w._]+\.[\w._]+", txt)
    valid_emails = []

    for w in match:
        try:
            v = validate_email(w)
            valid_emails.append(f"    {v.normalized}")
        except EmailNotValidError:
            pass

    if len(valid_emails) == 0:
        return "No email addresses found"
    else:
        return valid_emails


def search_word(txt, word):
    txt = txt.split()
    occurences: int = txt.count(word)
    return occurences


if __name__ == "__main__":
    main()
