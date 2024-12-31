from cryptography.fernet import Fernet
from PIL import Image
import numpy as np

# Function to generate a new encryption key and save it to a file.
def generate_key():
    key = Fernet.generate_key()  # Generate a symmetric encryption key.
    with open("key.key", "wb") as key_file:
        key_file.write(key)  # Write the key to a file for future use.

# Function to load the encryption key from a file.
def load_key():
    return open("key.key", "rb").read()  # Read and return the key from the file.

# Function to encrypt an image file.
def encrypt_image(image_path, encrypt_path):
    # Load the encryption key.
    key = load_key()
    fernet = Fernet(key)  # Initialize Fernet with the key.

    # Read the image file as binary data.
    with open(image_path, "rb") as image_file:
        image = image_file.read()

    # Encrypt the binary data.
    encrypted_image = fernet.encrypt(image)

    # Write the encrypted data to a new file.
    with open(encrypt_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_image)
    
    return encrypted_image  # Return the encrypted data.

# Function to decrypt an encrypted image file.
def decrypt_image(image_path, decrypt_path):
    # Load the encryption key.
    key = load_key()
    fernet = Fernet(key)  # Initialize Fernet with the key.

    # Read the encrypted file as binary data.
    with open(image_path, "rb") as image_file:
        image = image_file.read()

    # Decrypt the binary data.
    decrypted_image = fernet.decrypt(image)

    # Write the decrypted data to a new file.
    with open(decrypt_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_image)

# Function to visualize encrypted binary data as an RGB image.
def visualize_encrypted_data(encrypted_data, output_image_path, grid_size=(100, 100)):
    # Convert the encrypted binary data to a NumPy array of unsigned 8-bit integers.
    data = np.frombuffer(encrypted_data, dtype=np.uint8)

    # Truncate or pad the data to fit the specified grid size.
    data = data[: grid_size[0] * grid_size[1] * 3]
    if len(data) < grid_size[0] * grid_size[1] * 3:
        data = np.pad(data, (0, grid_size[0] * grid_size[1] * 3 - len(data)), mode='constant', constant_values=0)

    # Reshape the data to create an RGB image.
    rgb_data = data.reshape((grid_size[0], grid_size[1], 3))

    # Create an image from the RGB data and save it.
    image = Image.fromarray(rgb_data, 'RGB')
    image.save(output_image_path)
    print(f"Encrypted visualization saved to {output_image_path}")

if __name__ == "__main__":
    # Uncomment the following line to generate a new key (only needed once).
    generate_key()

    # File paths
    original_image = "data/image.png"  # Path to the original image file.
    encrypted_image = "data/encrypted_image.enc"  # Path to save the encrypted file.
    visualization_image = "data/encrypted_visualization.png"  # Path to save the visualization.
    decrypted_image = "data/decrypted_image.png"  # Path to save the decrypted image.

    # Encrypt the image and get the encrypted data.
    encrypted_data = encrypt_image(original_image, encrypted_image)

    # Visualize the encrypted binary data as an image.
    visualize_encrypted_data(encrypted_data, visualization_image)

    # Decrypt the encrypted image back to its original form.
    decrypt_image(encrypted_image, decrypted_image)
