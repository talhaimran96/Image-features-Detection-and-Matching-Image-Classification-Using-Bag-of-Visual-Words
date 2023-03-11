########################################################################################################################
# Muhammad Talha Imran
# MSDS-2022, SEECS NUST
# REGN # 402546
# Computer Vision Assignment 1
########################################################################################################################

# This part is the implementation of classification of the flower dataset using random forest and different number of clusters
# Ranging from 2 to 128, resulting confusion matrices are present in the results folder

import Pre_processing_pipeline as preprocess
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd

images_in, labesls_in = preprocess.read_images_to_array("../Datasets/flower_photos")

# Preforming 80-20 split, stratified
train_set, test_set, train_labels, test_labels = train_test_split(images_in, labesls_in, test_size=0.2, random_state=42,
                                                                  stratify=labesls_in, shuffle=True)

k = 200  # defining k as number of clusters

kmean = preprocess.compute_cluster_centriods(preprocess.compute_descriptor_array(train_set), k=k)
training_vocabulary = preprocess.compute_vocabulary(train_set, kmean=kmean, k=k)
test_vocabulary = preprocess.compute_vocabulary(test_set, kmean=kmean, k=k)

label_encoder = LabelEncoder()  # creating an instance of labelencoder, to convert categorical to numerical labels
label_encoder.fit(train_labels)  # fitting the label encoder

# encoding the test and training labels to numerical values
test_labs = label_encoder.transform(test_labels)  # accordian was named accordion in the training lable folder
# (I have renamed it to conform with the other one)
train_labs = label_encoder.transform(train_labels)

# using random forest, there are two hyperparameters to set, k=#number of cluster and max_depth of trees
classifier = RandomForestClassifier(max_depth=100, random_state=0)
classifier.fit(training_vocabulary, train_labs)
predictions = classifier.predict(test_vocabulary)

# Inverting the encodings for predicted and test labels
print(label_encoder.inverse_transform(test_labs))
print(label_encoder.inverse_transform(predictions))

# Classification report
print(classification_report(test_labels, label_encoder.inverse_transform(predictions),
                            target_names=label_encoder.classes_))
# Confusion Matrix
cm = confusion_matrix(test_labels, label_encoder.inverse_transform(predictions),
                      labels=label_encoder.classes_)

display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
display.plot()
plt.title(f"k = {k}")
plt.show()


def save_classification_report(report, path, k):
    """
    Save the classification report as csv
    :param report: Report to save
    :param path: Where to save the report
    :param k: hyper-parameter, k=# of clusters
    :return: Nothing
    """
    df = pd.DataFrame(report)
    df.to_csv(path + "\\" + "Classification_report_" + "k_" + f"{k}.csv")
    return 0


def display_examples(images, actual_labs, predicted_labs):
    """
    To display examples of predictions on images
    :param images: Images to display
    :param actual_labs: Correct labels
    :param predicted_labs: Predicted labels from the classifier
    :return: Nothing
    """
    p = len(images)
    q = 4
    p = p // q
    i = 1
    for img in images:
        plt.subplot(q, p, i)
        plt.imshow(img, cmap="gray")
        plt.title("Actual lab: " + actual_labs[i - 1] + ", "
                  + "Prediction: " + predicted_labs[i - 1])
        i += 1
    plt.show()
    return 0


## commented post data collection, can be uncommented to extract reports

n_samples = 20 / len(test_vocabulary)

# sub sampling from the test set to display images and labels as examples
X, x, Y, y = train_test_split(test_set, test_labels, test_size=n_samples, random_state=42,
                              stratify=test_labels, shuffle=True)

x_ = preprocess.compute_vocabulary(x, kmean=kmean, k=k)

report = classification_report(test_labels, label_encoder.inverse_transform(predictions),
                               target_names=label_encoder.classes_, output_dict=True)
save_classification_report(report=report, path="../results/Flowers_RF", k=k)

examples_predictions = classifier.predict(x_)
display_examples(x, y, label_encoder.inverse_transform(examples_predictions))
