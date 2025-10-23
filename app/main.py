import os
import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
from graph import create_chat_graph
import google.generativeai as genai  # ✅ Use the official SDK

load_dotenv()

DB_URI = "mongodb://admin:admin@localhost:27017"
config = {"configurable": {"thread_id": "3"}}

# ======================= TTS Function ======================= #
def speak_with_tts(text: str):
    """
    Uses Gemini 2.5 Pro TTS to convert text to speech.
    Saves the output audio to ./ai_generated/tts_output.wav
    """
    print("\n🔊 Generating TTS audio...")

    os.makedirs("./ai_generated", exist_ok=True)
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-2.5-pro-tts")

    prompt = (
        "You are having a casual conversation with a friend. "
        "Say the following in a friendly and amused way."
    )

    try:
        response = model.generate_audio(
            prompt=prompt,
            text=text,
            voice="Callirhoe",  # speaker/voice choice
            output_format="wav"
        )

        tts_path = "./ai_generated/tts_output.wav"
        with open(tts_path, "wb") as f:
            f.write(response.audio)  # save the raw audio bytes

        print(f"✅ TTS audio saved as: {tts_path}")

    except Exception as e:
        print(f"❌ Error generating TTS: {e}")

# ============================================================ #

def main():
    print("🎙️ LangGraph Voice Chat Initialized. Speak or press Ctrl+C to exit.\n")

    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)

        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Mic ready...")

            while True:
                try:
                    print("\nSay something...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Listening...")
                    audio = recognizer.listen(source)
                    print("Recognizing...")

                    try:
                        user_input = recognizer.recognize_google(audio)
                        print(f"You said: {user_input}")
                    except sr.UnknownValueError:
                        print("❗ Sorry, I couldn’t understand that. Please try again.")
                        continue
                    except sr.RequestError as e:
                        print(f"⚠️ Could not reach Google Speech Recognition service: {e}")
                        continue

                    # Process recognized text through LangGraph
                    for event in graph.stream(
                        {"messages": [{"role": "user", "content": user_input}]},
                        config,
                        stream_mode="values",
                    ):
                        if "messages" in event:
                            event["messages"][-1].pretty_print()

                    # Example TTS response
                    speak_with_tts("hahah I did NOT expect that. Can you believe it!.")

                except KeyboardInterrupt:
                    print("\n👋 Exiting voice chat. Goodbye!")
                    break
                except Exception as e:
                    print(f"⚠️ Unexpected error: {e}")
                    continue


if __name__ == "__main__":
    main()
