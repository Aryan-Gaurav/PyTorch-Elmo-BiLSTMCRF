""" Command Line Usage
Args:
    eval: Evaluate F1 Score and Accuracy on test set
    pred: Predict sentence.
    (optional): Sentence to predict on. If none given, predicts on "Peter Johnson lives in Los Angeles"

Example:
    > python test.py eval pred "Obama is from Hawaii"
"""

from model.data_utils import CoNLLDataset
from model.config import Config
from model.ner_model import NERModel
from model.ner_learner import NERLearner
import sys


def main():
    # create instance of config
    config = Config()
    if config.use_elmo: config.processing_word = None

    #build model
    model = NERModel(config)

    learn = NERLearner(config, model)
    learn.load()

    if len(sys.argv) == 1:
        print("No arguments given. Running full test")
        sys.argv.append("eval")
#         sys.argv.append("pred")

    if sys.argv[1] == "eval":
        # create datasets
        test = CoNLLDataset(config.filename_test, config.processing_word,
                             config.processing_tag, config.max_iter)
        learn.evaluate(test)

    elif sys.argv[1] == "pred":
        try:
            sent = sys.argv[2]
        except IndexError:
            sent = "Paracetamols are analgesic drugs. Penicillin is a drug"

        print("Predicting sentence: ", sent)
        pred = learn.predict(sent)
        print(pred)



if __name__ == "__main__":
    main()
