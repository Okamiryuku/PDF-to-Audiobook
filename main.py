import fitz
from google.cloud import texttospeech
from google.oauth2 import service_account


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()
    return text


def text_to_speech(text, output_file="output.mp3", language_code="en-US", voice_name="en-US-Wavenet-D"):
    # Replace 'path/to/your/keyfile.json' with the actual path to your service account key file
    credentials = service_account.Credentials.from_service_account_file('phonic-vortex-404823-8cffe46ce347.json')

    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_file, "wb") as out_file:
        out_file.write(response.audio_content)

    print(f'Audio content written to file "{output_file}"')


pdf_path = "Test PDF-8mb.pdf"
text = extract_text_from_pdf(pdf_path)
text_to_speech(text)
