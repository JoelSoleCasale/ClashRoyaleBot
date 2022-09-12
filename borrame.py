import asyncio, threading


def scheduler():
    print("scheduling...")

def main():

    threading.Timer(2, scheduler).start()

    print('hello world')

main()