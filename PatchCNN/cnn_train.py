import pickle

import keras
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from keras.layers import (Activation, BatchNormalization, Conv2D, Dense,
                          Dropout, Flatten, MaxPool2D)
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model, to_categorical
from numpy.random import normal
from skimage import filters, img_as_float, img_as_ubyte, img_as_uint, io
from skimage.filters import threshold_mean, threshold_otsu
from sklearn.model_selection import train_test_split

import cv2

INPUT_SHAPE = (50,50,1)

X = []
Y = []
'''
print("Reading images...")
hw_inputs = io.imread_collection("patches_hw/*.png")
printed_inputs = io.imread_collection("patches_printed/*.png")
noise_inputs = io.imread_collection("patches_noise/*.png")

for im in hw_inputs:
    X.append(img_as_float(im))
    Y.append(0)

for im in printed_inputs:
    X.append(img_as_float(im))
    Y.append(1)

for im in noise_inputs:
    X.append(img_as_float(im))
    Y.append(2)


X = np.array(X)
Y = np.array(Y)
print("Done!")

pickle.dump(X, open("models/featureMatrix.sav", "wb"), protocol=4)
pickle.dump(Y, open("models/Yarray.sav", "wb"), protocol=4)
print("Dumped arrays!")
'''
X = pickle.load(open("models/featureMatrix.sav", "rb"))
Y = pickle.load(open("models/Yarray.sav", "rb"))

Y = to_categorical(Y)
X = X.reshape(X.shape[0], 50, 50, 1).astype("float32")

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.3, shuffle=True)


classifier = Sequential()
classifier.add(Conv2D(32, (3, 3), input_shape=INPUT_SHAPE, activation='relu'))
classifier.add(Dropout(0.1))
classifier.add(MaxPool2D(pool_size=(2, 2)))
classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(Dropout(0.1))
classifier.add(MaxPool2D(pool_size=(2, 2)))
classifier.add(Flatten())
classifier.add(Dense(50, activation='relu'))
classifier.add(Dropout(0.2))
classifier.add(Dense(3))
classifier.add(Activation('softmax'))

classifier.compile(loss=keras.losses.categorical_crossentropy,
                   optimizer=keras.optimizers.Adam(),
                   metrics=['accuracy'])

print(classifier.summary())
plot_model(classifier, to_file='model.png')

train_gen = ImageDataGenerator(rotation_range=8,
                               width_shift_range=0.08,
                               shear_range=0.3,
                               height_shift_range=0.08,
                               zoom_range=0.08)
test_gen = ImageDataGenerator()
training_set = train_gen.flow(X_train, y_train, batch_size=64)
test_set = train_gen.flow(X_test, y_test, batch_size=64)
history = classifier.fit_generator(training_set,
                         steps_per_epoch=X_train.shape[0]//64,
                         validation_data=test_set,
                         validation_steps=X_test.shape[0]//64,
                         epochs=20)


# Plot statistics:
'''
# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# End statistics plot
'''
pickle.dump(classifier, open("models/cnn.modelsav", "wb"))