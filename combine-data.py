import hashlib
import pandas

def hash_name(name):
    name = "".join(name.split(" "))
    name = name.replace("&", "and")
    name = name.replace(',', '')
    name = name.replace('.', '')
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.replace('\'', '')
    name = name.lower()

    hash_object = hashlib.sha1(name.encode())
    return hash_object.hexdigest()

def add_to_data(data, header, df, name_field, ignore_cols):
    num_cols = 0
    for col in df.columns:
        if col != name_field and col not in ignore_cols:
            header += col + ","
            num_cols += 1

    for key in data.keys():
        for i in range(num_cols):
            data[key].append("n/a")

    for index, row in df.iterrows():
        i = len(next(iter(data.values()))) - num_cols
        for col in df.columns:
            if col != name_field and col not in ignore_cols:
                name_hash = hash_name(row[name_field])
                if name_hash in data:
                    data[name_hash][i] = str(row[col]).replace(',', "")
                i += 1
    return header

def is_complete(vals, covid_cases_index, ugrad_pop_index, reopening_model_index):
    return exists(vals[covid_cases_index]) and exists(vals[ugrad_pop_index]) and exists(vals[reopening_model_index])

def exists(s):
    return s != "n/a"

def main():
    covid_cases = pandas.read_csv("./data/colleges_cases.csv")
    niche_details_data = pandas.read_csv("./data/details-data-niche.csv")
    party_bestcolleges = pandas.read_csv("./data/party-schools-bestcolleges.csv")
    party_niche = pandas.read_csv("./data/party-schools-niche.csv")
    party_stacker = pandas.read_csv("./data/party-schools-stacker.csv")
    reopening_models = pandas.read_csv("./data/reopening-models-clean.csv")
    reopening_models = reopening_models.loc[:, ~reopening_models.columns.str.contains('^Unnamed')]
    undergrad_pop = pandas.read_csv("./data/undergrad-population.csv")

    header = "key,"
    data = {}

    for col in niche_details_data.columns:
        header += col + ","
    for index, row in niche_details_data.iterrows():
        data[hash_name(row["niche_name"])] = []
        for col in niche_details_data.columns:
            data[hash_name(row["niche_name"])].append(str(row[col]))

    header = add_to_data(data, header, party_niche, "name", [])
    header = add_to_data(data, header, party_bestcolleges, "name", [])
    header = add_to_data(data, header, party_stacker, "name", [])
    header = add_to_data(data, header, covid_cases, "college", ["date", "county", "city", "ipeds_id", "notes"])
    header = add_to_data(data, header, undergrad_pop, "name", ["UNITID"])
    header = add_to_data(data, header, reopening_models, "name", [])

    header += "is_complete,"
    col_names = header.split(",")
    covid_cases_index = col_names.index("covid_cases") - 1
    ugrad_pop_index = col_names.index("undergrad_pop") - 1
    reopening_model_index = col_names.index("reopening_plan") - 1

    CSV = header + "\n"
    num_complete = 0
    for key, val in data.items():
        complete = is_complete(val, covid_cases_index, ugrad_pop_index, reopening_model_index)
        if complete:
            num_complete += 1
        val.append(str(complete))
        CSV += str(key) + ","
        CSV += ",".join(val) + "\n"

    with open("./data/all-data.csv", "w") as file:
            file.write(CSV)

    print("Number of Complete Rows: " + str(num_complete))


if __name__=="__main__":
    main()