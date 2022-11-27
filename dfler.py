import requests
import time
import os
import json
from tqdm import tqdm
from datetime import datetime
from os import system, name
from parse import read_android_log, read_ios_log, construct_timeline
from generate_report import generate_report
from simpletransformers.ner import NERModel
import pandas as pd
import torch


def get_config():
    config_file = open('config.json')
    config_file = json.load(config_file)

    now = datetime.now()
    now = now.strftime("%d%m%Y_%H%M%S")
    output_dir = os.path.join(config_file['output_dir'], now)
    previous_step = 0
    previous_status = False
    use_cuda = True if torch.cuda.is_available() == True else False
    

    wkhtml_path = ""
    if name == 'nt':
        wkhtml_path = config_file['wkhtml_path']['windows']
    # for mac and linux(here, os.name is 'posix')
    else:
        wkhtml_path = config_file['wkhtml_path']['linux']

    return {
        "output_dir": output_dir,
        "model_dir": config_file['model_dir'],
        "previous_step": previous_step,
        "previous_status": previous_status,
        "wkhtml_path": wkhtml_path,
        "app_version": config_file['app_version'],
        "use_cuda": use_cuda
    }

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def menu():
    # clear_screen()
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
    # now = datetime.now()
    # now = now.strftime("%d%m%Y_%H%M%S")
    # output_dir = os.path.join("./result", now)
    config = get_config()

    if not os.path.exists(config['output_dir']):
        os.makedirs(config['output_dir'])

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
            android_logs.extend(ios_logs)
            # save to .json file
            config['previous_step'] = 1
            if(len(android_logs) == 0):
                print('No found files in the evidence folder!')
                config['previous_status'] = False
                time.sleep(1)
            else:
                with open(config['output_dir'] + '/raw_list.json', 'w') as file:
                    json.dump(android_logs, file)
                config['previous_status'] = True
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
            if config['previous_status'] == False and config['previous_step'] == 1:
                print('Please follow the steps accordingly')
                time.sleep(1)
                input("Press enter to continue...")
                continue
            elif (config['previous_step'] == 1 and config['previous_status'] == True) or (config['previous_step'] != 1 and config['previous_status'] == True):
                clear_screen()
                print('Forensic timeline construction is in process...\n')

                # Parse the raw flight logs
                os.makedirs(config['output_dir'] + '/parsed/android')
                android_path = os.path.join(config['output_dir'], 'parsed/android')
                os.makedirs(config['output_dir'] + '/parsed/ios')
                ios_path = os.path.join(config['output_dir'], 'parsed/ios')
                full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flight_logs')
                
                # Construct the forensic timeline from parsed flight log
                # print(full_path)
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
                            read_android_log(path, filename, android_path)
                            print("Finish Extracting file: %s\n" % filename)
                        android_parsed = True
                        
                    elif path.find("ios") != -1:
                        for filename in os.listdir(path):
                            if filename.find("parsed") != -1:
                                continue
                            print("path: ", path)
                            print("Extracting file: %s" % filename)
                            read_ios_log(path, filename, ios_path)
                            print("Finish Extracting file: %s\n" % filename)
                        ios_parsed = True

                parsed_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join(config['output_dir'], 'parsed'))
                for path, subdirs, files in os.walk(parsed_path):
                    for filename in files:
                        path_list.append(os.path.join(path, filename))
                    # if(ios_parsed or android_parsed):
                    #     for name in files:
                    #         file_ext = name.split(".")
                    #         file_ext = file_ext[-1] if len(file_ext) > 1 else ""
                    #         if(name.find("parsed_") != -1 and file_ext == "csv"):
                    #             path_list.append(os.path.join(path, name))

                parent_df = pd.DataFrame()
                print(parent_df)
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

                print('Save forensic timeline to .csv file...')
                parent_df.to_csv(config['output_dir'] + '/forensic_timeline.csv', index=False, encoding="utf-8")             
                
                print('Finish constructing timeline.')
                input("Press enter to continue...")
            else:
                print('Please follow the steps accordingly')
                time.sleep(1)
                input("Press enter to continue...")
                continue
        elif start == '3':
            if config['previous_status'] == False and config['previous_step'] == 2:
                print('Please follow the steps accordingly')
                time.sleep(1)
                input("Press enter to continue...")
                continue
            elif (config['previous_step'] == 2 and config['previous_status'] == True) or (config['previous_step'] != 2 and config['previous_status'] == True):
                clear_screen()
                print('Entity Recognition is in process...\n')

                # Load the fine-tuned model
                print("Loading model...\n")
                droner = NERModel(
                    "bert", "model", use_cuda=config['use_cuda']
                )
                
                # Load the forensic timeline
                print("Loading forensic timeline...\n")
                timeline = pd.read_csv(config['output_dir'] + '/forensic_timeline.csv', encoding="utf-8")
                
                print('Recognizing mentioned entities...')
                pred_list = []
                for row in tqdm(range(0, timeline.shape[0])):
                    message = timeline.iloc[row, 1]
                    [entities], _ = droner.predict([message])
                    timestamp = timeline.iloc[row, 0]
                    pred_list.append({"timestamp": timestamp, "entities": entities})
                
                # save to .json file
                with open(config['output_dir'] + '/ner_result.json', 'w') as file:
                    json.dump(pred_list, file)
                print('Finish recognizing mentioned entities...')
                input("Press enter to continue...")
            else:
                print('Please follow the steps accordingly')
                time.sleep(1)
                input("Press enter to continue...")
                continue
        elif start == '4':
            if config['previous_status'] == False and config['previous_step'] == 2:
                print('Please follow the steps accordingly')
                time.sleep(1)
                input("Press enter to continue...")
                continue
            elif (config['previous_step'] == 2 and config['previous_status'] == True) or (config['previous_step'] != 2 and config['previous_status'] == True):
                clear_screen()
                print('Forensic report generation is in process...\n')

                print('Loading the entity recognition results...')
                # Opening JSON file
                timeline_file = open(config['output_dir'] +  '/ner_result.json')
                timeline = json.load(timeline_file)

                print('Generating forensic report...')
                generate_report(config)
                # Load the NER results
                # ner_result = json.read('')
                print('Finish generating forensic report...')
                input("Press enter to continue...")
            else:
                print('Please follow the steps accordingly')
                time.sleep(1)
                input("Press enter to continue...")
                continue
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