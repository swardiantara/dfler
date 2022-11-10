import pandas as pd


def read_file(path, file_name):
    # file_name = "contoh.csv"
    full_path = f"{path}/{file_name}"
    file_ext = file_name.split(".")        
    file_ext = file_ext[1] if len(file_ext) > 1 else "" 
    # print("Ekstensi: %s" % file_ext)
    if file_ext == "csv":
        flight_log = ""
        first_line = ""
        first_col = ""
        sep = ""
        col_num = 0
        data_num = 0
        
        # read file first line
        with open(full_path, "r") as file:
            first_line = file.readline()
            first_col = first_line.split(',')[0]
            print("first col: ", first_col)
            file.close()
            
        print("num of line: ", len(first_line))
        if (first_col == "CUSTOM.date [local]"):
            print("Kondisi normal")
            flight_log = pd.read_csv(full_path, encoding="utf-8")
        elif (len(first_line) > 50 and (("No." in list(first_col))  or ("#" in list(first_col)))):
            print('Kondisi first col ada kolom tambahan')
            flight_log = pd.read_csv(full_path, encoding="utf-8")
            flight_log = flight_log.drop(flight_log.columns[[0]], axis=1)
        elif (len(first_line)> 50):
            print("Kondisi first line adalah kolom, namun first col berisi karakter random")
            dataframe = []
            with open(full_path) as file:
                for i, line in enumerate(file):
                    if i == 0: # First row should be column name
                        line = line.rstrip().split(",")
                        print("first line:", line)
                        print("Length: ", len(line))
                        start_index = line.index('CUSTOM.date [local]')
                        col_num = len(line) - start_index
                        dataframe.append(line[start_index:])
                        # if(len(line) > col_num):
                        #     sisa = len(line) - 169
                        # elif "#" in list(line[0]):
                        #     print("ada nih")
                        #     dataframe.append(line[1:])
                        # elif (len(line) > 160):
                        #     dataframe.append(line)
#                         print(sep)
                    elif i > 0:
#                         print("second line: ", line, '\n')
                        line = line.rstrip().split(",")
                        data_num = len(line)
                        if (data_num == col_num):
                            dataframe.append(line)
                        elif (data_num > col_num):
                            dataframe.append(line[data_num-col_num:])
                        else:
                            print("Jumlah data lebih kecil dari jumlah kolom")
                        # if (i == 1):
                        #     print("i = 1, len :", len(line))
                        #     col_num = len(line)
                        # if(len(line) > col_num):
                        #     sisa = len(line) - col_num
                        #     dataframe.append(line[sisa:])
                        # elif (len(line[0].split('/')) != 3):
                        #     print(len(line[0]))
                        #     print(line[0].split('/'))
                        #     dataframe.append(line[1:])
                        # else:
                        #     dataframe.append(line)
                flight_log = pd.DataFrame(data=dataframe[1:], columns=dataframe[0])
                file.close()
        else:
            print("Kondisi first line adalah karakter random")
            dataframe = []
            # read ulang file untuk ambil content
            with open(full_path) as file:
                for i, line in enumerate(file):
                    if i == 0: 
                        # sep = line.rstrip()[-1]
                        sep = ","
#                         print(sep)
                        print("first line:", line)
                        print("Length: ", len(line))
                    elif i > 0:
                        line = line.rstrip().split(sep)
                        # Second row should be column name
                        if (i == 1):
                            start_index = line.index('CUSTOM.date [local]')
                            col_num = len(line) - start_index
                            dataframe.append(line[start_index:])
                        else:
                            # 3rd... row should be the log records
                            data_num = len(line)
                            if (data_num == col_num):
                                dataframe.append(line)
                            elif (data_num > col_num):
                                dataframe.append(line[data_num-col_num:])
                            else:
                                print("The number of columns do not match")
                # if(dataframe[0][0] == "CUSTOM.date [local]"):
                #     flight_log = pd.DataFrame(data=dataframe[1:], columns=dataframe[0])
                # else:
                flight_log = pd.DataFrame(data=dataframe[1:], columns=dataframe[0])
                file.close()
