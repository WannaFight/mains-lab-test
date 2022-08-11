import numpy as np
import pandas as pd
from django.conf import settings

from bills.exceptions import DataFrameColumnsMismatch
from bills.models import BillInquiry


def _process_service_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with `-` values"""
    return df[df['service'] != '-']


def _process_number_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with non ``int`` values"""
    return df[df.number.astype(str).str.isnumeric()]


def _process_sum_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with no ``float`` nor ``int`` values"""
    df['sum'] = df['sum'].apply(lambda value: str(value).replace(',', '.'))
    df = df[pd.to_numeric(df['sum'], errors='coerce').apply(np.isfinite)]
    return df


def _process_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with wrong date"""
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.date
    return df.dropna()


def _rename_df_columns(df: pd.DataFrame, rules: list[dict]) -> pd.DataFrame:
    """Rename columns of different dataframes to common format"""
    df_columns = sorted(df.columns)

    for rule in rules:
        mapping_columns = sorted(rule.keys())

        if mapping_columns == df_columns:
            df = df.rename(columns=rule)
            return df

    raise DataFrameColumnsMismatch(f"Can not rename dataframe columns")


def process_bills_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df = _rename_df_columns(df, rules=settings.EXCEL_COLUMNS_MAPPING)
    df = _process_service_column(df)
    df = _process_number_column(df)
    df = _process_sum_column(df)
    df = _process_date_column(df)
    return df


def create_bill_inquiries_from_df(df: pd.DataFrame) -> None:
    """Create ``BillInquiry`` instances from given dataframe"""
    bill_inquiries_data = df.to_dict('records')
    to_create = [BillInquiry(**data) for data in bill_inquiries_data]
    BillInquiry.objects.bulk_create(to_create, batch_size=len(to_create))
