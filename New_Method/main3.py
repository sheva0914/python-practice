# coding: utf-8

# this is the main file of past method.

# classify traffic in each stages if there is any risk in it.
# there are 3 alert level.

import numpy as np
import time
# import random
# import setting_classifier
import setting_classifier_5_class

import functions as F
import c1_past as c1
# import classifier_smr as c0
# import classifier1 as c1
# import classifier1_h200 as c1_200
# import classifier2 as c2
# import classifier3 as c3


def accuracy(pre, ans):
    # return float(np.sum(np.argmax(pre, 1) == np.argmax(ans, 1)))
    k = np.argmax(pre)
    l = np.argmax(ans)
    if k == l:
        return 1
    else:
        return 0

classifier = c1
LABEL_NUM = 5

INPUT = "data/kdd_train_1000.csv"
INPUT1 = "data/kdd_train_20Percent.csv"
INPUT2 = "data/kdd_train_39_class.csv"
INPUT3 = "data/kdd_test_39_class.csv"

# data pre-process
test_data, test_label = [], []
# setting_classifier.data_read(INPUT3, test_data, test_label)
setting_classifier_5_class.data_read(INPUT3, test_data, test_label)

predict_histogram = np.zeros((LABEL_NUM, LABEL_NUM))
predict_list = []
label_list = []

tp_ = np.zeros([LABEL_NUM])
tn_ = np.zeros([LABEL_NUM])
fp_ = np.zeros([LABEL_NUM])
fn_ = np.zeros([LABEL_NUM])

_acc = np.zeros([LABEL_NUM])
P = np.zeros([LABEL_NUM])
R = np.zeros([LABEL_NUM])

test_start = 0
acc = 0
z = 0
print("classifying start!")
start = time.time()
for i, line_data in enumerate(test_data):
    c = 0
    line_label = test_label[i]

    # if i >= 20:
    #     break
    print("\n--data number : %d--" % i)

    line_predict = classifier.prediction(line_data)

    a = np.argmax(line_predict)
    b = np.argmax(line_label)
    if a == b:
        acc += 1
    # z.append(accuracy(line_predict, line_label))
    z += accuracy(line_predict, line_label)

    print("Predict      : %s" % str(line_predict))
    print("Ground Truth : %s" % str(line_label))

    # add tmp matrix to predict matrix
    F.update_result(line_predict, line_label, predict_histogram)
    predict_list.append(np.argmax(line_predict))
    label_list.append(np.argmax(line_label))

    if (i + 1) % 10 == 0:
        pre_sum = np.sum(predict_histogram, 1)
        gt_sum = np.sum(predict_histogram, 0)
        for j in range(0, LABEL_NUM):
            tp_[j] = np.diag(predict_histogram)[j]
            fp_[j] = pre_sum[j] - tp_[j]
            fn_[j] = gt_sum[j] - tp_[j]
            tn_[j] = np.ndarray.sum(predict_histogram) - (tp_[j] + fp_[j] + fn_[j])

            print(predict_histogram[j])
            P[j] = tp_[j] / (tp_[j] + fp_[j] + 1)
            R[j] = tp_[j] / (tp_[j] + fn_[j] + 1)
            _acc[j] = (tp_[j] + tn_[j]) / (tp_[j] + tn_[j] + fp_[j] + fn_[j])

        precision = float(np.sum(P) / LABEL_NUM)
        recall = float(np.sum(R) / LABEL_NUM)
        f_measure = 2 * precision * recall / (precision + recall)
        accuracy2 = float(np.sum(_acc) / LABEL_NUM)

        # accuracy = F.calc_acc(predict_list, label_list)

        print("--- Middle Result (classified %d batches) ---" % (i + 1))
        print("Precision    : %0.15f" % precision)
        print("Recall       : %0.15f" % recall)
        print("F Measure    : %0.15f" % f_measure)
        # print("Accuracy     : %0.15f" % (accuracy(predict_list, label_list) / (i+1)))
        print("Accuracy     : %0.15f" % (z / (i+1)))
        print("Accuracy     : %0.15f" % (acc / (i + 1)))
        print("Accuracy 2   : %0.15f\n" % accuracy2)


print("classification time : %s" % (time.time() - start))
print("Accuracy     : %0.15f" % (z / (i + 1)))


# count the number of each status per 1 class
pre_sum = np.sum(predict_histogram, 1)
gt_sum = np.sum(predict_histogram, 0)
for i in range(0, LABEL_NUM):
    tp_[j] = np.diag(predict_histogram)[j]
    fp_[j] = pre_sum[j] - tp_[j]
    fn_[j] = gt_sum[j] - tp_[j]
    tn_[j] = np.ndarray.sum(predict_histogram) - (tp_[j] + fp_[j] + fn_[j])

    print(predict_histogram[j])
    P[j] = tp_[j] / (tp_[j] + fp_[j] + 1)
    R[j] = tp_[j] / (tp_[j] + fn_[j] + 1)
    _acc[j] = (tp_[j] + tn_[j]) / (tp_[j] + tn_[j] + fp_[j] + fn_[j])

precision = float(np.sum(P) / LABEL_NUM)
recall = float(np.sum(R) / LABEL_NUM)
f_measure = 2 * precision * recall / (precision + recall)
accuracy2 = float(np.sum(_acc) / LABEL_NUM)
# accuracy = F.calc_acc(predict_list, label_list)

print("--- Total Result ---")
print("Precision    : %0.15f" % precision)
print("Recall       : %0.15f" % recall)
print("F Measure    : %0.15f" % f_measure)
print("Accuracy     : %0.15f" % (acc / len(test_data)))
print("Accuracy 2   : %0.15f\n" % accuracy2)

print("\nFinish All classification!!\n")
