Exploring techniques written in papers that consider the dataset from a customer centric point of view.
That is a dataset that has every datapoint associated with a customer ID.

# CD wow dataset


The CD wow dataset comes from an online CD retailer.
It has a record for each transaction that a customer makes,
and in each transaction they could have purchased multiple CDs.

```
 00001 19970101  1   11.77
 00002 19970112  1   12.00
 00002 19970112  5   77.00
 00003 19970102  2   20.76
 00003 19970330  2   20.76
 00003 19970402  2   19.54
 00003 19971115  5   57.45
 00003 19971125  4   20.96
 00003 19980528  1   16.99
```

_Sample of the dataset. Columns are user ID, transaction date, number of CDs in the purchase, and total dollar amount of the transaction_

Exploratory data analysis performed here:

[EDA](./notebooks/exploratory_cdwow.ipynb)
