import time
import requests
from pushyy import RemoteMessage, process_background_messages

def my_background_callback(data: RemoteMessage) -> None:
    # ..your code goes here..
    """
    One of the things you can do here: Mark a chat message
    as delivered by making a request to your server
    """
    print(data)
    

if __name__ == '__main__':
    for _ in range(3):
        try:
            process_background_messages(my_background_callback)
        except Exception as e:
            # Meh, run the loop again xD
            print(e)
        time.sleep(0.1)
