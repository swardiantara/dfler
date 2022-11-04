import pandas as pd
import math
import numpy as np
import sys
from seqeval.metrics import f1_score

from seqeval.metrics import classification_report as seqeval_classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from tqdm import tqdm, trange
from simpletransformers.ner import NERModel, NERArgs


def main():
    # Load the dataset
    dataset_train_path = './data/droner_train_4.csv'
    dataset_test_path = './data/droner_test_4.csv'
    dataset_train = pd.read_csv(dataset_train_path, encoding= 'unicode_escape')
    dataset_test = pd.read_csv(dataset_test_path, encoding= 'unicode_escape')

    # Drop the unused columns
    dataset_train = dataset_train.drop(dataset_train.columns[[0, 1, 2, 3]], axis=1)
    dataset_test = dataset_test.drop(dataset_test.columns[[0, 1, 2, 3]], axis=1)

    # Get the unique labels from train set
    label = dataset_train["labels"].unique().tolist()

    # Set the model configuration
    args = NERArgs()
    args.num_train_epochs = 4
    args.learning_rate = 0.0001 # 0.0001  5e-5, 3e-5, 2e-5
    args.overwrite_output_dir = True
    args.train_batch_size = 16
    args.eval_batch_size = 16

    # Create the model
    model = NERModel("bert", "bert-base-cased", labels=label, args =args, use_cuda=True)
    
    # Save the train history
    sys.stdout = open('./train_result/train_history.txt', 'w')
    model.train_model(dataset_train, eval_data = dataset_test, acc=accuracy_score)
    sys.stdout.close()

    #Save the train result
    result, model_outputs, preds_list = model.eval_model(dataset_test)
    sys.stdout = open('./train_result/train_evaluation.txt', 'w')
    print(result)
    sys.stdout.close()

    dataset_test_group = dataset_test.groupby(['sentence_id'], as_index=False)['words', 'labels'].agg(lambda x: list(x))
    y_test = dataset_test_group['labels']

    y_pred_list = []
    y_test_list = []
    for row in range(0, len(preds_list)):
        y_pred_list = np.concatenate((y_pred_list, preds_list[row]), axis=0)
        y_test_list = np.concatenate((y_test_list, y_test[row]), axis=0)

    data_prediction = pd.DataFrame({'actual_class': y_test_list, 'predicted_class': y_pred_list})

    sys.stdout = open('./train_result/confusion_matrix.txt', 'w')
    confusion_matrix = pd.crosstab(data_prediction['predicted_class'], data_prediction['actual_class'])
    print(confusion_matrix)
    sys.stdout.close()

    y_test = data_prediction['actual_class'].to_list()
    y_pred = data_prediction['predicted_class'].to_list()

    sys.stdout = open('./train_result/strict_evaluation.txt', 'w')
    sklearn_report = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True, labels=['O', 'B-ACTION', 'I-ACTION', 'B-COMPONENT', 'I-COMPONENT', 'B-FUNCTION', 'I-FUNCTION', 'B-ISSUE', 'I-ISSUE', 'B-STATE', 'I-STATE', 'B-PARAMETER', 'I-PARAMETER'])).T
    print(sklearn_report)
    sys.stdout.close()

    sys.stdout = open('./train_result/unstrict_evaluation.txt', 'w')
    seqeval_report = pd.DataFrame(seqeval_classification_report([y_test], [y_pred], output_dict=True)).T
    print(seqeval_report)
    sys.stdout.close()

if __name__ == "__main__":
    main()