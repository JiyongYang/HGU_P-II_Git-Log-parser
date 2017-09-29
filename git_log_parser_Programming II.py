import csv, os, string, re, datetime, copy

week = 4

DateTimeStandard = '2000-01-01 01:01:01'
pDateTimeStandard = datetime.datetime.strptime(DateTimeStandard, '%Y-%m-%d %H:%M:%S')
stInfo = []
result_dict = {}



# Read students number information
f_stNum = open('stNumInfo.csv', 'r', encoding='utf-8')
flg = 0
csv_rd = csv.reader(f_stNum)
for line in csv_rd:
    if flg == 0:
        flg = 1
        continue
    else:
        stInfo.append(line[0])
f_stNum.close()

# init
for stuNum in stInfo:
    for i in range(week):
        # 0: st_NUm, 1: Hw Num, 2: CPP, 3: CPPDate, 4: total cnt, 5: total ins, 6: total del, 7: IMG, 8: IMG date 9 :  size
        result_dict[(stuNum, i+1)] = [stuNum, i+1, "X", pDateTimeStandard, 0, 0, 0, "X", pDateTimeStandard, 0] 

# Open Result csv file
f_resultCsv = open('Result.csv', 'w', newline='')
f_resultCsv_wr = csv.writer(f_resultCsv)
f_resultCsv_wr.writerow(['stNum', 'Hw', 'CPP', 'Date', 'changes', 'insert', 'delete', 'IMG', 'Date', 'Size'])

# Read log files
dir = os.listdir('./assessment')
os.chdir('./assessment')

for log_file in dir:
    f_logFile = open(log_file, 'r', encoding='utf-8')
    stNum = log_file.split('-')[1].split('_')[0]
    readLog = f_logFile.readlines()
    flg = 0
    hwNum = 0
    date = pDateTimeStandard

    
    for line in readLog:
        line = line.lower().rstrip()
        ptn = re.compile(stNum+'_homework')
        
        if(line.startswith(' ') == False and len(line) > 1):
            line = line.strip()
            words = line.split(',')
            
            #result_dict[(stNum, hwNum)] = copy.deepcopy(data)
            
            hwNum = 0
            date = pDateTimeStandard
            # date
            date = words[1].split('+')[0]
            datelist = date.split()
            date = datetime.datetime.strptime(datelist[4]+"-"+datelist[1]+"-"+datelist[2]+" "+datelist[3], "%Y-%b-%d %H:%M:%S")
            
        elif(line.startswith(' ') == True and len(line) > 1):
            line = line.strip()
            if ptn.search(line):
                hwNum = line[line.find(stNum+'_homework')+17:line.find(stNum+'_homework')+19]
                if(hwNum[1] == '.'):
                    hwNum = hwNum[0]
                hwNum = int(hwNum)

                #data[1] = hwNum
                

                # cpp
                cppPtn = re.compile('cpp')
                if cppPtn.search(line):
                    temp = line.split('|')
                    for i in range(len(temp)):
                       temp[i]  = temp[i].strip()
                    total = temp[1].split()
                    if(len(total) > 1):
                        #print((stNum, hwNum))
                        total_str = total[1].strip()
                        total_cnt = len(total_str)
                        total_ins = total_str.count('+')
                        total_del = total_str.count('-')
                        result_dict[(stNum, hwNum)][4] += total_cnt
                        result_dict[(stNum, hwNum)][5] += total_ins
                        result_dict[(stNum, hwNum)][6] += total_del
                        if(result_dict[(stNum, hwNum)][3] < date):
                            result_dict[(stNum, hwNum)][2] = "CPP"
                            result_dict[(stNum, hwNum)][3] = date
                # img
                imgPtn = re.compile('[jpg][pni][gf]')
                if imgPtn.search(line):
                    temp = line.split('|')
                    for i in range(len(temp)):
                       temp[i]  = temp[i].strip()
                    if(len(temp[1].split()) > 3):
                        size = int(temp[1].split()[3])
                        if(stNum =='21400209'):
                            print(stNum, hwNum, result_dict[(stNum, hwNum)], date, size)
                        if(result_dict[(stNum, hwNum)][8] < date):
                            result_dict[(stNum, hwNum)][7] = "IMG"
                            result_dict[(stNum, hwNum)][9] = size
                            result_dict[(stNum, hwNum)][8] = date
                        elif(result_dict[(stNum, hwNum)][8] == date and result_dict[(stNum, hwNum)][9] == 0 and size > 0):
                            result_dict[(stNum, hwNum)][7] = "IMG"
                            result_dict[(stNum, hwNum)][9] = size
                            result_dict[(stNum, hwNum)][8] = date

resultDict_list = list(result_dict.values())
resultDict_list.sort()


for lst in resultDict_list:
    for i in range(len(lst)):
        if(i == 3 or i == 8):
            lst[i] = lst[i].ctime()
        else:
            lst[i] = str(lst[i])
    f_resultCsv_wr.writerow(lst)

f_resultCsv.close()
