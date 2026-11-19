from app.conversation import Conversation

def main():
    bot = Conversation()
    print("\n" + "=" * 50 + "\n" + "Littlebot AI Chatbot\n" + "=" * 50 + "\n\nType 'exit' to quit the chatbot.\n" + "-" * 50 + "\n")

    while True:

        try:
            user_message = input("\nYou: ")

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