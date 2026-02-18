from dotenv import load_dotenv

from delivery_agent import VoronAgent

load_dotenv()


def main():
    agent = VoronAgent()
    print("--- VoronCo Agent Online ---")

    while True:
        text = input("\nYou: ")
        if text.lower() in ["exit", "close"]: break

        print("\nAgent:", agent.answer(text))


if __name__ == "__main__":
    main()