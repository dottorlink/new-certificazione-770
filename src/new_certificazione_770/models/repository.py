# -*- coding: utf-8 -*-
"""
Repository module

@File: repository.py
@Date: 2024-08-08
"""

# Built-in/Generic Imports
from typing import Any, List, Optional, Type, Union

# Libs
from sqlmodel import (
    Session,
    SQLModel,
    and_,
    create_engine,
    delete,
    desc,
    distinct,
    func,
    inspect,
    select,
)

# Own modules
from .base_models import Distributor, Invoice, Setting

# Constants
CONNECTION_DIALECT = "sqlite"


# Class
class Repository:
    """Repository class"""

    def __init__(self, database_path: str) -> None:
        """init

        Args:
            database_path (str): database file path
        """
        self.connection_string = f"{CONNECTION_DIALECT}:///" + f"{database_path}"
        self.model: SQLModel | None = None
        self.session = None
        self.engine = None

    def open_session(self, echo: Any = False) -> None:
        """Create SQL engine and open session

        Args:
            echo (Any, optional): set echo debug level. Defaults to False.
        """
        self.engine = create_engine(self.connection_string, echo=echo, echo_pool=True)
        self.session = Session(
            self.engine, autoflush=False, expire_on_commit=True, autocommit=False
        )

        SQLModel.metadata.create_all(bind=self.engine, checkfirst=True)

        self.upgrade_tables()

    def upgrade_tables(self):
        # Control settings.code_somme_non_sogg
        inspector = inspect(self.engine)
        columns = inspector.get_columns("settings")
        column_names = [column["name"] for column in columns]
        if "code_somme_non_sogg" not in column_names:
            Setting.__table__.drop(self.engine)
            SQLModel.metadata.create_all(bind=self.engine, checkfirst=True)

    def recreate_table(self) -> None:
        """Recreate table"""
        SQLModel.metadata.drop_all(self.engine)
        SQLModel.metadata.create_all(self.engine)

    def _construct_get_stmt(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        return stmt

    def _construct_list_stmt(self, **filters):
        """Construct SQL statement list

        Raises:
            ValueError: Return invalid column name

        Returns:
            statement: SQL statement
        """
        stmt = select(self.model)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self.model, c):
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self.model, c) == v)

        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))
        return stmt

    def _to_model_cls(self, obj) -> SQLModel:
        """Turn an object to item"""
        if isinstance(obj, self.model):
            return obj
        elif isinstance(obj, dict):
            return self.model(**obj)
        elif isinstance(obj, (list, tuple, set)):
            return self.model(*obj)
        else:
            raise TypeError(f"Cannot cast {type(obj)} to {self.model}")

    def _to_dict(self, item: Any, exclude_unset: bool = True) -> dict:
        """Transform model item into dict

        Args:
            item (Any): item to transform
            exclude_unset (bool, optional): set exclude unset value. Defaults to True.

        Returns:
            dict: item dict
        """
        if not item:
            return None
        if isinstance(item, dict):
            return item
        elif hasattr(item, "dict"):
            # Is pydantic
            return item.dict(exclude_unset=exclude_unset)
        else:
            d = vars(item)
            d.pop("_sa_model_cls _state", None)
            d.pop("_sa_instance_state", None)
            return d

    def _set_model(self, model: Any) -> SQLModel:
        """Set class model

        Args:
            model (Any): model

        Returns:
            SQLModel: SQL model
        """
        if isinstance(model, str):
            self.model = Type[model]
        else:
            self.model = model

    def get_by_id(self, model: Any, id: int) -> Optional[SQLModel]:
        """Get model item by id

        Args:
            model (Any): SQL model
            id (int): id

        Returns:
            Optional[SQLModel]: return SQLModel | None
        """
        self._set_model(model)
        stmt = select(self.model).where(self.model.id == id)
        return self.session.exec(stmt).first()

    def get_first(self, model: Any, **filters) -> Optional[SQLModel]:
        """Get first item by filters

        Args:
            model (Any): SQL model

        Returns:
            Optional[SQLModel]: SQL Model | None
        """
        self._set_model(model)
        stmt = self._construct_list_stmt(**filters)
        return self.session.exec(stmt).first()

    def list(self, model: Any, **filters) -> List[SQLModel]:
        """Get list for model by filters

        Args:
            model (Any): SQL Model

        Returns:
            List[SQLModel]: List of SQL Model | None
        """
        self._set_model(model)
        stmt = self._construct_list_stmt(**filters)
        return self.session.exec(stmt).all()

    def add(self, model: Any, record: Any) -> Optional[SQLModel]:
        """Add record for model

        Args:
            model (Any): SQL Model
            record (Any): record to add

        Raises:
            e: SQL Exception

        Returns:
            Optional[SQLModel]: SQL Model record added | None
        """
        self._set_model(model)
        try:
            self.session.add(record)
            self.session.commit()
            self.session.refresh(record)
            return record
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_table(self, model) -> None:
        """Delete model table

        Args:
            model (SQLModel): SQL model

        Raises:
            e: SQL Exception
        """
        self._set_model(model)
        try:
            stmt = delete(self.model)
            self.session.exec(stmt)
            self.session.commit()
            return
        except Exception as e:
            self.session.rollback()
            raise e

    # Delete\
    def delete(self, model: Any, ids: int | tuple[int]) -> bool:
        """Delete model item by id

        Args:
            model (SQLModel): SQL model
            id (int): record id

        Raises:
            e: SQL Exception

        Returns:
            bool: Return success action
        """
        self._set_model(model=model)
        if isinstance(ids, list):
            for _id in ids:
                record = self.get_by_id(model=model, id=_id)
                try:
                    self.session.delete(instance=record)
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
                    raise e
            return True
        else:
            record = self.get_by_id(model=model, id=int(ids))
            if record is not None:
                try:
                    self.session.delete(record)
                    self.session.commit()
                    return True
                except Exception as e:
                    self.session.rollback()
                    raise e
            return False

    # Delete all item by filter
    def delete_bulk(self, model: Any, **filters) -> int:
        """Delete all model item by filter

        Args:
            model (Any): SQL Model

        Raises:
            e: SQL Exception

        Returns:
            int: number of deleted record
        """
        self._set_model(model)
        try:
            stmt = self._construct_list_stmt(**filters)
            result = self.session.exec(stmt).all()
            for record in result:
                self.session.delete(record)
                self.session.commit()
            return len(result)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, model: Any, record: Any) -> SQLModel:
        """Update record model

        Args:
            model (Any): SQL Model
            record (Any): record

        Raises:
            e: SQL Exception

        Returns:
            SQLModel: updated record
        """
        self._set_model(model)
        try:
            self.session.add(record)
            self.session.commit()
            self.session.refresh(record)
            return record
        except Exception as e:
            self.session.rollback()
            raise e

    def upsert(
        self, model: Any, record: Any, columns: str | List[str]
    ) -> Union[SQLModel, bool]:
        """Update or insert if not exists a record for model. Use columns for where condition

        Args:
            model (Any): SQL Model
            record (Any): record to update or insert if not exists
            columns (str | List[str]): list of columns to use as where condition

        Returns:
            Union[SQLModel, bool]: insert or updated record | True if updated or False if inserted
        """
        self._set_model(model)
        if isinstance(columns, str):
            columns = [columns]

        try:
            # get specified model
            # get obj columns and designate matches
            match_on = [getattr(self.model, col) == record.get(col) for col in columns]

            # reduce clauses into statement
            statement = select(self.model).where(and_(*match_on))

            # check for existing record
            upsert_record = self.session.exec(statement).first()

            # prepare the record
            if upsert_record:
                _ = [setattr(upsert_record, key, record[key]) for key in record]
                is_updated = True
            else:
                upsert_record = self.model(**record)
                is_updated = False

            # add to the session
            self.session.add(upsert_record)
            self.session.commit()
            self.session.refresh(upsert_record)
            return upsert_record, is_updated
        except Exception as e:
            self.session.rollback()
            raise e

    def get_years_from_invoices(self) -> List[int]:
        """Get list of distinct years (int) from Invoices table

        Returns:
            List[int]: list of distinct years
        """
        stmt = select(distinct(Invoice.year)).order_by(desc(Invoice.year))
        return self.session.exec(stmt).all()

    def get_data_for_dat(self, year: int, limit: int | None = None) -> List:
        """Get data for DAT export

        Args:
            year (int): year
            limit (int | None, optional): number of record to limit. Defaults to None.

        Returns:
            List: list of records for CSV DAT
        """

        stmt = (
            select(
                Distributor.fiscal_code,
                Distributor.last_name,
                Distributor.name,
                Distributor.gender,
                Distributor.birth_date,
                Distributor.birth_city,
                Distributor.birth_province,
                func.sum(Invoice.taxable_amount).label("taxable_amount"),
                func.sum(Invoice.taxable_amount * 0.22).label("taxable_amount_ri"),
                func.sum(Invoice.rit_amount).label("rit_amount"),
                func.sum(Invoice.inps_amount).label("inps_amount"),
                func.sum(Invoice.total_amount).label("total_amount"),
            )
            .where(and_(Distributor.id == Invoice.distributor_id, Invoice.year == year))
            .group_by(
                Distributor.id,
                Distributor.number,
                Distributor.name,
                Distributor.last_name,
            )
            .order_by(desc(Distributor.number))
        )

        if limit is not None:
            stmt = stmt.limit(limit)

        return self.session.exec(stmt).all()
