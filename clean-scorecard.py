import pandas
import requests
import io

def get_scorecard_data():
    """Read scorcard data into a pandas dataframe"""
    url = "http://data.ed.gov/dataset/9dc70e6b-8426-4d71-b9d5-70ce6094a3f4/resource/823ac095-bdfc-41b0-b508-4e8fc3110082/download/most-recent-cohorts-all-data-elements-1.csv";
    x = requests.get(url=url).content 
    return pandas.read_csv(io.StringIO(x.decode('utf8')))

if __name__=="__main__":
    df = get_scorecard_data()

    # UNITID: College Scorecard's unique ID for each school
    # INSTNM: Institution name
    # UGDS: Enrollment of undergraduate certificate/degree-seeking students
    df = df[['INSTNM', 'UGDS', 'REGION', 'LOCALE', 'CCSIZSET', 'ADM_RATE', 'TUITFTE']]

    # Remove NaN
    df = df.dropna()

    # Sort decsending by UGDS
    df = df.sort_values(by='UGDS', ascending=False)

    df = df.astype({'UGDS': 'int32'})
    df = df.astype({'REGION': 'int32'})
    df = df.astype({'LOCALE': 'int32'})
    df = df.astype({'CCSIZSET': 'int32'})
    df = df.astype({'TUITFTE': 'int32'})

    # Write to csv
    df.to_csv("./data/scorecard-clean.csv", index=False)