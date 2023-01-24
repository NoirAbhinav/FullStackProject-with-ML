import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import BatchNormalization
import datetime, os

def Model_generate(X_train, y_train,X_val,y_val, X_test,y_test,width,height,version):
    num_features = 64
    num_labels = 7
    batch_size = 64
    epochs = 40
    print(width,height)
    model = Sequential()
    model.add(Conv2D(num_features, kernel_size=(3, 3), activation='relu', input_shape=(width, height, 1), data_format='channels_last', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
    model.add(Conv2D(num_features, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2),padding='same'))
    model.add(Dropout(0.5))

    model.add(Conv2D(2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2),padding='same'))
    model.add(Dropout(0.5))

    model.add(Conv2D(2*2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(2*2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2),padding='same'))
    model.add(Dropout(0.5))

    model.add(Conv2D(2*2*2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(2*2*2*num_features, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2),padding='same'))
    model.add(Dropout(0.5))

    model.add(Flatten())

    model.add(Dense(2*2*2*num_features, activation='softmax'))
    model.add(Dropout(0.4))
    model.add(Dense(2*2*num_features, activation='softmax'))
    model.add(Dropout(0.4))
    model.add(Dense(2*num_features, activation='softmax'))
    model.add(Dropout(0.5))

    model.add(Dense(num_labels, activation='softmax'))
    model.summary()
    model.compile(loss=tf.keras.losses.categorical_crossentropy,
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
                metrics=['accuracy'])
    lr_reducer = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=3, verbose=1)
    logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)
    early_stopper = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=8, verbose=1, mode='auto')
    checkpointer = tf.keras.callbacks.ModelCheckpoint('/home/abhinav/Personal_project/FullStackProject-with-ML/MLOPS/emotion_detect/models', monitor='val_loss', verbose=1, save_best_only=True)
    model.fit(np.array(X_train), np.array(y_train),
            batch_size=batch_size,
            epochs=epochs,
            verbose=1,
            validation_data=(np.array(X_test), np.array(y_test)),
            shuffle=True,
            callbacks=[lr_reducer, tensorboard_callback, early_stopper, checkpointer])
    model.save(f'/home/abhinav/Personal_project/FullStackProject-with-ML/MLOPS/emotion_detect/models/model_{version}.h5')