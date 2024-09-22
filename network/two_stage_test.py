import time
import openpyxl
import pandas as pd
from keras.utils import np_utils
from sklearn.preprocessing import Normalizer
from keras.saving.legacy.model_config import model_from_json
from sklearn.metrics import confusion_matrix
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
    data_1 = np.concatenate((data1, data2), axis=1)
    data_1 = np.expand_dims(data_1[:, 0:6].astype(float), axis=2)

    data3 = dataset[:, 4:7]
    data_2 = np.concatenate((data1, data3), axis=1)
    data_2 = np.expand_dims(data_2[:, 0:7].astype(float), axis=2)

    labels = dataset[:, 7]
    labels = np_utils.to_categorical(labels)
    workload = dataset[:, 8]
    workload = np_utils.to_categorical(workload)

    return data_1, data_2, labels, workload

def load_model(path):
    json_file = open(path + ".json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path + ".h5")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return loaded_model

def evaluate_model(model, data, labels):
    predicted_label = np.argmax(model.predict(data), axis=-1)
    true_value = [np.argmax(label) for label in labels]

    confusion = confusion_matrix(true_value, predicted_label, labels=[0, 1])

    TN = confusion[0][0]
    FP = confusion[0][1]
    FN = confusion[1][0]
    TP = confusion[1][1]

    t1 = TN / (TN + FP) if (TN + FP) != 0 else 0
    t2 = FP / (TN + FP) if (TN + FP) != 0 else 0
    t3 = FN / (FN + TP) if (FN + TP) != 0 else 0
    t4 = TP / (FN + TP) if (FN + TP) != 0 else 0

    precision = t4 / (t4 + t2) if (t4 + t2) != 0 else 0
    recall = t4 / (t4 + t3) if (t4 + t3) != 0 else 0
    accuracy = (t1 + t4) / (t1 + t2 + t3 + t4) if (t1 + t2 + t3 + t4) != 0 else 0
    F1 = 2 * precision * recall / (precision + recall) if (precision + recall) != 0 else 0

    return {
        'TN': t1,
        'FP': t2,
        'FN': t3,
        'TP': t4,
        'precision': precision,
        'recall': recall,
        'accuracy': accuracy,
        'F1': F1
    }

def test():
    path = '../dataset/workload-1/test/'
    files = os.listdir(path)

    results = []

    workload_model = load_model("../model/MLP/workload-1/model")

    for file_i in files:
        data1, data2, labels, workloads = _load_preprocess_dataset(file_i)
        dataset_name = file_i.replace(".xlsx", '')

        # 第一部分: 根据predicted_workload_value进行检测
        predicted_workload_value = np.argmax(workload_model.predict(data1), axis=-1)
        
        for workload_type in range(3):
            workload_indices = [i for i, wl in enumerate(predicted_workload_value) if wl == workload_type]

            if workload_indices:
                workload_data = data2[workload_indices]
                workload_labels = labels[workload_indices]

                if workload_type == 0:
                    attack_model = load_model(f"../model/MLP/noise/model_test")
                # elif workload_type == 1:
                #     attack_model = load_model(f"../model/MLP/no-noise/model_test")
                elif workload_type == 1:
                    attack_model = load_model(f"../model/MLP/stress-c/model_test")
                else:
                    attack_model = load_model(f"../model/MLP/stress-m/model_test")

                metrics = evaluate_model(attack_model, workload_data, workload_labels)

                result = {
                    'name': dataset_name,
                    'type': 'predicted',
                    'workload': workload_type,
                    'TP': metrics['TP'],
                    'FP': metrics['FP'],
                    'FN': metrics['FN'],
                    'TN': metrics['TN'],
                    'precision': metrics['precision'],
                    'recall': metrics['recall'],
                    'F1': metrics['F1'],
                    'accuracy': metrics['accuracy']
                }

                results.append(result)

        # 第二部分: 根据true_workload_value进行检测
        true_workload_value = [np.argmax(workload) for workload in workloads]

        for workload_type in range(3):
            true_workload_indices = [i for i, wl in enumerate(true_workload_value) if wl == workload_type]

            if true_workload_indices:
                true_workload_data = data2[true_workload_indices]
                true_workload_labels = labels[true_workload_indices]

                if workload_type == 0:
                    attack_model = load_model(f"../model/MLP/noise/model_test")
                elif workload_type == 1:
                    attack_model = load_model(f"../model/MLP/stress-c/model_test")
                else:
                    attack_model = load_model(f"../model/MLP/stress-m/model_test")

                metrics = evaluate_model(attack_model, true_workload_data, true_workload_labels)

                result = {
                    'name': dataset_name,
                    'type': 'true',
                    'workload': workload_type,
                    'TP': metrics['TP'],
                    'FP': metrics['FP'],
                    'FN': metrics['FN'],
                    'TN': metrics['TN'],
                    'precision': metrics['precision'],
                    'recall': metrics['recall'],
                    'F1': metrics['F1'],
                    'accuracy': metrics['accuracy']
                }

                results.append(result)

    df = pd.DataFrame(results)

    mypath = "../dataset/workload-1/result/result.xlsx"
    with pd.ExcelWriter(mypath) as writer:
        df.to_excel(writer, sheet_name='page1', float_format='%.6f', index=False)

    print("Metrics saved to 'result.xlsx'")

if __name__ == '__main__':
    start_time = time.time()
    test()
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
