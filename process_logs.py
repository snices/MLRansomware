import re

# Desired Format: processname:Col3

# log file path to parse from
logfile = r"testLog.txt"
# indicator list file path that will be used to check for IoC's
indicators = r"VariableNames.txt"
# weights of each notable indicator
weights = r"Weights.csv"


# formatting indicator file
def formatting():
    f = open("IndicatorsFormatted.txt", "w", encoding='utf8')

    # formatting the indicator list
    with open(indicators, "r", encoding="utf8") as watchlist:
        for line in watchlist:
            keys = re.split(":", line)
            f.writelines(keys[-1])

    print("Indicator Formatting Completed.")


# formatting indicator file
def weights_format():
    f = open("WeightsFormatted.txt", "w", encoding='utf8')

    # formatting the weights list
    with open(weights, "r", encoding="utf8") as w:
        for line in w:
            keys = re.split(",", line)
            #print(keys[0][3:])
            f.writelines('%d' % int(keys[0][3:]) + "\n")

    print("Weight Formatting Completed.")


# look for matches between the logfile and indicator list
def find_matches():
    ioc = open("IndicatorsFormatted.txt", "r", encoding='utf8')
    search = open(logfile, "r", encoding='utf8')
    matches = open("matches.txt", "w", encoding='utf8')
    priority = open("WeightsFormatted.txt", "r", encoding='utf8')
    weight = priority.readlines()
    check = []
    for element in weight:
        check.append(element.strip())

    for line1 in search:
        count = 0
        key = re.split(":", line1)
        line1 = key[-1]
        pid = key[0]
        for line2 in ioc:
            # print(line1 + line2)
            x = re.search(line1, line2)
            if x is None:
                count = count + 1
            else:
                count = count + 1
                if len(key) >= 2 and str(count) in check:
                    print("Matched " + x.string.strip('\n') + " on line " + str(count) + " PROCESS: " + pid)
                    matches.writelines(pid + ":" + "Col" + str(count) + "\n")
                elif str(count) in check:
                    print("Matched " + x.string.strip('\n') + " on line " + str(count) + " PROCESS: " + "NULL")
                    matches.writelines("NO-PID-FOUND" + ":" + "Col" + str(count) + "\n")
        ioc.seek(0)


def convert_to_ML_form():
    infile = open("matches.txt", "r", encoding='utf8')
    ids = infile.readlines()
    for i in range(0, len(ids)):
        ids[i] = int(ids[i])
    # print(ids)

    outfile = open("matches.csv", "w", encoding='utf8')
    # for loop i < 5000
    # 0 else 1
    i = 1
    while i <= 5000:
        for j in ids:
            if j == i & i != 5000:
                outfile.writelines("1" + ",")
                i = i + 1
            elif j == i & i == 5000:
                outfile.writelines("1")
        if i != 5000:
            outfile.writelines("0" + ",")
        else:
            outfile.writelines("0")
        i = i + 1


weights_format()
formatting()
find_matches()
