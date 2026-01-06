import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



def load_quickdraw_data(data_dir='data/quickdraw', max_samples_per_class=10000):
    """
    Load and preprocess QuickDraw data
    Args:
        data_dir: Directory containing .npy files
        max_samples_per_class: Maximum samples to use per class
    Returns:
        X: Image data (n_samples, 28, 28, 1)
        y: Labels (n_samples,)
        class_names: List of class names
    """
    X = []
    y = []
    class_names = []
    
    # Get all .npy files
    npy_files = [f for f in os.listdir(data_dir) if f.endswith('.npy')]
    npy_files.sort()
    
    for idx, filename in enumerate(npy_files):
        class_name = filename.replace('.npy', '')
        class_names.append(class_name)
        
        filepath = os.path.join(data_dir, filename)
        data = np.load(filepath)
        
        # Limit samples
        data = data[:max_samples_per_class]
        
        # Reshape: QuickDraw is (n_samples, 784) -> (n_samples, 28, 28)
        data = data.reshape(-1, 28, 28)
        
        # Normalize to 0-1 range
        data = data.astype('float32') / 255.0
        
        # Add channel dimension: (n_samples, 28, 28, 1)
        data = np.expand_dims(data, axis=-1)
        
        X.append(data)
        y.append(np.full(len(data), idx))
        
        print(f"Loaded {len(data)} samples of {class_name}")
    
    # Concatenate all classes
    X = np.concatenate(X, axis=0)
    y = np.concatenate(y, axis=0)
    
    print(f"\nTotal samples: {len(X)}")
    print(f"Number of classes: {len(class_names)}")
    print(f"Image shape: {X[0].shape}")
    
    return X, y, class_names

def prepare_data(X, y, test_size=0.2, val_size=0.1):
    """
    Split data into train, validation, and test sets
    """
    # First split: train+val and test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Second split: train and val
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_size/(1-test_size), 
        random_state=42, stratify=y_train_val
    )
    
    print(f"\nTrain samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)

def create_model(input_shape=(28, 28, 1), num_classes=20):
    """
    Create CNN model for drawing recognition
    """
    model = keras.Sequential([
        # First Conv Block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second Conv Block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third Conv Block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.25),
        
        # Dense Layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def compile_model(model, learning_rate=0.001):
    """
    Compile the model with optimizer and loss
    """
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    return model


def create_data_generators(X_train, y_train, X_val, y_val, batch_size=32):
    """
    Create data generators with augmentation
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        fill_mode='nearest'
    )
    
    # No augmentation for validation
    val_datagen = ImageDataGenerator()
    
    train_generator = train_datagen.flow(
        X_train, y_train,
        batch_size=batch_size,
        shuffle=True
    )
    
    val_generator = val_datagen.flow(
        X_val, y_val,
        batch_size=batch_size,
        shuffle=False
    )
    
    return train_generator, val_generator

def train_model(model, train_data, val_data, epochs=50, batch_size=32, 
                use_generator=False, callbacks=None):
    """
    Train the model
    """
    if use_generator:
        X_train, y_train = train_data
        X_val, y_val = val_data
        train_gen, val_gen = create_data_generators(
            X_train, y_train, X_val, y_val, batch_size
        )
        
        steps_per_epoch = len(X_train) // batch_size
        validation_steps = len(X_val) // batch_size
        
        history = model.fit(
            train_gen,
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            validation_data=val_gen,
            validation_steps=validation_steps,
            callbacks=callbacks,
            verbose=1
        )
    else:
        X_train, y_train = train_data
        X_val, y_val = val_data
        
        history = model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
    
    return history

def create_callbacks(model_save_path='models/drawing_model.h5', 
                     checkpoint_dir='checkpoints'):
    """
    Create training callbacks
    """
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    
    callbacks = [
        # Save best model
        keras.callbacks.ModelCheckpoint(
            filepath=model_save_path,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Reduce learning rate on plateau
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        
        # Early stopping
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # TensorBoard (optional)
        # keras.callbacks.TensorBoard(log_dir='logs')
    ]
    
    return callbacks

def save_class_names(class_names, filepath='models/class_names.json'):
    """
    Save class names to JSON file
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(class_names, f, indent=2)
    
    print(f"Class names saved to {filepath}")


def main():
    """
    Main training pipeline
    """
    print("=" * 50)
    print("Starting Model Training")
    print("=" * 50)
    
    # Configuration
    DATA_DIR = 'data/quickdraw'
    MODEL_PATH = 'models/drawing_model.h5'
    CLASS_NAMES_PATH = 'models/class_names.json'
    MAX_SAMPLES_PER_CLASS = 10000
    EPOCHS = 50
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001
    USE_AUGMENTATION = True
    
    # Step 1: Load data
    print("\n[1/6] Loading data...")
    X, y, class_names = load_quickdraw_data(
        DATA_DIR, 
        max_samples_per_class=MAX_SAMPLES_PER_CLASS
    )
    
    # Step 2: Prepare train/val/test splits
    print("\n[2/6] Preparing data splits...")
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = prepare_data(X, y)
    
    # Step 3: Create model
    print("\n[3/6] Creating model...")
    model = create_model(input_shape=(28, 28, 1), num_classes=len(class_names))
    model = compile_model(model, learning_rate=LEARNING_RATE)
    
    # Print model summary
    model.summary()
    
    # Step 4: Create callbacks
    print("\n[4/6] Setting up callbacks...")
    callbacks = create_callbacks(MODEL_PATH)
    
    # Step 5: Train model
    print("\n[5/6] Training model...")
    history = train_model(
        model,
        (X_train, y_train),
        (X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        use_generator=USE_AUGMENTATION,
        callbacks=callbacks
    )
    
    # Step 6: Evaluate on test set
    print("\n[6/6] Evaluating on test set...")
    test_loss, test_accuracy, test_top3 = model.evaluate(
        X_test, y_test, verbose=1
    )
    
    print(f"\nTest Accuracy: {test_accuracy:.4f}")
    print(f"Test Top-3 Accuracy: {test_top3:.4f}")
    
    # Save class names
    save_class_names(class_names, CLASS_NAMES_PATH)
    
    # Save final model (even if not best)
    model.save(MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")
    
    print("\n" + "=" * 50)
    print("Training Complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()