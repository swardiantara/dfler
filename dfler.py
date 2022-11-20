import requests
import time
import os
from os import system, name
from parse import read_android_log, read_ios_log, construct_timeline
from simpletransformers.ner import NERModel
import pandas as pd

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
            
            files = os.listdir('flight_logs')
            android_logs = []
            ios_logs = []
            folders = [d for d in files if os.path.isdir('flight_logs'+'/'+d)]
            # print(folders)
            if(len(folders) == 0):
                print("No sub-folders in the evidence folder")
            else: 
                for folder in folders:
                    # Filtering only the files.
                    files = os.listdir('flight_logs/'+folder)
                    files = [f for f in files if os.path.isfile('flight_logs/'+folder+'/'+f)]
                    if(folder == 'android'):
                        android_logs.append(files)
                    else:
                        ios_logs.append(files)
            found_files = android_logs + ios_logs
            if(len(found_files) == 0):
                print('No found files in the evidence folder!')
                time.sleep(1)
            else:
                print('Finish checking evidence')
                time.sleep(1)
                print('Found files: \n')
                print('iOS logs: ')
                print(*ios_logs, sep="\n")
                print("\nAndroid logs: \n")
                print(*android_logs, sep="\n")
                time.sleep(1)
            input("Press enter to continue...")
        elif start == '2':
            clear_screen()
            print('Forensic timeline construction is in process...\n')

            # Parse the raw flight logs
            full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flight_logs')

            # Construct the forensic timeline from parsed flight log
            print(full_path)
            # print(os.path.join(dir_path, 'flight_logs'))
            path_list = []
            ios_parsed = False
            android_parsed = False
            for path, subdirs, files in os.walk(full_path):
                if path.find("android") != -1:
                    for filename in os.listdir(path):
                        if filename.find("parsed") != -1:
                            continue
                        print("path: ", path)
                        print("Extracting file: %s" % filename)
                        read_android_log(path, filename)
                        print("Finish Extracting file: %s\n" % filename)
                    android_parsed = True
                    
                elif path.find("ios") != -1:
                    for filename in os.listdir(path):
                        if filename.find("parsed") != -1:
                            continue
                        print("path: ", path)
                        print("Extracting file: %s" % filename)
                        read_ios_log(path, filename)
                        print("Finish Extracting file: %s\n" % filename)
                    ios_parsed = True
                
                if(ios_parsed or android_parsed):
                    for name in files:
                        file_ext = name.split(".")
                        file_ext = file_ext[-1] if len(file_ext) > 1 else ""
                        if(name.find("parsed_") != -1 and file_ext == "csv"):
                            path_list.append(os.path.join(path, name))

            parent_df = pd.DataFrame()
            for path in path_list:
                child_df = pd.read_csv(path, encoding='utf-8')
                parent_df = pd.concat([parent_df, child_df])

            # making copy of team column
            time_col = parent_df["time"].copy()
            parent_df["timestamp"] = parent_df["date"].str.cat(time_col, sep =" ")
            parent_df.drop(columns = ['time', 'date'], inplace=True)
            parent_df = parent_df[['timestamp', 'message']]
            parent_df['timestamp'] = pd.to_datetime(parent_df['timestamp'])
            # Sort the data by timestamp
            parent_df.sort_values(by='timestamp', inplace=True)
            
            parent_df.to_csv('./flight_logs/forensic_timeline.csv', index=False, encoding="utf-8")             
            input("Press enter to continue...")
        elif start == '3':
            clear_screen()
            print('Entity Recognition is in process...\n')
            # Load the fine-tuned model
            print("Loading model...\n")
            droner = NERModel(
                "bert", "outputs", use_cuda=True
            )
            
            # Load the forensic timeline
            print("Loading forensic timeline...\n")
            timeline = pd.read_csv('./flight_logs/forensic_timeline.csv', encoding="utf-8")
            
            print('Recognizing mentioned entities...')
            pred_list = []
            for row in range(0, timeline.shape[0]):
                message = timeline.iloc[row, 1]
                [entities], _ = droner.predict([message])
                timeline.iloc[row, 2]
                pred_list.append(timeline, entities)
            
            generate_report(pred_list)
            input("Press enter to continue...")
        elif start == '4':
            print('Generating forensic report...')

            # Load the NER results
            # ner_result = json.read('')
            input("Press enter to continue...")
        else:
            print('Invalid option!')
            input("Press enter to continue...")
    # Setiap progress, print apa proses nya, dan bagaimana progress nya.
    # payload = {
    #     "inputs": "Aircraft is returning to the Home Point. Minimum RTH Altitude is 30m. You can reset the RTH Altitude in Remote Controller Settings after cancelling RTH.",
    # }
    # output = query({
    #     "inputs": "Aircraft is returning to the Home Point. Minimum RTH Altitude is 30m. You can reset the RTH Altitude in Remote Controller Settings after cancelling RTH.",
    # })
    # print("================ Finish Detecting entities in log messages\n")

if __name__ == "__main__":
    main()