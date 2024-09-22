import time
import openpyxl
import pandas as pd
from keras.utils import np_utils
from sklearn.preprocessing import Normalizer
from keras.saving.legacy.model_config import model_from_json
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def _load_preprocess_dataset(name):
    dataset_path = "../dataset/workload-1/test/" + name
    _dataset = pd.read_excel(dataset_path, names=None)
    dataset = _dataset.values.tolist()
    dataset = np.array(dataset)
    np.random.shuffle(dataset)

    data1 = dataset[:, :4]
    transformer = Normalizer().fit(data1)
    data1 = transformer.transform(data1)
    data2 = dataset[:, 4:6]
    data = np.concatenate((data1, data2), axis=1)
    data = np.expand_dims(data[:, 0:6].astype(float), axis=2)

    labels = dataset[:, 8]
    labels = np_utils.to_categorical(labels)
    return data, labels


def test():
    path = '../dataset/workload-1/test/'
    files = os.listdir(path)
    results = []
    confusion_matrices = {}

    # Load the workload model for prediction
    json_file = open(r"../model/MLP/workload-1/model.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("../model/MLP/workload-1/model.h5")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


    for file_i in files:
        data, labels = _load_preprocess_dataset(file_i)
        dataset_name = file_i.replace(".xlsx", '')

        predicted_label = np.argmax(loaded_model.predict(data), axis=-1)

        true_value = []
        for label in labels:
            if str(label) == '[1. 0. 0.]':
                true_value.append(0)
            elif str(label) == '[0. 1. 0.]':
                true_value.append(1)
            elif str(label) == '[0. 0. 1.]':
                true_value.append(2)
            # else:
            #     true_value.append(3)

        confusion = confusion_matrix(true_value, predicted_label, labels=[0, 1, 2])

        print("Confusion Matrix:")
        print(confusion)

        precision = precision_score(true_value, predicted_label, labels=[0, 1, 2], average=None)
        recall = recall_score(true_value, predicted_label, labels=[0, 1, 2], average=None)
        accuracy = accuracy_score(true_value, predicted_label)
        F1 = f1_score(true_value, predicted_label, labels=[0, 1, 2], average=None)

        result = {
            'name': dataset_name,
            'confusion_matrix': confusion,
            'precision': precision,
            'recall': recall,
            'f1_score': F1,
            'accuracy': accuracy
        }

        results.append(result)
        confusion_matrices[dataset_name] = confusion

    data = {
        'name': [r['name'] for r in results],
        'precision': [', '.join(map(str, r['precision'])) for r in results],
        'recall': [', '.join(map(str, r['recall'])) for r in results],
        'f1_score': [', '.join(map(str, r['f1_score'])) for r in results],
        'accuracy': [r['accuracy'] for r in results]
    }

    df = pd.DataFrame(data)

    mypath = "../dataset/workload-1/result/result.xlsx"
    with pd.ExcelWriter(mypath) as writer:
        df.to_excel(writer, sheet_name='Summary', float_format='%.6f', index=False)

    # save_confusion_matrices_to_excel(confusion_matrices, mypath)

    print("Metrics saved to 'result.xlsx'")

if __name__ == '__main__':
    begin_1 = time.time()
    test()
    end_1 = time.time()
    time_1 = end_1 - begin_1
    print(time_1)
