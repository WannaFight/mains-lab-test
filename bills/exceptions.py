class DataFrameColumnsMismatch(Exception):
    """Raised when DataFrame columns do not match any
    of the existing mappings defined in ``settings.EXCEL_COLUMNS_MAPPING``
    """
    pass
