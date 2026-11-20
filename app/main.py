from app.conversation import Conversation
from speech.stt_provider import SpeechToTextProvider
from audio.microphone import Microphone
from audio.speaker import Speaker
from config.settings import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS

mic = Microphone(sample_rate=AUDIO_SAMPLE_RATE, channels=AUDIO_CHANNELS)
speaker = Speaker(volume=0.8)
stt_provider = SpeechToTextProvider()
audio_file_path = "recording.wav"

def main():
    bot = Conversation()
    print("\n" + "=" * 50 + "\n" + "Littlebot AI Chatbot\n" + "=" * 50 + "\n\nType 'exit' to quit the chatbot.\n" + "-" * 50 + "\n")

    while True:

        try:
            input("Press ENTER to start recording...")
            mic.start_recording()
            input()
            mic.stop_recording("recording.wav")
            
            
            user_message = stt_provider.transcribe(audio_file_path)

            print(f"\nYou: {user_message}\n")

            if user_message.lower() == "exit":
                print("\nLittlebot: Goodbye!\n")
                break

            if not user_message:
                continue

            response = bot.send_message(user_message)
            print(f"\nLittlebot: {response}\n")

        except KeyboardInterrupt:
            print("\n\nLittlebot: Shutting down...\n")
            break

        except Exception as error:
            print(f"\n\nLittlebot: An error occurred: {error}\n")

if __name__ == "__main__":
    main()