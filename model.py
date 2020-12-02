from model_helper import * 
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

def map_reopening_plan(s):
    if s == "Fully online":
        return -1
    elif s == "Primarily online":
        return -0.5
    elif s == "Hybrid":
        return 0
    elif s == "Primarily in person":
        return 0.5
    elif s == "Fully in person":
        return 1
    else:
        return float('nan')

def map_covid_cases(n):
    if n < 10:
        return 0
    elif n < 200:
        return 1
    elif n >= 200:
        return 2
    else:
        return float('nan')

def load_and_clean_data():
    # Load dataset
    df = pd.read_csv("./data/all-data.csv")

    # Keep only relevant columns
    df = df[['UGDS', 'LOCALE', 'ADM_RATE', 'REGION', 'CCSIZSET', 'TUITFTE', 'reopening_plan', 'covid_cases']]

    # Map reopening plan to float from -1 to 1
    df['reopening_plan'] = df['reopening_plan'].apply(map_reopening_plan)

    # Map covid cases to three categories
    df['covid_cases'] = df['covid_cases'].apply(map_covid_cases)

    # Drop rows with NaN
    df = df.dropna()

    # Encode LOCALE, REGION, and CCSIZSET as one-hot vectors
    locale_col = df['LOCALE'].tolist()
    df = df.drop(columns=['LOCALE'])
    locale_options = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
    locale_option_names = ["Locale_" + str(xi) for xi in locale_options]
    locale_matrix = convert_to_one_hot(locale_options, locale_col)

    region_col = df['REGION'].tolist()
    df = df.drop(columns=['REGION'])
    region_options = list(range(10))
    region_option_names = ["Region_" + str(xi) for xi in region_options]
    region_matrix = convert_to_one_hot(region_options, region_col)

    carnegie_col = df['CCSIZSET'].tolist()
    df = df.drop(columns=['CCSIZSET'])
    carnegie_options = list(range(18))
    carnegie_options.append(-2)
    carnegie_option_names = ["Carnegie_" + str(xi) for xi in carnegie_options]
    carnegie_matrix = convert_to_one_hot(carnegie_options, carnegie_col)

    # Remove covid_cases from data so that it is not normalized
    covid_col = df['covid_cases'].tolist()
    df = df.drop(columns=['covid_cases'])

    # Normalize the values in the dataset
    df = normalize(df)
    df = reset(df)

    # Add locale, carnegie, region, and covid back to the datase
    locale_df = pd.DataFrame(data=locale_matrix, columns=locale_option_names)
    carnegie_df = pd.DataFrame(data=carnegie_matrix, columns=carnegie_option_names)
    region_df = pd.DataFrame(data=region_matrix, columns=region_option_names)
    df = pd.concat([df, locale_df, carnegie_df, region_df], axis=1, sort=False)
    df['covid_cases'] = covid_col

    return df

def test_model(test, model):
    # Evaluate the precision of the model for each row in the test set
    test_clean = test.drop(columns=["covid_cases"])
    correct = 0
    total = 0
    correct_by_bucket = {0: 0, 1: 0, 2: 0} # True positives
    predictions_by_bucket = {0: 0, 1: 0, 2: 0} # True positives + false positives
    total_by_bucket = {0: 0, 1: 0, 2: 0} # True positives + false negatives
    for index, row_clean in test_clean.iterrows():
        actual = test.loc[index]["covid_cases"]
        numpy_batch = np.array([row_clean.values])
        prediction_list = model.predict_on_batch(x=numpy_batch)[0].tolist()
        prediction = prediction_list.index(max(prediction_list))

        if int(actual) == int(prediction):
            correct += 1
            correct_by_bucket[actual] += 1
        total += 1
        total_by_bucket[actual] += 1
        predictions_by_bucket[prediction] += 1
    
    # Print the results
    print("\n" + ("-" * 50))
    print("TEST SET RESULTS")
    print("=" * 50)
    print()
    print("Overall Precision: %0.3f\n" % (correct/total))
    for k in correct_by_bucket.keys():
        print("Bucket %d:" % (k))
        print("\tPrecision: %0.3f" % (correct_by_bucket[k]/predictions_by_bucket[k]))
        print("\tActual Count: %d" % (total_by_bucket[k]))
        print("\tNum Predictions: %d" % (predictions_by_bucket[k]))
        print()
    print("-" * 50)

def main():
    tf.get_logger().setLevel('ERROR')

    df = load_and_clean_data()

    # Split into test and train sets
    train, test = train_test_split(df, test_size=0.25)
    x_train = train.drop(columns=['covid_cases']).values
    y_train = train['covid_cases'].values
    y_train = tf.keras.utils.to_categorical(y_train)

    # Train the model
    epochs = 2000
    batch_size = 20
    my_model = create_model()
    epochs, mse = train_model(my_model, x_train, y_train, epochs, batch_size)

    # Test the model
    test_model(test, my_model)

    # Plot the loss curve
    plot_the_loss_curve(epochs, mse)

if __name__=="__main__":
    main()