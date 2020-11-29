import matplotlib.pyplot as plt
import pandas
import numpy

def is_in_person_or_hybrid(s):
    return s == "Fully in person" or s == "Primarily in person" or s == "Hybrid"

def is_mostly_in_person(s):
    return s == "Fully in person" or s == "Primarily in person"

def is_mostly_online(s):
    return s == "Primarily online"

def is_hybrid(s):
    return s == "Hybrid"

def plot(x, y, title, x_title, y_title):
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    z = numpy.polyfit(x, y, 1)
    p = numpy.poly1d(z)
    plt.plot(x, p(x), "--r")
    plt.show()

def bar_plot(x, y, title, x_title, y_title):
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    ax = plt.gca()
    plt.show()

def plot_gender_ratio(df):
    df = df[df["is_complete"] == True]
    df = df[df["percent_female"] != "n/a"]
    df = df[df["reopening_plan"].map(is_in_person_or_hybrid) == True]
    df = df[df["undergrad_pop"] > 10000]
    df = df[["covid_cases", "percent_female"]].dropna()
    print(df)
    covid_cases = df["covid_cases"].tolist()
    percent_female = df["percent_female"].tolist()

    covid_cases = list(map(lambda x: float(x), covid_cases))
    percent_female = list(map(lambda x: int(x[0:-1]), percent_female))

    plot(
        percent_female,
        covid_cases,
        "Covid Cases vs Gender Ratio For Schools With More Than 10,000 Undergrads",
        'Percent of undergraduate population that is female',
        'Covid-19 cases reported'
        )

def plot_political_affiliation(df):
    df = df[df["is_complete"] == True]
    df = df[df["self_democratic"] != "n/a"]
    df = df[df["reopening_plan"].map(is_mostly_online or is_hybrid) == True]
    df = df[df["undergrad_pop"] > 10000]
    df = df[["covid_cases", "self_democratic"]].dropna()
    print(df)
    covid_cases = df["covid_cases"].tolist()
    self_democratic = df["self_democratic"].tolist()

    covid_cases = list(map(lambda x: float(x), covid_cases))
    self_democratic = list(map(lambda x: int(x[0:-1]), self_democratic))

    plot(
        self_democratic,
        covid_cases,
        "Covid Cases vs Political Affiliation For Schools With More Than 10,000 Undergrads",
        'Percent of student body that identifies as Democrat (based on Niche survey)',
        'Covid-19 cases reported'
        )

def plot_party_schools(df):
    df = df[df["is_complete"] == True]
    df = df[df["niche_party_school_grade"] != "n/a"]
    df = df[df["reopening_plan"].map(is_mostly_in_person) == True]
    df = df[["covid_cases", "niche_party_school_grade", "undergrad_pop"]].dropna()
    print(df)
    covid_cases = df["covid_cases"].tolist()
    covid_cases = list(map(lambda x: float(x), covid_cases))

    grade_categories = ["A+", "A", "A-", "B+", "B"]
    num_schools = [0, 0, 0, 0, 0]
    covid_per_ugrad = [0, 0, 0, 0, 0]

    for i in df.index:
        num_schools[grade_categories.index(df["niche_party_school_grade"][i])] += 1
        covid_per_ugrad[grade_categories.index(df["niche_party_school_grade"][i])] += float(df["covid_cases"][i]) / float(df["undergrad_pop"][i])

    av_covid_per_ugrad = []
    for i in range(len(num_schools)):
        av_covid_per_ugrad.append(covid_per_ugrad[i] / num_schools[i])

    bar_plot(
        grade_categories,
        av_covid_per_ugrad,
        "Average Covid Cases Per Undergrad vs Niche Party School Grade For Schools That Are Mostly In Person",
        'Niche Party School Grade',
        'Average Number of Covid-19 Cases Per Undergrad'
        )

def plot_reopening_model(df):
    df = df[df["is_complete"] == True]
    df = df[df["reopening_plan"] != "Undetermined"]
    df = df[df["reopening_plan"] != "Other"]
    df = df[["covid_cases", "reopening_plan", "undergrad_pop"]].dropna()
    print(df)
    covid_cases = df["covid_cases"].tolist()
    covid_cases = list(map(lambda x: float(x), covid_cases))

    reopening_categories = ["Fully in person", "Primarily in person", "Hybrid", "Primarily online", "Fully online"]
    num_schools = [0, 0, 0, 0, 0]
    covid_per_ugrad = [0, 0, 0, 0, 0]

    for i in df.index:
        num_schools[reopening_categories.index(df["reopening_plan"][i])] += 1
        covid_per_ugrad[reopening_categories.index(df["reopening_plan"][i])] += float(df["covid_cases"][i]) / float(df["undergrad_pop"][i])

    av_covid_per_ugrad = []
    for i in range(len(num_schools)):
        av_covid_per_ugrad.append(covid_per_ugrad[i] / num_schools[i])

    bar_plot(
        reopening_categories,
        av_covid_per_ugrad,
        "Average Covid Cases Per Undergrad vs Reopening Model",
        'Reopening Model',
        'Average Number of Covid-19 Cases Per Undergrad'
        )

def main():
    df = pandas.read_csv("./data/all-data.csv")
    plot_reopening_model(df)

if __name__=="__main__":
    main()