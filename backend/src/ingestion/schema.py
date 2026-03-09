import pandera as pa
from pandera import Column, DataFrameSchema, Check


TELCO_SCHEMA = DataFrameSchema(
    {
        "customerid": Column(str, nullable=False),

        "gender": Column(
            str,
            checks=Check.isin(["Male", "Female"]),
            nullable=False,
        ),

        "seniorcitizen": Column(
            int,
            checks=Check.isin([0, 1]),
            nullable=False,
        ),

        "partner": Column(str, checks=Check.isin(["Yes", "No"])),
        "dependents": Column(str, checks=Check.isin(["Yes", "No"])),

        "tenure": Column(int, checks=Check.ge(0)),

        "phoneservice": Column(str, checks=Check.isin(["Yes", "No"])),
        "multiplelines": Column(
            str,
            checks=Check.isin(["Yes", "No", "No phone service"]),
        ),

        "internetservice": Column(
            str,
            checks=Check.isin(["DSL", "Fiber optic", "No"]),
        ),

        "onlinesecurity": Column(str),
        "onlinebackup": Column(str),
        "deviceprotection": Column(str),
        "techsupport": Column(str),
        "streamingtv": Column(str),
        "streamingmovies": Column(str),

        "contract": Column(
            str,
            checks=Check.isin(["Month-to-Month", "One year", "Two year"]),
        ),

        "paperlessbilling": Column(str, checks=Check.isin(["Yes", "No"])),

        "paymentmethod": Column(str),

        "monthlycharges": Column(float, checks=Check.ge(0)),
        "totalcharges": Column(float, checks=Check.ge(0), nullable=True),

        "churn": Column(str, checks=Check.isin(["Yes", "No"]), required=False, nullable=True),
    },
    strict=True,
)
