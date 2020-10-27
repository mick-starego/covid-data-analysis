import re
import pandas

def get_college_name(raw_name):
    missing_char = ""

    raw_name_split = re.split("[a-z][A-Z]", raw_name)
    if len(raw_name_split) == 1:
        raw_name_split = raw_name.split(')')
        missing_char = ")"
    else:
        missing_char = raw_name[len(raw_name_split[0])]

    if len(raw_name_split) == 2:
        return raw_name_split[0].replace("?", "") + missing_char
    else:
        print(raw_name)
        for s in raw_name_split:
            print("\t" + s)
        print()
        return raw_name

def main():
    df = pandas.read_csv("./data/reopening-models-raw.csv")
    df["Name"] = df["Name"].apply(get_college_name)
    df.to_csv("./data/reopening-models-clean.csv", index=False)

if __name__=="__main__":
    main()