#         flight_log = ""
#         with open(full_path, "r") as file:
#             first_line = file.readline()
#             first_col = first_line.split(',')
#             print("num of line: ", len(first_line))
#             sep = ""
#             if (first_col == "CUSTOM.date [local]"):
#                 print("masuk waras")
#                 flight_log = pd.read_csv(full_path, encoding="utf-8")
#             else:
#                 print("masuk ndak waras")
#                 dataframe = []
#                 for i, line in enumerate(file):
#                     if i == 0: # First row should be column name
#                         sep = line.rstrip()[-1]
#                         # print(sep)
#                         # print("first line:", line)
#                     elif i > 0:
#                         # print("second line: ", line)
#                         line = line.rstrip().split(sep)
#                         print(len(line))
#                         dataframe.append(line.rstrip().split(sep))
#                 flight_log = pd.DataFrame(data=dataframe[1:], columns=dataframe[0])
#             file.close()
        # CUSTOM.date [local]
        # CUSTOM.updateTime [local]
        # APP.message
        # APP.tip
        # APP.warning
        # print(flight_log)
        # Filter non empty message
        print(flight_log.shape)
        df_message = flight_log[flight_log.iloc[:, -3].notnull()]
        df_tip = flight_log[flight_log.iloc[:, -2].notnull()]
        df_warning = flight_log[flight_log.iloc[:, -1].notnull()]
        merged = pd.concat([df_message, df_tip, df_warning], ignore_index=True)
        remove_duplicate = merged.drop_duplicates()
        record_list = []
        for i in range (0, remove_duplicate.shape[0]):
            date = remove_duplicate.iloc[i, 0]
            time = remove_duplicate.iloc[i, 1]
            message = str(remove_duplicate.iloc[i, -3]).strip()
            tip = str(remove_duplicate.iloc[i, -2]).strip()
            warning = str(remove_duplicate.iloc[i, -1]).strip()
            if not message == "" and message != "nan":
                # message = str(remove_duplicate.iloc[i, -3]).strip()
                # print("message : {}, length: {}".format(message, len(message)))
                record_list.append([date, time, message])
            if not tip == "" and tip != "nan":
                # message = str(remove_duplicate.iloc[i, -2]).strip()
                # print("message : {}, length: {}".format(tip, len(tip)))
                record_list.append([date, time, tip])
            if not warning == "" and warning != "nan":
                # message = str(remove_duplicate.iloc[i, -1]).strip()
                # print("message : {}, length: {}".format(warning, len(warning)))
                record_list.append([date, time, warning])
        dataframe = pd.DataFrame(record_list, index=None, columns=["date", "time", "message"])
        file_name = "parsed_" + file_name
        dataframe.to_csv(f"{path}/{file_name}.csv", index=False, encoding='utf-8')
        print(dataframe.shape)
        return ""
    elif file_ext == "":
        # Extract the ERROR_POP_LOG file content
        with open(full_path, 'r', encoding='utf-8') as file:
            # Extract the file contents here
            # contents = file.read().strip()
            date = file_name.split("-")
            if (len(date) == 3 or len(date) == 4):
                date = date[0] + "/" + date[1] + "/" + date[2]
            elif ():
                date = date[0] + "/" + date[1] + "/" + date[2]
            else:
                date = file_name
            record_list = []
            lines = file.readlines()
            message = ""
            time = ""
            for line in lines:
                word = line.split(" ")
                if len(word) < 3 and word[0] == "##":
                    time =  word[1].strip()
                    continue
                elif len(word) > 2 and word[0] == "##":
                    time = word[1].strip()
                    message = " ".join(word[2:]).strip()
                else:
                    message = " ".join(word).strip()
                if not message == "" and not time == "":
                    record_list.append([date, time, message])
                # print(record_list)
            dataframe = pd.DataFrame(record_list, index=None, columns=["date", "time", "message"])
            file_name = "parsed_" + file_name
            dataframe.to_csv(f"{path}/{file_name}.csv", index=False, encoding='utf-8')
            print(dataframe.shape)
            file.close()
        return ""