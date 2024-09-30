# -*- coding: utf-8 -*-
"""
Controller class module

@File: controller.py
@Date: 2024-08-08
"""

# Built-in/Generic Imports
from typing import Any, Dict

# Own modules
from models import Company, Distributor, Invoice, Repository, Setting


# Errors
class KeyAttributeNotFoundError(ValueError):
    """KeyAttributeNotFoundError

    Args:
        ValueError (_type_): Key attribute not found
    """


class NoDataFoundError(ValueError):
    """NoDataFoundError

    Args:
        ValueError (_type_): No Data Found Error
    """


# Class
class Controller:
    """Controller Class"""

    def __init__(self, db_path: str, echo: Any = False):
        """Init

        Args:
            db_path (str): database file path
            echo (Any, optional): SQL echo flag. Defaults to False.
        """
        # Create Repository object
        self.repository = Repository(database_path=db_path)
        self.repository.open_session(echo=echo)

    def get_distributor_by_id(self, id: int) -> dict | None:
        """Get distributor by id

        Args:
            id (int): record id

        Returns:
            dict | None: record
        """
        record = self.repository.get_by_id(model=Distributor, id=id)
        return (
            record.model_dump(exclude={"created_at", "updated_at"}) if record else None
        )

    def delete_distributor_by_id(self, ids: int | tuple[int]) -> None:
        """Delete distributor by id

        Args:
            id (int): record id

        Raises:
            ValueError: No distributor found for id
        """
        if self.repository.delete(model=Distributor, ids=ids):
            return
        msg = f"No Distributor found for {ids=}"
        raise NoDataFoundError(msg)

    def import_data(self, data: Any, model: str):
        """Import data

        Args:
            data (Any): Data item to import
            model (str): Model type

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if model == Distributor.__name__:
            return self.import_distributor(data)
        elif model == Invoice.__name__:
            return self.import_invoice(data)
        else:
            msg = f"Model unknown: {model=}"
            raise ValueError(msg)

    def import_invoice(self, record: Any) -> tuple[Dict[str, Any] | None, bool]:
        """Import data into Invoices table

        Args:
            record (Any): data record

        Raises:
            KeyAttributeNotFoundError: Key attribute not found
            NoDataFoundError: No Distributor found

        Returns:
            tuple[Dict[str, Any] | None, bool]: record inserted, False
        """
        key = "distributor_number"
        if dict(record).get(key, None) is None:
            msg = f"Item has not {key} attribute or {key} value is None"
            raise KeyAttributeNotFoundError(msg)

        number = record[key]
        filters = {"number": number}

        _distributor = self.repository.get_first(Distributor, **filters)
        if _distributor is None:
            msg = f"No Distributor found with {number=}"
            raise NoDataFoundError(msg)

        record["distributor_id"] = _distributor.id
        _invoice = Invoice(**record)
        _invoice = self.repository.add(model=Invoice, record=_invoice)
        return (
            _invoice.model_dump(exclude={"created_at", "updated_at"})
            if _invoice
            else None
        ), False

    def import_distributor(self, record: Any) -> tuple[Dict[str, Any] | None, bool]:
        """Import data into Distributor table

        Args:
            record (Any): data record

        Raises:
            KeyAttributeNotFoundError: attribute not found

        Returns:
            tuple[Dict[str, Any] | None, bool]: record inserted or updated, is update
        """
        key = "number"
        if dict(record).get(key, None) is None:
            msg = f"Item has not [{key}] attribute or value is None"
            raise KeyAttributeNotFoundError(msg)

        _record, is_updated = self.repository.upsert(
            model=Distributor, record=record, columns=key
        )
        return (
            _record.model_dump(exclude={"created_at", "updated_at"})
            if _record
            else None
        ), is_updated

    def update_distributor(self, record: Any) -> tuple[Dict[str, Any] | None, bool]:
        """_summary_

        Args:
            record (Any): record data

        Returns:
            tuple[Dict[str, Any] | None, bool]: record inserted or updated, is update
        """
        key = "id"
        if dict(record).get(key, None):
            _record, is_updated = self.repository.upsert(
                model=Distributor, record=record, columns=key
            )
        else:
            _record = Distributor(**record)
            _record = self.repository.add(model=Distributor, record=_record)
            is_updated = False
        return (
            _record.model_dump(exclude={"created_at", "updated_at"})
            if _record
            else None
        ), is_updated

    def update_company(self, record: Any) -> tuple[Dict[str, Any] | None, bool]:
        """Update or insert record in Company table

        Args:
            record (Any): record data

        Returns:
            tuple[Dict[str, Any] | None, bool]: record inserted or updated, is update
        """
        key = "id"
        if dict(record).get(key, None):
            _record, is_updated = self.repository.upsert(
                model=Company, record=record, columns=key
            )
        else:
            _record = Company(**record)
            _record = self.repository.add(model=Company, record=_record)
            is_updated = False
        return (
            _record.model_dump(exclude={"created_at", "updated_at"})
            if _record
            else None
        ), is_updated

    def update_settings(self, record: Any) -> tuple[Dict[str, Any] | None, bool]:
        """Update or insert record in Setting table

        Args:
            record (Any): record data

        Returns:
            tuple[Dict[str, Any] | None, bool]: record inserted or updated, is update
        """
        key = "id"
        if dict(record).get(key, None):
            _record, is_updated = self.repository.upsert(
                model=Setting, record=record, columns=key
            )
        else:
            _record = Setting(**record)
            _record = self.repository.add(model=Setting, record=_record)
            is_updated = False
        return (
            _record.model_dump(exclude={"created_at", "updated_at"})
            if _record
            else None
        ), is_updated

    def get_all_distributors(self) -> list:
        """Get all Distributor from table

        Returns:
            list: list of distributor
        """
        records = self.repository.list(Distributor)
        return (
            list(
                [
                    row.model_dump(mode="json", exclude={"created_at", "updated_at"})
                    for row in records
                ]
            )
            if records
            else None
        )

    def get_company(self) -> Dict[str, Any] | None:
        """Get first Company record

        Returns:
            Dict[str, Any] | None: company record | None
        """
        _record = self.repository.get_first(Company)
        return (
            _record.model_dump(exclude={"created_at", "updated_at"})
            if _record
            else None
        )

    def get_settings(self) -> Dict[str, Any] | None:
        """Get first Company record

        Returns:
            Dict[str, Any] | None: company record | None
        """
        _record = self.repository.get_first(Setting)
        return (
            _record.model_dump(exclude={"created_at", "updated_at"})
            if _record
            else None
        )

    def get_years_from_invoices(self) -> list:
        """Get distinct years from Invoice table

        Returns:
            list: list of year (int)
        """
        records = self.repository.get_years_from_invoices()
        return records

    def get_data_for_export_dat(
        self, year: int, limit: int | None = None
    ) -> list | None:
        """Get data for CSV DAT export

        Args:
            year (int): year
            limit (int | None, optional): limit for records return or All. Defaults to None.

        Raises:
            ValueError: Model unknown

        Returns:
            list | None: lst of records or None
        """
        records = self.repository.get_data_for_dat(year, limit=limit)
        return list([row for row in records]) if records else None

    def delete_table(self, model: str) -> None:
        """Delete model table

        Args:
            model (Any): model

        Raises:
            ValueError: model unknown error
        """
        if model == Distributor.__name__:
            self.repository.delete_table(model=Distributor)
        elif model == Invoice.__name__:
            self.repository.delete_table(model=Invoice)
        else:
            msg = f"Model unknown: {model=}"
            raise ValueError(msg)
