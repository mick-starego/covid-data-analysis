import pandas

def get_scorecard_data():
    """Read scorcard data into a pandas dataframe"""
    return pandas.read_csv("https://data.ed.gov/dataset/9dc70e6b-8426-4d71-b9d5-70ce6094a3f4/resource/823ac095-bdfc-41b0-b508-4e8fc3110082/download/most-recent-cohorts-all-data-elements-1.csv")

if __name__=="__main__":
    df = get_scorecard_data()

    # UNITID: College Scorecard's unique ID for each school
    # INSTNM: Institution name
    # UGDS: Enrollment of undergraduate certificate/degree-seeking students
    df = df[['UNITID', 'INSTNM', 'UGDS']]

    # Remove NaN
    df = df.dropna()

    # Sort decsending by UGDS
    df = df.sort_values(by='UGDS', ascending=False)

    # Convert UGDS to ints
    df = df.astype({'UGDS': 'int32'})

    # Remove schools with UGDS < 100. These schools are much too small for our analysis.
    df = df[df['UGDS'] >= 100]

    # Write to csv
    df.to_csv("./undergrad-population.csv", index=False)