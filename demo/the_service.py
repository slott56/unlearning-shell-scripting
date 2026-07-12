"""
A sample service to start and stop
"""
import time
from math import fmod

def main():
    print("Sample Service")
    while True:
        offset = fmod(time.monotonic(), 2.0)
        time.sleep(offset)
        print(time.asctime())

if __name__ == "__main__":
    main()
