# IEEE Fraud Detection
## Information
It is a kaggle competition
[here](https://www.kaggle.com/c/ieee-fraud-detection/overview).
The purpose is to find out the probability of each transaction to be fraud.

## Download data
Click "Download All" [here](https://www.kaggle.com/c/ieee-fraud-detection/data).
Assuming it is called: data.zip.

Create folder called *data* and move .csv files into it.
```{shell}

mkdir data
unzip data.zip
rm -f data.zip
mv *.csv data
```

## Run notebook
jupyter-notebook FraudDetection.ipynb
