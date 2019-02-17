import pandas as pd
import tqdm

try:
    ipy_str = str(type(get_ipython()))
    if "zmqshell" in ipy_str or "terminal" in ipy_str:
        from tqdm import tqdm, tqdm_notebook

        tqdm.pandas(tqdm_notebook)
except:
    from tqdm import tqdm

    tqdm.pandas()


def read_cdwow(filename):
    df = (
        # read the data
        pd.read_csv(
            filename,
            names=["id", "date", "num_purchased", "dollars"],
            header=None,
            sep=r"\s+",
        )
        # format the dates as dates
        .pipe(lambda x: x.assign(date=pd.to_datetime(x.date, format="%Y%m%d")))
        # calculate the average cost per CD in the basket
        .pipe(lambda x: x.assign(price_per_cd=x.dollars / x.num_purchased))
    )

    return df


def summarise_users(data, reporting_date, frequency_period=90):
    """
    data: the dataframe that we're going to be summarising
    reporting_date: fixed point in time. We're going to 
        look at data before this point to calculate our
        summary.
    frequency_period: the time period that we will use for 
        calculating the frequency of the users.
    """
    summary = (
        data.query("date <= @reporting_date")
        .groupby("id")
        .progress_apply(summarise_user, reporting_date=reporting_date)
    )

    return summary


def calculate_recency(data, reporting_date):
    return (reporting_date - data.date.max()).days


def calculate_frequency(data):
    return data.date.nunique()


def calculate_tenure(data):
    return (data.date.max() - data.date.min()).days


def calculate_clumpiness(data):
    # New Measures of Clumpiness for Incidence Data by Zhang
    # Suggests variance of inter visit times is a pretty decent
    # measure of clumpiness
    return (
        data.sort_values("date")
        # difference between actions
        .date.diff()
        # Calculate this in days
        .dt.days
        # get the variance
        .var()
    )


def calculate_number_purchases(data):
    return data.num_purchased.sum()


def calculate_total_dollars(data):
    return data.dollars.sum()


def summarise_user(user_data, reporting_date):
    """Calculate a summary of an individual user
    user_data: groupby object that contains the user information
    reporting_date: the end date that we're calculating from. 
        Used for the calculation of recency.
    """
    # Calculate summary statistics
    recency = calculate_recency(user_data, reporting_date)
    frequency = calculate_frequency(user_data)
    tenure = calculate_tenure(user_data)
    clumpiness = calculate_clumpiness(user_data)
    number_purchases = calculate_number_purchases(user_data)
    total_dollars = calculate_total_dollars(user_data)

    return pd.Series(
        {
            "recency": recency,
            "frequency": frequency,
            "tenure": tenure,
            "clumpiness": clumpiness,
            "number_purchases": number_purchases,
            "total_dollars": total_dollars,
        }
    )
