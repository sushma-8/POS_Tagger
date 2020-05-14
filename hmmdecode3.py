"""
Results for Italian:
Correct: 9837
Total: 10417
Accuracy: 0.944321781703

Results for Japanese:
Correct: 11445
Total: 12438
Accuracy: 0.920164013507

Results for Hindi:
Correct: 32764
Total: 35430
Accuracy: 0.924753034152

"""

import json
import operator
import sys

file_path = sys.argv[1]


class HMMDecode:

    def __init__(self):
        self.word_list = {}
        self.transition_probabilities = {}
        self.emission_probabilities = {}
        self.tag_list = []
        self.open_tags = None

    def viterbi_decode(self, sentence):
        words = sentence.strip().split()
        previous_tag_list = [['Q0']]
        tag_list = [{'Q0': 0}]
        bt_tags_dict = [{'Q0': None}]
        index = 0
        words.append('hmm_end_word')
        for word in words:
            index += 1
            temp_dict = {}
            temp_tag_list = []
            temp_bt_tags = {}
            if word not in self.word_list:
                possible_tags = self.tag_list
            else:
                possible_tags = self.word_list[word]
            for tag in possible_tags:
                temp_tag_list.append(tag)
                if word + '/' + tag in self.emission_probabilities:
                    emission_prob = self.emission_probabilities[word + '/' + tag]
                else:
                    emission_prob = 0
                for prev_tag in previous_tag_list[index - 1]:
                    transition_prob = self.transition_probabilities[prev_tag + '-' + tag]
                    current_probability = tag_list[index - 1][prev_tag] + emission_prob + transition_prob
                    if tag in temp_dict:
                        if current_probability > temp_dict[tag]:
                            temp_bt_tags[tag] = prev_tag
                            temp_dict[tag] = current_probability
                    else:
                        temp_bt_tags[tag] = prev_tag
                        temp_dict[tag] = current_probability
            previous_tag_list.append(temp_tag_list)
            tag_list.append(temp_dict)

            bt_tags_dict.append(temp_bt_tags)

        final_tag = tag_list[-1]
        final_tag = max(final_tag.items(), key=operator.itemgetter(1))[0]
        tag_seq = []
        prev_tag = final_tag
        index = len(bt_tags_dict)

        while prev_tag != 'Q0':
            index -= 1
            cur_tag = prev_tag
            tag_seq.insert(0, cur_tag)
            prev_tag = bt_tags_dict[index][cur_tag]
        output_sent = ''
        for idx, word in enumerate(words[:-1]):
            output_sent = output_sent + word + '/' + tag_seq[idx] + ' '
        return output_sent

    def parse_test_input(self):
        fp = open(file_path, 'r')
        output_file = open('hmmoutput.txt', 'w')
        for line in fp.readlines():
            sentence_tags = self.viterbi_decode(line)
            output_file.write(sentence_tags.strip() + '\n')

    def read_model(self):
        with open('hmmmodel.txt', 'r') as json_file:
            temp_list = json.load(json_file)
            self.word_list = temp_list[0]
            self.transition_probabilities = temp_list[1]
            self.emission_probabilities = temp_list[2]
            self.tag_list = temp_list[3]['tag_list']
            self.word_list['hmm_end_word'] = ["Q1"]


if __name__ == "__main__":
    model = HMMDecode()
    model.read_model()
    model.parse_test_input()
