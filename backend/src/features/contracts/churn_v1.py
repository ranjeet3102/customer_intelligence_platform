import pandera as pa
from pandera import Column, DataFrameSchema, Check


#identity columns
identity_column = {
    "customerid": Column(
        pa.String,
        nullable=False,
        description="Unqiue customer identifier",
    ),

    "snapshot_date": Column(
        pa.DateTime,
        nullable=False,
        description="Feature snapshot date",
    ),

    "feature_version": Column(
        pa.String,
        nullable=False,
        checks=Check.isin(["v1"]),
        description="Feature contract version",
        ),

    "source": Column(
        pa.String,
        nullable=False,
        checks=Check.isin(["prod","csv"]),
        description="Data origin",
    ),
}
    

    
#numeric continuous columns
numeric_columns = {
    "tenure":Column(
        pa.Int,
        nullable=False,
        checks=Check.ge(0),
        description = "Customer tenure in months"
    ),

    "monthlycharges":Column(
        pa.Float,
        nullable=False,
        checks=Check.ge(0),
        description="Monthly billing amount",
    ),

    "totalcharges":Column(
        pa.Float,
        nullable=False,
        checks=Check.ge(0),
        description="Total billing amount",
    ),
}
    
    
#Binary categorical columns
binary_features={
    "seniorcitizen":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "partner":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "dependents":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "phoneservice":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "multiplelines":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "onlinesecurity":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "onlinebackup":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "deviceprotection":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "techsupport":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "streamingtv":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "streamingmovies":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),

    "paperlessbilling":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
    ),
}


#Encoding cagtegorical columns
encoded_features={
    "contract_le":Column(
        pa.Int,
        nullable=False,
        checks=Check.ge(0),
        description="Label encoded contract type",
    ),

    "paymentmethod_le":Column(
        pa.Int,
        nullable=False,
        checks=Check.ge(0),
        description="Label encoded payment method",
    ),

    "internetservice_le":Column(
        pa.Int,
        nullable=False,
        checks=Check.ge(0),
        description="Label encoded internet service type",
    ),
}


#Derived Aggregate features
derived_features={
    "services_cnt":Column(
        pa.Int,
        nullable=False,
        checks=Check.ge(0),
        description="Total subscribed services count",
    ),

    "addon_services_cnt":Column(
        pa.Int,
        nullable=False,
        checks=Check.ge(0),
        description="Total subscribed addon services count",
    )
}
    

#label column
label_schema={
    "churn":Column(
        pa.Int,
        nullable=False,
        checks=Check.isin([0,1]),
        required=False,
        description="Churn Label",
    )
}
    
    

#final features
FEATURE_SCHEMA_V1 = DataFrameSchema(
    columns={
        **identity_column,
        **numeric_columns,
        **binary_features,
        **encoded_features,
        **derived_features,
        **label_schema
},
strict=True,unique=[["customerid","snapshot_data"]],)


