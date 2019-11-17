import os
from keras import layers
from keras import models
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.xception import Xception
from keras.applications.inception_v3 import InceptionV3
from keras.applications.densenet import DenseNet121
from keras.applications.nasnet import NASNetLarge
#from keras_applications.efficientnet import EfficientNetB0
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.resnet import ResNet50
from keras.applications.resnet import ResNet101
from keras_applications.resnext import ResNeXt50
from keras_applications.resnext import ResNeXt101
from keras.layers.normalization import BatchNormalization
from keras.layers import Dense, Input, Conv2D, MaxPooling2D, GlobalAveragePooling2D, GlobalMaxPooling2D, Flatten, Activation, Dropout
from keras.models import Model
from keras import backend as K

'Methods for building blocks with dropout and BN'
def conv_block(units, dropout=0.2, activation='relu', block=1, layer=1):

    def layer_wrapper(inp):
        x = Conv2D(units, (3, 3), padding='same', name='block{}_conv{}'.format(block, layer))(inp)
        x = BatchNormalization(name='block{}_bn{}'.format(block, layer))(x)
        x = Activation(activation, name='block{}_act{}'.format(block, layer))(x)
        x = Dropout(dropout, name='block{}_dropout{}'.format(block, layer))(x)
        return x

    return layer_wrapper

def dense_block(units, dropout=0.2, activation='relu', name='fc1'):

    def layer_wrapper(inp):
        x = Dense(units, name=name)(inp)
        x = BatchNormalization(name='{}_bn'.format(name))(x)
        x = Activation(activation, name='{}_act'.format(name))(x)
        x = Dropout(dropout, name='{}_dropout'.format(name))(x)
        return x

    return layer_wrapper


def VGG16_Model(nbr_classes, in_shape):

    return VGG16(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def VGG16_BN(nbr_classes, input_shape=None, conv_dropout=0.0, dropout=0.3, activation='relu'):
    """Instantiates the VGG16 architecture with Batch Normalization

    # Arguments
        input_tensor: Keras tensor (i.e. output of `layers.Input()`) to use as image input for the model.
        input_shape: shape tuple
        classes: optional number of classes to classify images

    # Returns
        A Keras model instance.
    """
    print(input_shape)
    img_input = Input(shape=input_shape)

    # Block 1
    x = conv_block(64, dropout=conv_dropout, activation=activation, block=1, layer=1)(img_input)
    x = conv_block(64, dropout=conv_dropout, activation=activation, block=1, layer=2)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = conv_block(128, dropout=conv_dropout, activation=activation, block=2, layer=1)(x)
    x = conv_block(128, dropout=conv_dropout, activation=activation, block=2, layer=2)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = conv_block(256, dropout=conv_dropout, activation=activation, block=3, layer=1)(x)
    x = conv_block(256, dropout=conv_dropout, activation=activation, block=3, layer=2)(x)
    x = conv_block(256, dropout=conv_dropout, activation=activation, block=3, layer=3)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = conv_block(512, dropout=conv_dropout, activation=activation, block=4, layer=1)(x)
    x = conv_block(512, dropout=conv_dropout, activation=activation, block=4, layer=2)(x)
    x = conv_block(512, dropout=conv_dropout, activation=activation, block=4, layer=3)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = conv_block(512, dropout=conv_dropout, activation=activation, block=5, layer=1)(x)
    x = conv_block(512, dropout=conv_dropout, activation=activation, block=5, layer=2)(x)
    x = conv_block(512, dropout=conv_dropout, activation=activation, block=5, layer=3)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)

    # Flatten
    x = GlobalAveragePooling2D()(x)

    # FC Layers
    x = dense_block(4096, dropout=dropout, activation=activation, name='fc1')(x)
    x = dense_block(4096, dropout=dropout, activation=activation, name='fc2')(x)
    
    # Classification block    
    y = Dense(nbr_classes, activation='softmax', name='predictions')(x)

    # Create model.
    return Model(img_input, y, name='vgg16_bn')
    

def VGG19_Model(nbr_classes, in_shape):

    return VGG19(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def Xception_Model(nbr_classes, in_shape):

    return Xception(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def Inception_Model(nbr_classes, in_shape):

    return InceptionV3(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def DenseNet_Model(nbr_classes, in_shape):

    return DenseNet121(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def NASNet_Model(nbr_classes, in_shape):

    return NASNetLarge(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def Inception_ResNet_Model(nbr_classes, in_shape):

    return Inception_ResNet_V2(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

'''
def EfficientNet_Model(nbr_classes, in_shape):

    return EfficientNetB0(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)
'''

def ResNet50_Model(nbr_classes, in_shape):

    return ResNet50(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def ResNet101_Model(nbr_classes, in_shape):

    return ResNet101(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def ResNeXt50_Model(nbr_classes, in_shape):

    return ResNeXt50(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

def ResNeXt101_Model(nbr_classes, in_shape):

    return ResNeXt101(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

'Add other models below'
