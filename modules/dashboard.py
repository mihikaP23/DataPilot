import plotly.express as px
import pandas as pd


# ==========================================================
# Helper Functions
# ==========================================================

def get_numeric_columns(df):
    """
    Returns all numeric columns.
    """

    return list(df.select_dtypes(include="number").columns)


def get_categorical_columns(df):
    """
    Returns all categorical columns.
    """

    return list(df.select_dtypes(include=["object", "category"]).columns)


# ==========================================================
# KPI Functions
# ==========================================================

def generate_kpis(df):
    """
    Generate dashboard KPIs.
    """

    kpis = {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Numeric Columns":
        len(get_numeric_columns(df)),

        "Categorical Columns":
        len(get_categorical_columns(df)),

        "Missing Values":
        int(df.isnull().sum().sum())

    }

    return kpis


# ==========================================================
# Bar Chart
# ==========================================================

def create_bar_chart(df, x_col, y_col):

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col} by {x_col}",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )

    return fig


# ==========================================================
# Line Chart
# ==========================================================

def create_line_chart(df, x_col, y_col):

    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        markers=True,
        title=f"{y_col} over {x_col}",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )

    return fig


# ==========================================================
# Scatter Plot
# ==========================================================

def create_scatter_plot(df, x_col, y_col):

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        title=f"{x_col} vs {y_col}",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col
    )

    return fig