# Import the required library
from googletrans import Translator

# Function to translate text
def translate_text():
    # Initialize the Translator
    translator = Translator()

    # Input text from the user
    text = input("Enter the text you want to translate: ")

    # Input the source language (if not specified, will use 'auto' for automatic detection)
    source_language = input("Enter the source language (or press Enter to auto-detect): ")
    if not source_language:
        source_language = 'auto'

    # Input the target language
    target_language = input("Enter the target language: ")

    # Perform the translation
    translation = translator.translate(text, src=source_language, dest=target_language)

    # Output the translated text
    print(f"Translated text ({translation.src} -> {translation.dest}): {translation.text}")

# Run the translator
if __name__ == "__main__":
    translate_text()
