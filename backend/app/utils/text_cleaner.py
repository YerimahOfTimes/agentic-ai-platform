def clean_output(text):
    unwanted_phrases = [
        "you are a professional",
        "final answer is as follows",
        "assistant who has mastered"
    ]

    for phrase in unwanted_phrases:
        text = text.replace(phrase, "")

    return text.strip()
