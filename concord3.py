
import sys

def extract_e_words(file):

    e_words = []
    line = file.readline()
    while line != "\"\"\"\"\n":
        e_words.append(line.strip())
        line = file.readline()
    return e_words

def extract_b_lines(file):
    b_lines = []
    line = file.readline()
    while line:
        b_lines.append(line.strip())
        line = file.readline()
    return b_lines
    
def create_capped_body_lines(body_lines_raw, exclusion_words):

    capped_body_line_lst = []

    for line in body_lines_raw:
        split_line = line.split()
        for index, word in enumerate(split_line):
            if word.lower() not in exclusion_words:
                split_copy = split_line.copy()
                capped_word = word.upper()
                split_copy[index] = capped_word
                joined_line = " ".join(split_copy)
                capped_body_line_lst.append((joined_line, capped_word))
                
    return capped_body_line_lst

def alphabetically_order_bodylines(body_lines):

    return sorted(body_lines, key = lambda item: item[1].lower())

def cut_off_left_side(idx_of_keyword_start, line):

    new_line_start_idx = idx_of_keyword_start - 20
    new_line = line[new_line_start_idx:]
    i = 0
    # The slice already begins at a word boundary.
    if new_line_start_idx == 0 or line[new_line_start_idx- 1] == " ":
        return line[new_line_start_idx:]
    
    while new_line[i] != ' ':
        i += 1
    i+= 1
    final_line = new_line[i:]
    return final_line

def cut_off_right_side(idx_of_keyword_start, line):
    final_allowed_idx = idx_of_keyword_start + 30

    if final_allowed_idx >= len(line) - 1:
        return line

    # The character following the limit is a space, so a word
    # ends exactly at the limit.
    if line[final_allowed_idx + 1] == " ":
        return line[:final_allowed_idx + 1]

    # The limit occurs inside a word. Find its starting space.
    cutoff = line.rfind(" ", idx_of_keyword_start, final_allowed_idx + 1)
    return line[:cutoff]

def KWIC_format(idx_of_keywordstart, keyword, line):
    
    keyword_column = 29
    idx_of_keywordstart = line.find(keyword)
    num_spaces = keyword_column - idx_of_keywordstart
    formatted_line = " "* num_spaces + line
    return formatted_line

def cut_sides(ordered_body_lines):
    final_lines = []
    keyword_column = 29
    left_limit = 20
    right_limit = 30
    for tup in ordered_body_lines:
        line = tup[0]
        keyword = tup[1]
        split = tup[0].split()
        words = split.copy()
        mum_spaces = 0
        idx_of_keywordstart = 0
        new_res = 'fake'

        '''keyword_index = words.index(keyword)
        left_words = []
        right_words = []'''
        
        for word in words:
            if word == tup[1]:
                break
            else:
                idx_of_keywordstart = idx_of_keywordstart + len(word) + 1
                
        sign = keyword_column - idx_of_keywordstart

        if(idx_of_keywordstart > 20):
            line = cut_off_left_side(idx_of_keywordstart,line)
            idx_of_keywordstart = line.find(keyword)
        if(idx_of_keywordstart + 30 < len(line)):
            line = cut_off_right_side(idx_of_keywordstart,line)

        final_line = KWIC_format(idx_of_keywordstart, keyword, line)
        final_lines.append(final_line)
    return final_lines
        

def generate_concordance(body_lines, exclusion_words):
        """Generate output without retaining one full line copy per keyword."""
        exclusion_words = set(exclusion_words)
        entries = []

        for raw_line in body_lines:
            words = raw_line.split()
            normalized_line = " ".join(words)
            word_start = 0

            for word in words:
                word_end = word_start + len(word)
                if word.lower() not in exclusion_words:
                    entries.append(
                        (word.upper().lower(), normalized_line, word_start, word_end)
                    )
                word_start = word_end + 1

        entries.sort(key=lambda item: item[0])
        final_result = []

        for _, line, keyword_start, keyword_end in entries:
            left_start = 0
            if keyword_start > 20:
                left_start = keyword_start - 20
                if line[left_start - 1] != " ":
                    next_space = line.find(" ", left_start)
                    left_start = next_space + 1

            relative_keyword_start = keyword_start - left_start
            right_end = len(line)
            final_allowed_idx = left_start + relative_keyword_start + 30
            if final_allowed_idx < len(line) - 1:
                if line[final_allowed_idx + 1] == " ":
                    right_end = final_allowed_idx + 1
                else:
                    right_end = line.rfind(
                        " ", keyword_start, final_allowed_idx + 1
                    )

            context = (
                line[left_start:keyword_start]
                + line[keyword_start:keyword_end].upper()
                + line[keyword_end:right_end]
            )
            final_result.append(" " * (29 - relative_keyword_start) + context)

        return final_result
       

def main ():
    file_name = sys.argv[1]
    file = open(file_name, "r")

    num = file.readline()
    sep = file.readline()

    exclusion_words = extract_e_words(file)
    exclusion_words_lower = [word.lower() for word in exclusion_words]
        
    body_lines_raw = extract_b_lines(file)

    for line in generate_concordance(body_lines_raw, exclusion_words_lower):
        print(line)
    
    

    

if __name__ == "__main__":
    main()
