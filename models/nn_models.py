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

def VGG16_Model(nbr_classes, in_shape):

    return VGG16(include_top=True, 
                 weights=None, 
                 input_shape=in_shape, 
                 classes=nbr_classes)

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
