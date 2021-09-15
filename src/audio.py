import pyttsx3


def text_to_speech(text, gender='Male'):
    """
    Function to convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]

    engine = pyttsx3.init('nsss')

    # Setting up voice rate
    engine.setProperty('rate', 135)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass
        