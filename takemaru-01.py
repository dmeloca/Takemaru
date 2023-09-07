import os
from PIL import Image
import sys
import time
import random

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_tittle():
    tittle = '''
        ███        ▄████████    ▄█   ▄█▄    ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████    ▄████████ ███    █▄  
    ▀█████████▄   ███    ███   ███ ▄███▀   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███ ███    ███ 
       ▀███▀▀██   ███    ███   ███▐██▀     ███    █▀  ███   ███   ███   ███    ███   ███    ███ ███    ███ 
        ███   ▀   ███    ███  ▄█████▀     ▄███▄▄▄     ███   ███   ███   ███    ███  ▄███▄▄▄▄██▀ ███    ███ 
        ███     ▀███████████ ▀▀█████▄    ▀▀███▀▀▀     ███   ███   ███ ▀███████████ ▀▀███▀▀▀▀▀   ███    ███ 
        ███       ███    ███   ███▐██▄     ███    █▄  ███   ███   ███   ███    ███ ▀███████████ ███    ███ 
        ███       ███    ███   ███ ▀███▄   ███    ███ ███   ███   ███   ███    ███   ███    ███ ███    ███ 
       ▄████▀     ███    █▀    ███   ▀█▀   ██████████  ▀█   ███   █▀    ███    █▀    ███    ███ ████████▀  
                               ▀                                                     ███    ███                   '''

    print(f"\033[0;31m{tittle}\033[0m")

def show_menu():
    #type_animation("\033[0;35m[*]\033[0m Listando Opciones")
    print("\033[0;35m[*]\033[0m Listando Opciones")
    print("  \033[1;30m|-[1]\033[0m Imprime imágen por consola")
    print("  \033[1;30m|-[2]\033[0m Esconder un mensaje")
    print("  \033[1;30m|-[3]\033[0m Extraer un mensaje")
    print("  \033[1;30m|-[4]\033[0m Cifrar un mensaje (Cifrado Cesar)")
    print("  \033[1;30m|-[5]\033[0m Descifrar un mensaje (Cifrado Cesar)")
    print("  \033[1;30m|-[6]\033[0m Salir")
    choice = input(f"\033[0;35m[*]\033[0m Ingrese el número de opción: ")
    return choice

