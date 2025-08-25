# LLM-Privacy-Wrapper
Designed to protect sensitive information when interacting with Large Language Models (LLMs). It allows you to encode sensitive words or phrases in your input text with innocent replacements before sending it to the LLM, and then decode the LLM's response to restore the original sensitive information.

## Overview

The `LLMPrivacyWrapper` class provides the following functionalities:

-   **Encoding:** Replaces sensitive words/phrases in the input text with predefined innocent alternatives.
-   **Decoding:** Restores the original sensitive words/phrases in the LLM's response.
-   **LLM Interaction:**  Provides a method to send the encoded text to an LLM (using the OpenAI API) and decode the response.

## Installation

No specific installation is required as the code is self-contained.  Ensure you have the following dependencies installed:

```bash
pip install openai
