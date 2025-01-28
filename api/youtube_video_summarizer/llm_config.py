from langchain_groq import ChatGroq


def initialize_groq() -> ChatGroq:
    return ChatGroq(
        # model by meta -> model limits (https://console.groq.com/settings/limits)
        model="llama-3.1-8b-instant",
        # temperature is a parameter of the model which controls the randomness of the outputs. Higher temp = more random, lower temp = more predictable.
        temperature=0.3,
        max_retries=2,
        max_tokens=100,
        # other params...
    )
