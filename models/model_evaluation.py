model = ModelBuilder(curr_model, classes, input_shape=input_shape)

'Loading the best weights for the trained model to be evaluated'
weight_folder = config['load-weights']['weights_folder']
weights =  config['load-weights']['weights']
model.load_weights(os.path.join(weight_folder, weights))

train_data = os.listdir(train_data_dir)
data_len   = len(train_data)

random.shuffle(train_data)

val_range  = json.loads(config['model-parameters']['val_range'])
train_data = train_data[int(data_len * val_range) + 1:]
val_data   = train_data[:int(data_len * val_range)]

val_datagen = DataGenerator(train_data_dir, val_data, classes, test=True,
                             n_channels=n_channels, dim=data_shape, 
                             batch_size=5)
test_data = os.listdir(test_data_dir)
test_datagen = DataGenerator(test_data_dir, test_data, classes, test=True, 
                            n_channels=n_channels, dim=data_shape, 
                            batch_size=1)
            
'Getting predictions: n_classes probabilities per input'
probabilities = model.predict(test_datagen, 1552)

'Getting the chosen class prediction for each input.'
predicted_class_indices=np.argmax(probabilities, axis=1) # Using argmax as rule, thereby always getting a prediction
prediction = pd.DataFrame(predicted_class_indices, columns=['predictions']).to_csv('vgg_predictions.csv') # Save to CSV

'Getting the actual label for each prediction'
labels = (test_datagen.classes)
predicted_class = [labels[k] for k in predicted_class_indices]

'Getting the true labels for the data predicted on'
#images = os.listdir(test_data_dir)
images = test_data
#images = images[:1500]

true_class         = []
true_class_indices = []
#images = os.listdir(test_data)
for i in range(len(images)):
    for k in range(len(classes)):
        if classes[k] in images[i]:
            true_class_indices.append(k)
            true_class.append(classes[k])

'Getting the count of each true label'
cnt = {}
for c in classes:
    cnt[c] = 0
    
for f in true_class:
    for c in classes:
        if c in f:
            cnt[c] += 1

print(len(true_class), cnt)

'Getting the count of predicted class'
cnt = {}
for c in classes:
    cnt[c] = 0
    
for f in predicted_class:
    for c in classes:
        if c in f:
            cnt[c] += 1

print(len(predicted_class), cnt)

'Check to see that the predicted amount is right'
print(len(true_class), len(predicted_class))
assert len(true_class) == len(predicted_class)

'Confusion matrix for the data'
conf_matrix = confusion_matrix(predicted_class_indices, true_class_indices)
print(conf_matrix)
print(predicted_class[0:10])
print(true_class[0:10])

'Plotting the confusion matrix'
df_cm = pd.DataFrame(conf_matrix, index = [i for i in classes],
                  columns = [i for i in classes])

plt.figure(figsize = (6, 6))
sn.heatmap(df_cm, annot=True)

'Using keras evaluate'
model = ModelBuilder(curr_model, classes, input_shape=input_shape)

'Loading the best weights for the trained model to be evaluated'
weight_folder = config['load-weights']['weights_folder']
weights =  config['load-weights']['weights']
model.load_weights(os.path.join(weight_folder, weights))

model.compile_model(optimizer=optimizer, 
                    loss=loss, 
                    metrics=metrics, 
                    learning_rate=lr)

test_datagen = DataGenerator(test_data_dir, test_data, classes,
                             n_channels=n_channels, dim=data_shape, 
                             batch_size=1, shuffle=False)

val_datagen = DataGenerator(train_data_dir, val_data, classes, 
                            n_channels=n_channels, dim=data_shape, 
                            batch_size=5)


'Testing keras evaluate'
scores = model.evaluate(val_datagen, 113)
print(scores)
