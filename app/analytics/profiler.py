def generate_profile(df):

    missing_per_column = (
        df.isnull().sum().to_dict()
    )

    missing_percentage = (
        (df.isnull().sum() / len(df)) * 100

    ).round(2).to_dict()

    unique_values = (
        df.nunique()
        .to_dict()
    )

    profile = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": len(df.select_dtypes(include=['number']).columns),
        "categorical_columns": len(df.select_dtypes(include=['object']).columns),
        "missing_per_column": missing_per_column,
        "missing_percentage": missing_percentage,
        "unique_values": unique_values
    }
    return profile