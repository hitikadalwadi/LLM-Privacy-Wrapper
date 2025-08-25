# LLM-Privacy-Wrapper
Designed to protect sensitive information when interacting with Large Language Models (LLMs). It allows you to encode sensitive words or phrases in your input text with innocent replacements before sending it to the LLM, and then decode the LLM's response to restore the original sensitive information.

## Overview

The `LLMPrivacyWrapper` class provides the following functionalities:

-   **Encoding:** Replaces sensitive words/phrases in the input text with predefined innocent alternatives.
-   **Decoding:** Restores the original sensitive words/phrases in the LLM's response.
-   **LLM Interaction:**  Provides a method to send the encoded text to an LLM (using the OpenAI API) and decode the response.
## Usage

1.  **Import the Class**

    ```python
    from llm_privacy_wrapper import LLMPrivacyWrapper
    ```

2.  **Initialize the Wrapper**

    Create an instance of the `LLMPrivacyWrapper` class, providing a dictionary that maps sensitive words/phrases to their replacements.

    ```python
    replacement_map = {
        "Hogwarts": "Hogsmith State Secondary School",
        "Albus Dumbledore": "Merlin",
        "Ministry of Magic": "London Bureau of Immigration and Statistics"
    }

    my_wrapper = LLMPrivacyWrapper(replacement_map)
    ```

3.  **Encoding Text**

    Use the `encode` method to replace sensitive words/phrases in your input text.

    ```python
    text = "Important information for all employees of Hogwarts."
    encoded_text = my_wrapper.encode(text)
    print(encoded_text)
    # Output: Important information for all employees of Hogsmith State Secondary School.
    ```

4.  **Decoding Text**

    Use the `decode` method to restore the original sensitive words/phrases in the LLM's response.

    ```python
    encoded_response = "The headmaster of Hogsmith State Secondary School is Merlin."
    decoded_response = my_wrapper.decode(encoded_response)
    print(decoded_response)
    # Output: The headmaster of Hogwarts is Albus Dumbledore.
    ```

5.  **Interacting with the LLM**

    Use the `answer_with_llm` method to send the encoded text to the LLM and decode the response. This method requires an OpenAI client and the model name.

    ```python
    import os
    from openai import OpenAI

    # Load API key from file (or set as environment variable)
    with open("nebuis_api.txt", "r") as file:
        nebuis_api_key = file.read().strip()

    os.environ["NEBIUS_API_KEY"] = nebuis_api_key

    client = OpenAI(
        base_url="https://api.studio.nebius.ai/v1/",  # Replace with your API endpoint
        api_key=os.environ.get("NEBIUS_API_KEY"),
    )

    model = "meta-llama/Meta-Llama-3.1-70B-Instruct"  # Replace with your desired model

    prompt = "Tell me about Hogwarts and Albus Dumbledore."
    result = my_wrapper.answer_with_llm(prompt, client=client, model=model)
    print(result)
    ```
