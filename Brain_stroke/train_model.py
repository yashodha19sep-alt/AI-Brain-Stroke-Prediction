import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
from sklearn.metrics import classification_report

# ========================
# PATHS
# ========================
train_dir = 'Brain_Stroke_CT-SCAN_image/Train'
val_dir = 'Brain_Stroke_CT-SCAN_image/Validation'
test_dir = 'Brain_Stroke_CT-SCAN_image/Test'

IMG_SIZE = (224, 224)
BATCH_SIZE = 10
EPOCHS = 25

# ========================
# DATA GENERATORS
# ========================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

val_data = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)
# ========================
# CLASS WEIGHTS (HANDLE IMBALANCE)
# ========================
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_data.classes),
    y=train_data.classes
)

class_weights = dict(enumerate(class_weights))
print("Class Weights:", class_weights)

# ========================
# MODEL (MobileNetV2)
# ========================
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze most layers, train last layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

for layer in base_model.layers[-30:]:
    layer.trainable = True

# Custom head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
predictions = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# ========================
# COMPILE (IMPORTANT TWEAK)
# ========================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),  # 🔥 lower LR
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ========================
# CALLBACKS (VERY IMPORTANT)
# ========================
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=2,
    min_lr=1e-6,
    verbose=1
)

# ========================
# TRAIN
# ========================
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr]
)

# ========================
# TEST EVALUATION
# ========================
test_data = val_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

loss, accuracy = model.evaluate(test_data)
print(f"Test Accuracy: {accuracy*100:.2f}%")

# ========================
# SAVE MODEL
# ========================
model.save("brain_stroke_model.h5")
print("✅ Model saved as brain_stroke_model.h5")
preds = model.predict(test_data)
pred_labels = (preds > 0.5).astype(int)

print(classification_report(test_data.classes, pred_labels))
