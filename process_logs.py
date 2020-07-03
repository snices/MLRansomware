import re

# log file path to parse from
logfile = r"path"
# indicator list file path that will be used to check for IoC's
indicators = r"path"


# formatting indicator file
def formatting():
    f = open("IndicatorsFormatted.txt", "w", encoding='utf8')

    # formatting the indicator list
    with open(indicators, "r", encoding="utf8") as watchlist:
        for line in watchlist:
            keys = re.split(":", line)
            f.writelines(keys[-1])

    print("Formatting Completed.")


# look for matches between the logfile and indicator list
def find_matches():
    ioc = open("IndicatorsFormatted.txt", "r", encoding='utf8')
    search = open(logfile, "r", encoding='utf8')
    matches = open("matches.txt", "w", encoding='utf8')

    for line1 in search:
        count = 0
        for line2 in ioc:
            # print(line1 + line2)
            x = re.search(line1, line2)
            if x is None:
                count = count + 1
            else:
                count = count + 1
                print("Matched " + x.string.strip('\n') + " on line " + str(count))
                matches.writelines(str(count) + "\n")
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


formatting()
find_matches()
convert_to_ML_form()
