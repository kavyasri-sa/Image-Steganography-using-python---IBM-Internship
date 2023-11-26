from PIL import Image

def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def encode_text(image_path, text, output_path):
    binary_text = text_to_binary(text)
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_length = format(len(binary_text), '016b')
    for i in range(16):
        pixel_value = list(pixels[i])
        pixel_value[-1] = int(binary_length[i])
        pixels[i] = tuple(pixel_value)
    for i in range(16, len(pixels)):
        if binary_text:
            pixel_value = list(pixels[i])
            pixel_value[-1] = int(binary_text[0])
            pixels[i] = tuple(pixel_value)
            binary_text = binary_text[1:]
    encoded_img = Image.new('RGB', img.size)
    encoded_img.putdata(pixels)
    encoded_img.save(output_path)
    print(f"Message encoded successfully. Encoded image saved at {output_path}")

def decode_text(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_length = ''.join([str(pixel_value[-1]) for pixel_value in pixels[:16]])
    text_length = int(binary_length, 2)
    binary_text = ''.join([str(pixel_value[-1]) for pixel_value in pixels[16:16+text_length]])
    decoded_text = ''.join([chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)])
    print(f"Decoded message: {decoded_text}")

if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Encode text in an image")
        print("2. Decode text from an image")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice == '1':
            image_path = input("Enter the path of the image file: ")
            text_to_hide = input("Enter the text to hide: ")
            output_image_path = input("Enter the path to save the encoded image: ")
            encode_text(image_path, text_to_hide, output_image_path)
        elif choice == '2':
            image_path = input("Enter the path of the image file: ")
            decode_text(image_path)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
