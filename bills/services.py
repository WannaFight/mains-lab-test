import logging
import random

import numpy as np
import pandas as pd
from django.conf import settings

from bills.exceptions import DataFrameColumnsMismatch
from bills.models import BillInquiry, ServiceClass


logger = logging.getLogger(__name__)


def _process_service_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with `-` values"""
    logger.info("Processing service column...")
    return df[df['service'] != '-']


def _process_number_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with non ``int`` values"""
    logger.info("Processing number column...")
    return df[df.number.astype(str).str.isnumeric()]


def _process_sum_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with no ``float`` nor ``int`` values"""
    logger.info("Processing sum column...")
    df['sum'] = df['sum'].apply(lambda value: str(value).replace(',', '.'))
    df = df[pd.to_numeric(df['sum'], errors='coerce').apply(np.isfinite)]
    return df


def _process_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with wrong date"""
    logger.info("Processing date column...")
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


def _exclude_existing_bills(data: list[dict]) -> list[dict]:
    """Exclude items from ``data`` with values of ``client_name``
    and ``number`` that already exists in database
    """
    existing_clients_with_bills = list(
        BillInquiry.objects.values_list(
            'client_name', 'number'
        )
    )
    data = [
        item for item in data
        if (item['client_name'], item['number'])
        not in existing_clients_with_bills
    ]
    return data


def create_bill_inquiries_from_df(df: pd.DataFrame) -> None:
    """Create ``BillInquiry`` instances from given dataframe"""
    bill_inquiries_data = df.to_dict('records')
    bill_inquiries_data = _exclude_existing_bills(bill_inquiries_data)
    service_class_ids = ServiceClass.objects.values_list('pk', flat=True)

    to_create = [
        BillInquiry(
            **data,
            service_class_id=random.choice(service_class_ids) or None
        ) for data in bill_inquiries_data
    ]

    if to_create:
        BillInquiry.objects.bulk_create(to_create, batch_size=len(to_create))
        logger.info(f"Created {len(to_create)} BillInquiry instances")
    else:
        logger.info(
            "Skipped all records from dataframe, "
            "because they already exist in database"
        )
