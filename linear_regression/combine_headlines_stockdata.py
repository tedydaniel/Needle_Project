import numpy as np
import read_headlines
import read_stock_data
import pprint


def combine():
    dates_words_counter, frequent_words, frequent_words_nums = read_headlines.read()
    stock_close_value = read_stock_data.read()

    words_keys = np.fromiter(dates_words_counter.keys(), dtype=np.int)

    stock_changes = {}
    next_day_date = False
    last_day_close = 0
    for date, close_value in stock_close_value.items():
        if next_day_date:
            stock_changes[read_headlines.date_to_int(next_day_date)] = (read_headlines.date_to_int(date), last_day_close / close_value)
        last_day_close = close_value
        next_day_date = date

    all_words_for_change = {}
    for key, value in stock_changes.items():
        all_words = np.zeros(len(frequent_words))
        dates_after = np.argwhere(words_keys >= value[0])
        dates_before = np.argwhere(words_keys <= key)
        day_to_count = np.intersect1d(dates_after, dates_before)
        day_count = []
        for x in np.nditer(day_to_count):
            all_words = all_words + dates_words_counter[words_keys[x]]
            day_count.append(words_keys[x])
        all_words_for_change[key] = (all_words, value[1])

    return all_words_for_change


if __name__ == "__main__":
    pprint.pprint(combine())
