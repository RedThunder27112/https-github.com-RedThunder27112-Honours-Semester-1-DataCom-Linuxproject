import time
import subprocess
import sys

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

def text_to_morse(text):
    morse_code = ""
    for char in text.upper():
        if char == ' ':
            morse_code += ' '
        elif char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char] + ' '
    return morse_code.strip()

def play_morse_code(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            # Play a short beep for dot
            subprocess.call(["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif symbol == '-':
            # Play a long beep for dash
            subprocess.call(["paplay", "/usr/share/sounds/freedesktop/stereo/bell.oga"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.3)  # Add a slight pause between dot and dash
        elif symbol == ' ':
            # Pause between characters
            time.sleep(0.4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 MorseCode.py <message>")
        sys.exit(1)

    input_text = sys.argv[1]
    morse_code = text_to_morse(input_text)
    print("\nMorse code:", morse_code)
    play_morse_code(morse_code)