def display_image(image_path): 
    while True:
        try:
            image = Image.open(image_path)
            width, height = image.size

            aspect_ratio = height / width
            new_width = 80
            new_height = int(new_width * aspect_ratio)

            resized_image = image.resize((new_width, new_height))
            resized_image = resized_image.convert("L")  # Convierte a escala de grises

            for y in range(new_height):
                for x in range(new_width):
                    pixel_value = resized_image.getpixel((x, y))
                    
                    # Solo muestra un carácter si el píxel no es blanco
                    char = " .:-=+*%@#"[min(pixel_value // 25, 9)] if pixel_value > 25 else " "
                    
                    print(char, end="")
                print()
            
            # Si la imagen se mostró correctamente, sal del bucle
            break
        except FileNotFoundError:
            print(f"\033[7;31m  |-[!]\033[0m Ruta incorrecta. Inténtalo nuevamente.")
            break

def hide_message(image_path, message, path_encoded):
    original_image = Image.open(image_path)
    width, height = original_image.size

    encoded_image = original_image.copy()

    binary_message = ''.join(format(ord(char), '08b') for char in message)

    index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(original_image.getpixel((x, y)))

            for i in range(3):
                if index < len(binary_message):
                    pixel[i] = pixel[i] & 0xFE | int(binary_message[index])
                    index += 1

            encoded_image.putpixel((x, y), tuple(pixel))
    encoded_image.save(path_encoded)
    print(f"\033[0;32m  |-[$]\033[0m Mensaje oculto en la imagen y guardado como '{path_encoded}'.")
    time.sleep(1)

def clean_code_image(image_path, message):
    have_code = check_code(image_path)
    original_image = Image.open(image_path)
    width, height = original_image.size

    encoded_image = original_image.copy()
    message_clean = " " * len(have_code)

    binary_message = ''.join(format(ord(char), '08b') for char in message_clean)

    index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(original_image.getpixel((x, y)))

            for i in range(3):
                if index < len(binary_message):
                    pixel[i] = pixel[i] & 0xFE | int(binary_message[index])
                    index += 1

            encoded_image.putpixel((x, y), tuple(pixel))
    encoded_image.save(image_path)

def hide_message_options(image_path, message, path_encoded):
    while True:
        try:
            have_code = check_code(image_path)
            if len(have_code) == 0:
                try:
                    path_encoded = hide_message(image_path, message, path_encoded) 
                except ValueError:
                    break
            else:
                print(f"\033[7;31m  |-[!]\033[0m La foto ya tiene un mensaje: {have_code}")
                answer = input("\033[0;36m  |-[+]\033[0m ¿Desea continuar?(Y/N)")
                if answer == "Y" or answer == "y":
                    clean_code = input("\033[0;36m  |-[+]\033[0m ¿Desea eliminar el mensaje?(Y/N)")
                    if clean_code == "Y" or clean_code == "y":
                        clean_code_image(image_path, message)
                        path_encode = hide_message(image_path, message, path_encoded)
                        break
                    elif clean_code == "N" or clean_code == "n":
                        print(f"\033[0;36m  |-[+]\033[0m Añadiendo su mensaje al ya existente")
                        message_with_existing_code = have_code + message
                        path_encoded = hide_message(image_path, message_with_existing_code, path_encoded)
                        break
                    else:
                        print("\033[7;31m[!]\033[0m Opción inválida, por favor ingrese un número de opción válido")
                        break
                elif answer == "N" or answer == "n":
                    print("\033[0;36m  |-[-]\033[0m Saliendo")
                    break
                else:
                    print("\033[7;31m[!]\033[0m Opción inválida, por favor ingrese un número de opción válido")

        except FileNotFoundError:
            print("\033[7;31m  |-[!]\033[0m Hubo un error. Inténtalo nuevamente.")
            break
            
def check_code(encoded_image_path):
    while True:
        try:
            encoded_image = Image.open(encoded_image_path)
            width, height = encoded_image.size

            binary_message = ""

            for y in range(height):
                for x in range(width):
                    pixel = list(encoded_image.getpixel((x, y)))

                    for i in range(3):
                        binary_message += str(pixel[i] & 1)

            message = ""
            for i in range(0, len(binary_message), 8):
                char = chr(int(binary_message[i:i+8], 2))
                if char == '\0':
                    break
                message += char
            return message
            time.sleep(1)
            break
        except FileNotFoundError:
            print(f"\033[0;31m  |-[!]\033[0m Ruta incorrecta. Inténtalo nuevamente.")
            break

def retrieve_message(encoded_image_path):
    while True:
        try:
            encoded_image = Image.open(encoded_image_path)
            width, height = encoded_image.size

            binary_message = ""

            for y in range(height):
                for x in range(width):
                    pixel = list(encoded_image.getpixel((x, y)))

                    for i in range(3):
                        binary_message += str(pixel[i] & 1)

            message = ""
            for i in range(0, len(binary_message), 8):
                char = chr(int(binary_message[i:i+8], 2))
                if char == '\0':
                    break
                message += char

            print("\033[0;32m  |-[$]\033[0m Mensaje recuperado:", message)
            time.sleep(1)
            break
        except FileNotFoundError:
            print(f"\033[7;31m  |-[!]\033[0m Ruta incorrecta. Inténtalo nuevamente.")
            break

def caesar_cipher_encrypt(message, rotation):
    try:
        encrypted_message = ""

        for char in message:
            if char.isalpha():  # Ignora caracteres que no son letras
                shift = rotation % 26  # Asegura que el desplazamiento sea dentro del rango de letras
                if char.islower():
                    new_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
                else:
                    new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                encrypted_message += new_char
            else:
                encrypted_message += char
        print("\033[0;32m  |-[$]\033[0m Mensaje cifrado:", encrypted_message)
    except ValueError:
        print("\033[0;31m  |-[!]\033[0m Error: La rotación debe ser un valor entero.")

def caesar_cipher_decrypt(encrypted_message, rotation):
    while True:
        try:
            decrypted_message = ""
            for char in encrypted_message:
                if char.isalpha():  # Ignora caracteres que no son letras
                    shift = rotation % 26  # Asegura que el desplazamiento sea dentro del rango de letras
                    if char.islower():
                        new_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
                    else:
                        new_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
                    decrypted_message += new_char
                else:
                    decrypted_message += char
            print("\033[0;32m  |-[$]\033[0m Mensaje descifrado:", decrypted_message)
            break
        except ValueError:
            print("\033[0;31m  |-[!]\033[0m Error: La rotación debe ser un valor entero.")

def main():
    try: 
        clear_console()  # Borra el contenido de la consola
        show_tittle()
        time.sleep(0.5)
        while True:
            choice = show_menu()
            if choice == "1":
                print("\033[0;36m  |-[+]\033[0m Has seleccionado la opción 1")
                try:
                    image_path = input(f"\033[0;36m  |-[+]\033[0m Image Path: ")  # Ruta de la imagen
                    display_image(image_path)
                except AttributeError:
                    image_path = input(f"\033[0;36m  |-[+]\033[0m Image Path: ")  # Ruta de la imagen
                    display_image(image_path)

            elif choice == "2":
                print("\033[0;36m  |-[+]\033[0m Has seleccionado la opción 2")
                image_path = input("\033[0;36m  |-[+]\033[0m Introduce la ruta de la imagen: ")
                message = input("\033[0;36m  |-[+]\033[0m Introduce el mensaje a ocultar: ")
                encoded_path = input("\033[0;36m  |-[+]\033[0m Introduce la ruta de la imagen con mensaje oculto: ")
                hide_message_options(image_path, message, encoded_path)
            elif choice == "3":
                print("\033[0;36m  |-[+]\033[0m Has seleccionado la opción 3")
                encoded_image_path = input("\033[0;36m  |-[+]\033[0m Introduce la ruta de la imagen con el mensaje oculto: ")
                retrieve_message(encoded_image_path)
            elif choice == "4":
                print("\033[0;36m  |-[+]\033[0m Has seleccionado la opción 4")
                text_to_cypher = input("\033[0;36m  |-[+]\033[0m Introduce el texto que deseas cifrar: ")
                rotation_number = int(input("\033[0;36m  |-[+]\033[0m Introduce el número de letras que deseas rotar el texto: "))
                try:
                    caesar_cipher_encrypt(text_to_cypher, rotation_number)
                except ValueError:
                    print("\033[0;31m  |-[!]\033[0m Error: La rotación debe ser un valor entero.")
            elif choice == "5":
                print("\033[0;36m  |-[+]\033[0m Has seleccionado la opción 4")
                encrypted_text = input("\033[0;36m  |-[+]\033[0m Introduce el texto que deseas descifrar: ")
                rotation_number = int(input("\033[0;36m  |-[+]\033[0m Introduce el número de letras que fue rotado el texto: "))
                try:
                    caesar_cipher_decrypt(encrypted_text, rotation_number)
                except ValueError:
                    print("\033[0;31m  |-[!]\033[0m Error: La rotación debe ser un valor entero.")
            elif choice == "6":
                print("\033[0;31m  [*]\033[0m Saliendo del programa")
                time.sleep(0.5)
                clear_console()
                break
            else:
                print("\033[0;31m[!]\033[0m Opción inválida, por favor ingrese un número de opción válido")
    except KeyboardInterrupt:
        print("\n\033[0;31m¡Ctrl + C detectado! Saliendo...\033[0m")
        time.sleep(0.5)
        clear_console()

if __name__ == "__main__":
    main()
