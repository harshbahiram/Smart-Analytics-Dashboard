def generate_insights(df, profile):
    """Generate data quality and correlation insights."""
    insights = []

    for col, percent in profile[
        "missing_percentage"
    ].items():

        if percent > 30:

            insights.append(

                f"Column '{col}' contains "
                f"{percent}% missing values."

            )

    if profile["duplicate_rows"] > 0:

        insights.append(

            f"Dataset contains "
            f"{profile['duplicate_rows']} duplicate rows."

        )

    numeric_df = df.select_dtypes(
        include=['number']
    )

    if numeric_df.shape[1] >= 2:

        corr_matrix = numeric_df.corr()

        columns = corr_matrix.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                col1 = columns[i]
                col2 = columns[j]

                corr_value = corr_matrix.loc[
                        col1,
                        col2
                ]

                if corr_value > 0.7:
                    insights.append(
                        f"'{col1}' and '{col2}' "
                        f"have strong positive correlation "
                        f"({corr_value:.2f})."
                    )

                elif corr_value < -0.7:
                    insights.append(
                        f"'{col1}' and '{col2}' "
                        f"have strong negative correlation "
                        f"({corr_value:.2f})."
                    )

    if not insights:

        insights.append(
            "No major data quality issues detected."
        )

    return insights