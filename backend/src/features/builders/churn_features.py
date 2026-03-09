import pandas as pd
from sklearn.preprocessing import LabelEncoder
from src.features.contracts.churn_v1 import FEATURE_SCHEMA_V1

Binary_columns=[
    "seniorcitizen",
    "partner",
    "dependents",
    "phoneservice",
    "multiplelines",
    "onlinesecurity",
    "onlinebackup",
    "deviceprotection",
    "techsupport",
    "streamingtv",
    "streamingmovies",
    "paperlessbilling",
    # churn is the label — handled separately below, only when present
]


Categorical_columns=[
    "contract",
    "paymentmethod",
    "internetservice"
]

Services_columns=[
    "phoneservice",
    "multiplelines",
    "onlinesecurity",
    "onlinebackup",
    "deviceprotection",
    "techsupport",
    "streamingtv",
    "streamingmovies",
]

Addon_services_columns=[
    "onlinesecurity",
    "onlinebackup",
    "deviceprotection",
    "techsupport",
]


def normalize_binary_columns(df: pd.DataFrame) -> pd.DataFrame:

    df=df.copy()
    for col in Binary_columns:
        if col in df.columns:   # skip columns absent in inference data
            df[col]=(df[col].replace({"Yes":1,"No":0,True:1,False:0,"No internet service":0,"No phone service":0}).astype(int))
    return df


def encode_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:

    df=df.copy()
    encoders={}
    for col in Categorical_columns:
        le=LabelEncoder()
        values=df[col].astype(str)

        encoded=le.fit_transform(values)
        new_cols=f"{col}_le"
        df[new_cols]=encoded
        encoders[col]=le

    return df, encoders


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:

    df=df.copy()
    df["services_cnt"]=df[Services_columns].sum(axis=1)
    df['addon_services_cnt']=df[Addon_services_columns].sum(axis=1)
    return df

def add_snapshot_metadata(df: pd.DataFrame,
                          snapshot_date:  str,
                           feature_version: str="v1", 
                           source: str = "prod") -> pd.DataFrame:

    df=df.copy()
    df["snapshot_date"]=pd.to_datetime(snapshot_date)
    df["feature_version"]=feature_version
    df["source"]=source
    return df


def validated_feature_contract(df):
    allowed_cols=set(FEATURE_SCHEMA_V1.columns.keys())
    df=df[[col for col in df.columns if col in allowed_cols]]
    validated_df=FEATURE_SCHEMA_V1.validate(df)
    return validated_df


def build_churn_features(df: pd.DataFrame,
                         snapshot_date: str,
                         feature_version: str = "v1",
                         source: str = "prod") -> pd.DataFrame:

    df=normalize_binary_columns(df)
    df, encoders = encode_categorical_columns(df)
    df=add_derived_features(df)
    df=add_snapshot_metadata(df, snapshot_date=snapshot_date, feature_version=feature_version, source=source)

    # Encode churn label only when present (training data). Skip for inference data.
    if "churn" in df.columns:
        df["churn"] = (df["churn"].replace({"Yes": 1, "No": 0, True: 1, False: 0}).astype(int))

    validated_df=validated_feature_contract(df)

    return validated_df,encoders


