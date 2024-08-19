import eel
import os
from queue import Queue

class ChatBot:
    started = False
    userinputQueue = Queue()

    @staticmethod
    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        return ChatBot.userinputQueue.get()

    @staticmethod
    def close_callback(route, websockets):
        print("Closing application...")
        if not websockets:
            print('Bye!')
            exit()

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        ChatBot.userinputQueue.put(msg)
        print("User input received:", msg)
        eel.addUserMsg(msg)  # Show user input on frontend

    @staticmethod
    def close():
        ChatBot.started = False
        print("ChatBot closed.")

    @staticmethod
    def addUserMsg(msg):
        eel.addUserMsg(msg)

    @staticmethod
    def addAppMsg(msg):
        eel.addAppMsg(msg)

    @staticmethod
    # Ensure that Eel is initialized properly and runs in a separate thread
    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        print("Starting ChatBot from path:", path)

        web_path = os.path.join(path, 'web')
        eel.init(web_path, allowed_extensions=['.js', '.html'])

        try:
            eel.start('index.html', mode='default',
                    host='localhost',
                    port=27005,
                    block=False,
                    size=(350, 480),
                    position=(10, 100),
                    disable_cache=True,
                    close_callback=ChatBot.close_callback)
            ChatBot.started = True
            print("ChatBot started.")

            # Send the initial message to the frontend
            eel.addAppMsg("Hey!! I'm Proton. What would you like to do now?")

            while ChatBot.started:
                try:
                    eel.sleep(10.0)
                except Exception as e:
                    print("Exception in main loop:", e)
                    break

        except Exception as e:
            print("Exception in start method:", e)


if __name__ == "__main__":
    ChatBot.start()
