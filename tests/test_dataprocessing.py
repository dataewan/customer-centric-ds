import pandas as pd
import pytest
import numpy as np
from customercentric import dataprocessing

# Create the test data
df = pd.DataFrame(
    {
        "id": [1, 1, 1, 1, 1, 1],
        "date": [
            "1999-01-01",
            "1999-01-02",
            "1999-01-02",
            "1999-01-11",
            "1999-01-12",
            "1999-01-20",
        ],
        "num_purchased": [1, 1, 1, 2, 2, 2],
        "dollars": [1, 1, 1, 2, 2, 2],
    }
)
df = df.assign(date=pd.to_datetime(df.date))

df_2 = pd.DataFrame(
    {
        "id": [1, 1],
        "date": ["1999-01-01", "1999-01-01"],
        "num_purchased": [1, 2],
        "dollars": [1, 11],
    }
)

df_2 = df_2.assign(date=pd.to_datetime(df_2.date))


def test_recency():
    output = dataprocessing.calculate_recency(df, pd.to_datetime("1999-01-20"))
    assert output == 0
    output = dataprocessing.calculate_recency(df_2, pd.to_datetime("1999-01-20"))
    assert output == 19


def test_frequency():
    output = dataprocessing.calculate_frequency(df)
    # one of the days isn't unique, so it shouldn't be counted as unique
    assert output == 5
    output = dataprocessing.calculate_frequency(df_2)
    # one of the days isn't unique, so it shouldn't be counted as unique
    assert output == 1


def test_tenure():
    output = dataprocessing.calculate_tenure(df)
    assert output == 19
    output = dataprocessing.calculate_tenure(df_2)
    assert output == 0


def test_clumpiness():
    output = dataprocessing.calculate_clumpiness(df)
    # The values are Nan, 1, 0, 9, 1, 8
    # mean of 3.8
    # (1 - 3.8)^2 +
    # (0 - 3.8)^2 +
    # (9 - 3.8)^2 +
    # (1 - 3.8)^2 +
    # (8 - 3.8)^2 = 74.8
    # 74.8 / 4 (because pandas uses the unbiassed estimator) = 18.7
    assert output == pytest.approx(18.7)
    # The second dataframe has two visits on the same day, so there isn't a clumpiness
    output = dataprocessing.calculate_clumpiness(df_2)
    assert np.isnan(output)


def test_num_purchases():
    output = dataprocessing.calculate_number_purchases(df)
    assert output == 9
    output = dataprocessing.calculate_number_purchases(df_2)
    assert output == 3


def test_total_dollars():
    output = dataprocessing.calculate_total_dollars(df)
    assert output == 9
    output = dataprocessing.calculate_total_dollars(df_2)
    assert output == 12
