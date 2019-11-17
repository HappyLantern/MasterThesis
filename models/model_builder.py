import nn_models
from keras import optimizers
import pickle

class ModelBuilder():

    def __init__(self, model_name, classes, input_shape=(128, 128, 3)):
        self.model_name  = model_name
        self.classes     = classes
        self.input_shape = input_shape
        self.__build_model__()
        
    def __build_model__(self):
        
        self.model = None
        if self.model_name == 'vgg16':
            self.model = nn_models.VGG16_Model(len(self.classes), self.input_shape)
        if self.model_name == 'vgg16bn':
            self.model = nn_models.VGG16_BN(len(self.classes), self.input_shape)
        if self.model_name == 'vgg19':
            self.model = nn_models.VGG19_Model(len(self.classes), self.input_shape)
        if self.model_name == 'xception':
            self.model = nn_models.Xception_Model(len(self.classes), self.input_shape)
        if self.model_name == 'inception_v3':
            self.model = nn_models.Inception_V3_Model(len(self.classes), self.input_shape)
        if self.model_name == 'densenet':
            self.model = nn_models.DenseNet_Model(len(self.classes), self.input_shape)
        if self.model_name == 'nasnet':
            self.model = nn_models.NASNet_Model(len(self.classes), self.input_shape)
        if self.model_name == 'efficientnet':
            self.model = nn_models.EfficientNet_Model(len(self.classes), self.input_shape)
        if self.model_name == 'inception_resnet_v2':
            self.model = nn_models.Inception_ResNet_V2_Model(len(self.classes), self.input_shape)
        if self.model_name == 'ResNet50':
            self.model = nn_models.ResNet50_Model(len(self.classes), self.input_shape)
        if self.model_name == 'ResNet101':
            self.model = nn_models.ResNet101_Model(len(self.classes), self.input_shape)
        if self.model_name == 'ResNeXt50':
            self.model = nn_models.ResNeXt50_Model(len(self.classes), self.input_shape)
        if self.model_name == 'ResNeXt101':
            self.model = nn_models.ResNeXt101_Model(len(self.classes), self.input_shape)
        
        'Add all models here'

    def compile_model(self, metrics, optimizer='RMSProp', learning_rate=1e-3, loss='categorical_crossentropy'):
        'Parameters for model'
        
        'lr, rho'
        if optimizer == 'RMSProp':
            self.model.compile(optimizer=optimizers.RMSprop(learning_rate),
                               loss=loss,
                               metrics=metrics)
        'lr, beta_1, beta_2, amsgrad'
        if optimizer == 'Adam':
            self.model.compile(optimizer=optimizers.Adam(learning_rate), 
                               loss=loss, 
                               metrics=metrics)
            
        'lr, decay, momentum, nesterov'
        if optimizer == 'SGD':
            self.model.compile(optimizer=optimizers.SGD(learning_rate, momentum=0.9),
                               loss=loss,
                               metrics=metrics)
            
    def predict(self, test_gen, steps):
        predictions = self.model.predict_generator(test_gen, steps, verbose=1)
        return predictions

    def fit_model(self, train_gen, val_gen, callbacks, epochs=30, steps_per_epoch=50, val_steps_per_epoch=50):
        'Fits model, returns training history'
        
        self.model.summary()
        history = self.model.fit_generator(train_gen, 
                                           validation_data = val_gen,
                                           steps_per_epoch=steps_per_epoch,
                                           epochs=epochs,
                                           validation_steps=val_steps_per_epoch,
                                           callbacks=callbacks)
        self.history = history
        return history.history

    def print_model(self):
        pass
    
    def evaluate(self, test_gen, steps):
        scores = self.model.evaluate_generator(test_gen,
                            steps=steps, verbose=1)
        return scores
    
    def load_weights(self, weights):
        self.model.load_weights(weights)

    def save_model(self):
        
        self.model.save('multiclass.h5')
        with open('trainHistoryDict', 'wb') as file_pi:
            pickle.dump(self.history.history, file_pi)

    def print_summary(self):
        self.model.summary()


