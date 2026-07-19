import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)


# ==========================================================
# GET NUMERIC COLUMNS
# ==========================================================

def get_numeric_columns(df):

    return list(df.select_dtypes(include="number").columns)


# ==========================================================
# TRAIN MODEL
# ==========================================================

def train_model(df, target_column):

    numeric_df = df.select_dtypes(include="number").copy()

    if target_column not in numeric_df.columns:

        raise ValueError(
            "Target column must be numeric."
        )

    X = numeric_df.drop(columns=[target_column])

    y = numeric_df[target_column]

    if X.shape[1] == 0:

        raise ValueError(
            "No feature columns available."
        )

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42

    )

    model = LinearRegression()

    model.fit(

        X_train,

        y_train

    )

    predictions = model.predict(X_test)

    mse = mean_squared_error(

        y_test,

        predictions

    )

    rmse = np.sqrt(mse)

    metrics = {

        "R2 Score":

            round(

                r2_score(

                    y_test,

                    predictions

                ),

                4

            ),

        "MAE":

            round(

                mean_absolute_error(

                    y_test,

                    predictions

                ),

                4

            ),

        "MSE":

            round(

                mse,

                4

            ),

        "RMSE":

            round(

                rmse,

                4

            )

    }

    prediction_df = pd.DataFrame({

        "Actual":

            y_test.values,

        "Predicted":

            predictions

    })

    return (

        model,

        prediction_df,

        metrics

    )


# ==========================================================
# FUTURE PREDICTION
# ==========================================================

def predict_new_data(

        model,

        input_df

):

    prediction = model.predict(

        input_df

    )

    return prediction