import time
import openpyxl
import pandas as pd

from keras.utils import np_utils

from sklearn.preprocessing import StandardScaler, Normalizer
from keras.saving.legacy.model_config import model_from_json
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix
import numpy as np


import os


os.environ["CUDA_VISIBLE_DEVICES"] = "1"



def _load_preprocess_dataset(name):
    # data path

    dataset_path = "../dataset/noise/test/" + name
    # dataset_path = "../dataset/no-noise/test/" + name
    # dataset_path = "../dataset/stress-m/test/" + name

    # shuffle(乱序)
    _dataset = pd.read_excel(dataset_path, names=None)
    dataset = _dataset.values.tolist()
    dataset = np.array(dataset)
    np.random.shuffle(dataset)
    # print(dataset)

    # normalize
    data1 = dataset[:, :4]
    # 每一行进行归一化(只对前四个元素归一化，因为前四个元素比较大)
    transformer = Normalizer().fit(data1)

    data1 = transformer.transform(data1)
    data2 = dataset[:, 4:7]
    data = np.concatenate((data1, data2), axis=1)
    data = np.expand_dims(data[:, 0:7].astype(float), axis=2)


    labels = dataset[:, 7]
    labels = np_utils.to_categorical(labels)  # one-hot编码 0:[1,0] 1:[0,1]
    # print(labels)

    return data, labels


def test():
    path = '../dataset/noise/test/'
    # path = '../dataset/no-noise/test/'
    # path = '../dataset/stress-m/test/'

    file = os.listdir(path)
    name = []
    tp = []
    tn = []
    fp = []
    fn = []
    acc = []
    f1 = []
    pre = []
    rec = []
    # other

    for file_i in file:
        data, labels = _load_preprocess_dataset(file_i)
        name.append(file_i.replace(".xlsx", ''))

        # 加载模型用做预测
        json_file = open(r"../model/MLP/noise/model_test.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("../model/MLP/noise/model_test.h5")
        loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # print("...........................................")

        # # 输出预测类别

        predicted = loaded_model.predict(data)  # 返回对应概率值

        predicted_label = np.argmax(loaded_model.predict(data), axis=-1)


        true_value = []
        for label in labels:

            if str(label) == '[0. 1.]':
                true_value.append(1)
            else:
                true_value.append(0)


        # plot confusion matrix
        confusion = confusion_matrix(true_value, predicted_label, labels=[0, 1])

        TN = confusion[0][0]
        FP = confusion[0][1]
        FN = confusion[1][0]
        TP = confusion[1][1]
        t1 = TN / (TN + FP)
        t2 = FP / (TN + FP)
        t3 = FN / (FN + TP)
        t4 = TP / (FN + TP)
        tn.append('{:.4f}'.format(t1))
        fp.append('{:.4f}'.format(t2))
        fn.append('{:.4f}'.format(t3))
        tp.append('{:.4f}'.format(t4))
        print('TN:', t1 )
        print('FP:', t2)
        print('FN:', t3)
        print('TP:', t4)

        precision = t4 / (t4 + t2)
        pre.append('{:.4f}'.format(precision))
        print("precision:", precision)
        recall = t4 / (t4 + t3)
        rec.append('{:.4f}'.format(recall))
        print("recall:", recall)
        accuracy = (t1 + t4) / (t1 + t2 + t3 + t4)
        acc.append('{:.4f}'.format(accuracy))
        print("accuracy:", accuracy)
        F1 = 2 * precision * recall / (precision + recall)
        f1.append('{:.4f}'.format(F1))
        print("F1:", F1)

    name = np.array(name)
    name = name.reshape(-1, 1)

    tp = np.array(tp)
    tp = tp.reshape(-1, 1)

    tn = np.array(tn)
    tn = tn.reshape(-1, 1)

    fp = np.array(fp)
    fp = fp.reshape(-1, 1)

    fn = np.array(fn)
    fn = fn.reshape(-1, 1)

    pre = np.array(pre)
    pre = pre.reshape(-1, 1)

    rec = np.array(rec)
    rec = rec.reshape(-1, 1)

    acc = np.array(acc)
    acc = acc.reshape(-1, 1)

    f1 = np.array(f1)
    f1 = f1.reshape(-1, 1)

    data = np.concatenate((name, tp, fn, tn, fp, pre, rec, f1, acc), axis=1)
    dataFrame = pd.DataFrame(data, columns=['name', 'TP', 'FN', 'TN', 'FP',
                                            'precision', 'recall', 'F1', 'accuracy'])

    mypath = "../dataset/noise_6/libreoffice/result/MLP/result.xlsx"

    # 新建空白工作簿
    mybook = openpyxl.Workbook()
    # 根据参数(mypath)保存空白工作簿(mybook),即创建保存多个空白的excel文件
    mybook.save(mypath)

    with pd.ExcelWriter(mypath) as writer:
        dataFrame.to_excel(writer, sheet_name='page1', float_format='%.6f', index=False)


if __name__ == '__main__':
    begin_1 = time.time()
    test()
    end_1 = time.time()
    time_1 = end_1 - begin_1
    print(time_1)

