# POS_Tagger
POS Tagging using Hidden Markov Model
# Data
The training and development data are uploaded in hmm_training_data. It has the following format:
- Two files (one Italian, one Japanese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
- Two files (one Italian, one Japanese) with untagged development data, with words separated by spaces and each sentence on a new line.
- Two files (one Italian, one Japanese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.
- A readme/license file.

# Code
There are two programs: hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data. The learning program will be invoked in the following way:

> python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.

The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

# Results
Obtained the following results for Italian, Japanese and Hindi languages:<br />

Results for Italian:<br />
Accuracy: 0.944321781703

Results for Japanese:<br />
Accuracy: 0.920164013507

Results for Hindi:<br />
Accuracy: 0.924753034152
