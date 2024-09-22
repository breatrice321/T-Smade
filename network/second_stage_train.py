import time

import numpy as np
import pandas as pd
import psutil

import tensorflow as tf

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.preprocessing import normalize, Normalizer

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils


import os

os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def _load_preprocess_dataset():
     _dataset_path = "../dataset/noise/train/training_dataset.xlsx"
    # _dataset_path = "../dataset/no-noise/train/training_dataset.xlsx"
    # _dataset_path = "../dataset/stress-m/train/training_dataset.xlsx"


    # shuffle(乱序)
    _dataset = pd.read_excel(_dataset_path, names=None)
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


def baseline_model():
    model = Sequential()
    # MLP
    model.add(Dense(12, input_dim=7, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(2, activation='sigmoid'))
    print(model.summary())
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['binary_accuracy'])

    return model


def train():
    # 获取进程ID
    pid = os.getpid()
    p = psutil.Process(pid)

    # 记录训练开始时的内存使用情况
    start_memory = p.memory_info().rss

    data, labels = _load_preprocess_dataset()

    # 训练分类器
    estimator = KerasClassifier(build_fn=baseline_model, epochs=50, batch_size=1, verbose=1)  # 模型，轮数，每次数据批数，显示进度条
    estimator.fit(data, labels, validation_split=0.2)  # 训练模型

    # 记录训练结束时的内存使用情况
    end_memory = p.memory_info().rss

    # 计算内存消耗
    memory_cost = end_memory - start_memory
    print(f"Memory cost for training: {memory_cost / (1024 * 1024)} MB")

    # model:6 input
    model_json = estimator.model.to_json()
    with open(r"../model/MLP/noise/model_test.json", 'w') as json_file:
        json_file.write(model_json)  # 权重不在json中,只保存网络结构
    estimator.model.save_weights('../model/MLP/noise/model_test.h5')


if __name__ == '__main__':
    begin = time.time()
    train()
    end = time.time()
    time = end - begin
    print(time)
