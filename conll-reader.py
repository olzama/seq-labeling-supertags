# Olga Zamaraeva 2024
# python conll-reader.py UD_English-EWT/en_ewt-ud-test.conllu examples-test.json

# Read in CONLL-U files.
import sys
import json
import re


def parse_conllu(file_path, output_path):
    SEP = '# text = '
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    sentences_data = []
    current_sentence = []
    original_sentence_text = ""
    working_sentence_text = ""
    original_count = 0
    original_sentences = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            if line.startswith('# sent_id'):
                s_id = line.split('=')[1].strip()
            if line.startswith(SEP):
                original_count += 1
                original_sentence_text = line[len(SEP):]
                original_sentences[original_sentence_text] = s_id
                working_sentence_text = original_sentence_text  # Copy to avoid modifying the original text
                current_sentence = []
        else:
            parts = line.split('\t')
            if len(parts) < 10 or '-' in parts[0]:
                continue
            word_form = parts[1]
            # Find start and end positions for each token in the working sentence text
            match = re.search(re.escape(word_form), working_sentence_text)
            if match:
                word_start = match.start()
                word_end = match.end()
                token_data = {
                    'word': word_form,
                    'start': word_start,
                    'end': word_end
                }
                current_sentence.append(token_data)
                # Replace matched token in working_sentence_text to avoid duplicate matches
                working_sentence_text = working_sentence_text[:word_start] + ' ' * len(
                    word_form) + working_sentence_text[word_end:]
        # If we reach the end of a sentence, store it and reset
        if line == '' or line.startswith('# sent_id') or line.startswith('# newpar') or line.startswith('# newdoc'):
            if current_sentence:
                sentences_data.append({
                    'text': original_sentence_text,  # Store the original sentence text here
                    'words': current_sentence
                })
                current_sentence = []
    if current_sentence:
        sentences_data.append({
            'text': original_sentence_text,
            'words': current_sentence
        })
    output_data = {
        'sentences': sentences_data
    }
    print("Original sentence count:", original_count)
    print("Retreived sentence count:", len(sentences_data))
    print("Sentences in the original data but not in the retreived data:")
    set_of_retreived_sentences = set([sentence['text'] for sentence in sentences_data])
    diff = set(list(original_sentences.keys())) - set_of_retreived_sentences
    # print difference of sets:
    print(diff)
    for k in diff:
        print(original_sentences[k])

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)


#main
if __name__ == "__main__":
    parse_conllu(sys.argv[1], sys.argv[2])
