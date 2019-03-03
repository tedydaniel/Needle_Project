import combine_headlines_stockdata
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


def learn_stock_news(combined):
    data = list(combined.values())
    features_num = len(data[0][0])
    train_data = np.zeros((1900, features_num))
    train_labels_value = np.zeros(1900)
    test_data = np.zeros((len(data) - 1900, features_num))
    test_labels_values = np.zeros(len(data) - 1900)
    perms = np.random.permutation(len(data))

    i = 0
    for x in np.nditer(perms[:1900]):
        train_data[i] = data[x][0]
        train_labels_value[i] = (data[x][1] - 1) * 100
        i += 1

    j = 0
    for y in np.nditer(perms[1900:]):
        test_data[j] = data[y][0]
        test_labels_values[j] = (data[y][1] - 1) * 100
        j += 1

    labals_std = np.std(np.concatenate((train_labels_value, test_labels_values)))
    labals_mean = np.mean(np.concatenate((train_labels_value, test_labels_values)))

    learner = linear_model.LinearRegression()
    learner.fit(train_data, train_labels_value)
    prediction = learner.predict(test_data)
    random_prediction = np.random.normal(labals_mean, labals_std, 88)
    mean_squared_err = mean_squared_error(test_labels_values, prediction)
    score = r2_score(test_labels_values, prediction)
    random_mean_squared_err = mean_squared_error(test_labels_values, random_prediction)
    random_score = r2_score(test_labels_values, random_prediction)

    print(mean_squared_err)
    print(random_mean_squared_err)
    print(score)
    print(random_score)


if __name__ == "__main__":
    data_combined = combine_headlines_stockdata.combine()
    learn_stock_news(data_combined)
