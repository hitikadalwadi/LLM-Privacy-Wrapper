import re
from typing import Callable
import os
from openai import OpenAI

with open("nebuis_api.txt", "r") as file:
    nebuis_api_key = file.read().strip()

os.environ["NEBIUS_API_KEY"] = nebuis_api_key


class LLMPrivacyWrapper:
    def __init__(self, replacement_map: dict):
        """
        Initializes the wrapper with a mapping of words to their replacements.

        replacement_map: Dictionary where keys are sensitive words and values are their innocent replacements.
        """
        self.replacement_map = replacement_map
        self.reverse_map = {v: k for k, v in replacement_map.items()}  # Reverse for decoding

    def encode(self, text: str) -> str:
        """
        Replaces sensitive words and phrases with innocent alternatives.
        Handles both single words and multi-word phrases.
        Preserves all formatting, punctuation, spacing, and newlines.

        :param text: Input text containing sensitive words/phrases.
        :return: Encoded text with innocent replacements.
        """
        # Sort replacement keys by length (longest first) to handle multi-word phrases first
        sorted_keys = sorted(self.replacement_map.keys(), key=len, reverse=True)

        result = text
        for key in sorted_keys:
            replacement = self.replacement_map[key]

            # Create regex pattern for exact phrase matching with word boundaries
            if ' ' in key:  # Multi-word phrase
                # Escape special regex characters and replace spaces with \s+ to handle multiple spaces
                escaped_key = re.escape(key).replace(r'\ ', r'\s+')
                pattern = r'\b' + escaped_key + r'\b'
            else:  # Single word
                pattern = r'\b' + re.escape(key) + r'\b'

            # Case-insensitive matching with case preservation
            def replace_match(match):
                matched_text = match.group(0)
                print(f"Encoding: '{matched_text}' -> '{replacement}'")

                # Try to preserve case pattern for single words
                if ' ' not in key and ' ' not in replacement:
                    if matched_text.isupper():
                        return replacement.upper()
                    elif matched_text.istitle():
                        return replacement.title()
                    elif matched_text.islower():
                        return replacement.lower()

                return replacement

            result = re.sub(pattern, replace_match, result, flags=re.IGNORECASE)

        return result

    def decode(self, text: str) -> str:
        """
        Restores original sensitive words and phrases in the text.
        Handles both single words and multi-word phrases.
        Preserves all formatting, punctuation, spacing, and newlines.

        :param text: Encoded text with innocent replacements.
        :return: Decoded text with original words/phrases restored.
        """
        # Sort reverse_map keys by length (longest first) to handle multi-word phrases first
        sorted_keys = sorted(self.reverse_map.keys(), key=len, reverse=True)

        result = text
        for key in sorted_keys:
            original = self.reverse_map[key]

            # Create regex pattern for exact phrase matching with word boundaries
            if ' ' in key:  # Multi-word phrase
                # Escape special regex characters and replace spaces with \s+ to handle multiple spaces
                escaped_key = re.escape(key).replace(r'\ ', r'\s+')
                pattern = r'\b' + escaped_key + r'\b'
            else:  # Single word
                pattern = r'\b' + re.escape(key) + r'\b'

            # Case-insensitive matching with case preservation
            def replace_match(match):
                matched_text = match.group(0)
                print(f"Decoding: '{matched_text}' -> '{original}'")

                # Try to preserve case pattern for single words
                if ' ' not in key and ' ' not in original:
                    if matched_text.isupper():
                        return original.upper()
                    elif matched_text.istitle():
                        return original.title()
                    elif matched_text.islower():
                        return original.lower()

                return original

            result = re.sub(pattern, replace_match, result, flags=re.IGNORECASE)

        return result

    def answer_with_llm(self, text: str, client, model: str) -> str:
        """
        Encodes text, sends it to the LLM, and then decodes the response.

        :param text: The original input text.
        :param client: OpenAI client instance.
        :param model: Model name to use.
        :return: The final processed text with original words restored.
        """
        # Step 1: Encode the text (replace sensitive words)
        encoded_text = self.encode(text)
        print(f"Original: {text}")
        print(f"Encoded: {encoded_text}")

        # Step 2: Send encoded text to the actual LLM
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": encoded_text
                    }
                ]
            )
            llm_response = completion.choices[0].message.content
            print(f"LLM Response: {llm_response}")

        except Exception as e:
            print(f"Error calling LLM: {e}")
            return f"Error: {str(e)}"

        # Step 3: Decode the response (restore original words)
        decoded_response = self.decode(llm_response)
        print(f"Final Decoded: {decoded_response}")

        return decoded_response


my_wrapper = LLMPrivacyWrapper(
    {"Hogwarts": "Hogsmith State Secondary School",
     "Albus Dumbledore": "Merlin",
     "Ministry of Magic": "London Bureau of Immigration and Statistics"}
)

prompt = """Edit the following announcement in a natural and supportive English.
Add some appropriate emoji to liven up the message. Explain your edits.

Human Resource Department

Important information for all employees

Dear workers of Hogwarts,

We must inform you of many issues which are now of importance. Hogwarts, as you all know, still under the leadership of Albus Dumbledore, even if sometimes it feels like rules do not apply here. However, as the Ministry of Magic keeps reminding us, we have responsibilities, and therefore you must pay attention.

First of all, Ministry of Magic people are coming. They will do inspection for checking on safety and teaching. This is requirement, do not argue. They will be in all classrooms and dungeons. If you are hiding things you should not have, better to do something about it now, before they see.

Second, regarding House-Elves. We see again that some staff are using them in magical experiments. This is not allowed! Stop doing this, or we will be forced to write reports. Albus Dumbledore says this is “highly inappropriate,” and honestly, so do we.

This is all. Try not to make more problems.

— Hogwarts HR Office
"""

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY"),
)

model = "meta-llama/Meta-Llama-3.1-70B-Instruct"

result = my_wrapper.answer_with_llm(prompt,
                                    client=client, model=model)

print(result)

# Debug
encoded_prompt = my_wrapper.encode(prompt)

print(encoded_prompt)

decoded_prompt = my_wrapper.decode(encoded_prompt)

print("Original prompt:", repr(prompt))
print("Encoded prompt:", repr(encoded_prompt))
print("Decoded prompt:", repr(decoded_prompt))
print("Are they equal?", decoded_prompt == prompt)