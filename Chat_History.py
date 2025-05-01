def view_chat_history():
    try:
        with open("chat_history.txt", "r") as f:
            print("\n--- Chat History ---\n")
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("No chat history found.")

if __name__ == "__main__":
    view_chat_history()
