import json
import sys
import math

file_path = sys.argv[1]


class HMM:

    def __init__(self):
        self.tag_count = {}
        self.tag_transitions = {}
        self.word_tag = {}
        self.word_list = {}
        self.transition_probabilities = {}
        self.emission_probabilities = {}
        self.count = 0
        self.total_tag_count = {}
        self.tag_list = set()

    def parse_input(self):
        fp = open(file_path, 'r')
        for line in fp.readlines():
            self.count += 1
            current_tag = 'Q0'
            for mapping in line.split():
                word, tag = mapping.rsplit('/', 1)

                self.tag_list.add(tag)
                mapping = word + '/' + tag
                if mapping in self.word_tag:
                    self.word_tag[mapping] += 1
                else:
                    self.word_tag[mapping] = 1

                if tag in self.total_tag_count:
                    self.total_tag_count[tag] += 1
                else:
                    self.total_tag_count[tag] = 1

                if word in self.word_list:
                    if tag not in self.word_list[word]:
                        self.word_list[word].append(tag)
                else:
                    self.word_list[word] = [tag]

                transition = current_tag + '-' + tag

                if transition in self.tag_transitions:
                    self.tag_transitions[transition] += 1
                else:
                    self.tag_transitions[transition] = 1
                current_tag = tag

            transition = current_tag + '-Q1'
            if transition in self.tag_transitions:
                self.tag_transitions[transition] += 1
            else:
                self.tag_transitions[transition] = 1

        self.total_tag_count['Q0'] = self.count
        self.total_tag_count['Q1'] = self.count

    def calculate_transition_probabilities(self):
        number_transition = len(self.tag_transitions)
        for transition in self.tag_transitions:
            self.transition_probabilities[transition] = math.log(self.tag_transitions[transition] + 1) - math.log(
                number_transition + self.total_tag_count[transition.split('-')[0]])

        # Smoothing transition probabilities
        for f_tag in self.total_tag_count:
            for s_tag in self.total_tag_count:
                if f_tag + '-' + s_tag in self.transition_probabilities:
                    continue
                self.transition_probabilities[f_tag + '-' + s_tag] = - math.log(
                    (number_transition + self.total_tag_count[f_tag]))

    def calculate_emission_probabilities(self):
        for pair in self.word_tag:
            self.emission_probabilities[pair] = math.log(self.word_tag[pair]) - math.log(
                self.total_tag_count[pair.rsplit('/', 1)[1]])

    def write_model(self):
        fp = open('hmmmodel.txt', 'w')
        temp_list = [self.word_list, self.transition_probabilities, self.emission_probabilities,
                     {'tag_list': list(self.tag_list)}]
        json.dump(temp_list, fp)
        fp.close()


if __name__ == "__main__":
    model = HMM()
    model.parse_input()
    model.calculate_transition_probabilities()
    model.calculate_emission_probabilities()
    model.write_model()
