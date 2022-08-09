import numpy as np
import pandas as pd

from bills.models import BillInquiry


def _process_service_column(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['service'] != '-']


def _process_number_column(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.number.astype(str).str.isnumeric()]


def _process_sum_column(df: pd.DataFrame) -> pd.DataFrame:
    df['sum'] = df['sum'].apply(lambda value: str(value).replace(',', '.'))
    df = df[pd.to_numeric(df['sum'], errors='coerce').apply(np.isfinite)]
    return df


def _process_date_column(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.date
    return df.dropna()


def process_bills_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df = df.rename(columns={'№': 'number'})
    df = _process_service_column(df)
    df = _process_number_column(df)
    df = _process_sum_column(df)
    df = _process_date_column(df)
    return df


def create_bill_inquiries_from_df(df: pd.DataFrame) -> None:
    bill_inquiries_data = df.to_dict('records')
    to_create = [BillInquiry(**data) for data in bill_inquiries_data]
    BillInquiry.objects.bulk_create(to_create, batch_size=len(to_create))
