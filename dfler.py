import requests
from alive_progress import alive_bar
import time
import os
from os import system, name
from parse import read_file

API_URL = "https://api-inference.huggingface.co/models/swardiantara/droner"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def menu():
    clear_screen()
    print("\t\t====================================================================\n")
    print("\t\t================ Drone Flight Log Entity Recognizer ================\n")
    print("\t\t====================================================================\n\n")
    print("\t\tAction to perform:\n")
    print("\t\t\t1. Evidence Checking\n")
    print("\t\t\t2. Forensic Timeline Construction\n")
    print("\t\t\t3. Drone Entity Recognition\n")
    print("\t\t\t4. Forensic Report Generation\n")
    print("\t\t\t0. Exit\n\n")
    option = input("\t\tEnter option: ")
    return option


def main():
    start = menu()
    if start == '0':
        print("Exit program...")
        time.sleep(2)
        return 0
    while start != '0':
        start = menu()
        if start == '0':
            print("Exit program...")
            time.sleep(1)
            return 0
            break
        elif start == '1':
            clear_screen()
            print('Evidence checking in process...\n')
            time.sleep(1)
            
            files = os.listdir('data')
            files = [f for f in files if os.path.isfile('data'+'/'+f)] #Filtering only the files.
            
            if(len(files) == 0):
                print('No found files in the evidence folder!')
                time.sleep(1)
            else:
                print('Finish checking evidence')
                time.sleep(1)
                print('Found files: ')
                print(*files, sep="\n")
                time.sleep(1)
            input("Press enter to continue...")
        elif start == '2':
            clear_screen()
            print('Forensic construction is in process...\n')
            full_path = os.path.join(os.getcwd(), 'data')
            os.chdir(full_path)

            for filename in os.listdir():
                print("Extracting file: %s" % filename)
                read_file(full_path, filename)
                print("Finish Extracting file: %s\n" % filename)
            input("Press enter to continue...")
        elif start == '3':
            print('choose 3')
            input("Press enter to continue...")
        elif start == '4':
            print('choose 4')
            input("Press enter to continue...")
        else:
            print('Invalid option!')
            input("Press enter to continue...")
    # Setiap progress, print apa proses nya, dan bagaimana progress nya.
    # print("================ Detecting entities in log messages\n")
    # for total in 5000, 7000, 4000, 0:
    #     with alive_bar(total) as bar:
    #         for _ in range(5000):
    #             time.sleep(.001)
    #             bar()
    # payload = {
    #     "inputs": "Aircraft is returning to the Home Point. Minimum RTH Altitude is 30m. You can reset the RTH Altitude in Remote Controller Settings after cancelling RTH.",
    # }
    # output = query({
    #     "inputs": "Aircraft is returning to the Home Point. Minimum RTH Altitude is 30m. You can reset the RTH Altitude in Remote Controller Settings after cancelling RTH.",
    # })
    # print("================ Finish Detecting entities in log messages\n")

if __name__ == "__main__":
    main()