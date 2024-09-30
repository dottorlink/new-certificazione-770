# -*- coding: utf-8 -*-
"""
Base model for database

@File: base_models.py
@Date: 2024-08-08
"""

# Built-in/Generic Imports
import re
from datetime import date, datetime
from typing import Optional

from pydantic import ConfigDict, field_validator

# Libs
from sqlmodel import Field, Relationship, SQLModel

# Constants


# Class
class BaseModel(SQLModel):
    """Base SQL model

    Args:
        SQLModel (base class): SQL Base model
    """

    id: Optional[int] = Field(default=None, primary_key=True, title="ID")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, exclude=True)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        exclude=True,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_to_upper=True,
        use_enum_values=True,
        populate_by_name=True,
    )


class Setting(BaseModel, table=True, extend_existing=True):
    __tablename__ = "settings"

    # code_ente_prev: str = Field(
    #     title="Codice Ente Previdenziale", min_length=1, max_length=16
    # )

    # denom_ente_prev: str = Field(
    #     title="Denominazione Ente Previdenziale", min_length=1, max_length=50
    # )

    # code_somme_non_sogg: str = Field(
    #     title="Codice altre somme non soggette", min_length=1, max_length=2
    # )

    name: str = Field(title="Field code", min_length=1, max_length=20)
    title: str = Field(title="Field title", min_length=1)
    type: str = Field(title="Field Type", default="str", min_length=1)
    value: str = Field(title="Field type", min_length=1, max_length=100)


class Distributor(BaseModel, table=True, extend_existing=True):
    """Distributor class model

    Args:
        BaseModel (base SQL model): Base SQL model
        table (bool, optional): define if is table. Defaults to True.
        extend_existing (bool, optional): extend exists. Defaults to True.

    Raises:
        ValueError: validate error

    Returns:
        model: SQL model
    """

    __tablename__ = "distributors"

    # Distributor info
    number: str = Field(index=True, unique=True, title="Number")
    name: Optional[str] = Field(title="Name", max_length=20)
    last_name: str = Field(title="Last name", min_length=1, max_length=60)
    gender: str = Field(title="Gender", min_length=1, max_length=1, default="M")
    vat_number: Optional[str] = Field(title="VAT Number", default="")
    fiscal_code: str = Field(title="Fiscal Code", min_length=1, max_length=16)

    # Birth Info
    birth_date: date = Field(title="Birth Date")
    birth_city: str = Field(title="Birth City", min_length=1, max_length=62)
    birth_province: str = Field(title="Birth Province", min_length=1, max_length=2)

    # Residential infos
    residential_city: Optional[str] = Field(
        title="Residential City", default="", max_length=62
    )
    residential_province: Optional[str] = Field(
        title="Residential Province", default="", max_length=2
    )
    residential_address: Optional[str] = Field(
        title="Residential Address", default="", max_length=100
    )
    residential_zip_code: Optional[str] = Field(
        title="Residential ZIP Code", default="", max_length=5
    )

    invoices: list["Invoice"] = Relationship(
        back_populates="distributor",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_to_upper=True,
        use_enum_values=True,
        populate_by_name=True,
    )

    @field_validator("fiscal_code")
    @classmethod
    def check_valid_fiscal_code(cls, value: str) -> str:
        """Check valid fiscal code

        Args:
            value (str): fiscal code

        Raises:
            ValueError: Error if fiscal code is not valid

        Returns:
            str: valid fiscal code
        """
        regex = r"^([A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1})$|([0-9]{11})$"
        if not re.match(pattern=regex, string=value):
            raise ValueError("Invalid Fiscal Code. Control value format")
        return value

    @field_validator("vat_number")
    @classmethod
    def check_valid_vat_number(cls, value: str) -> str:
        """Check valid VAT Number

        Args:
            value (str): VAT Number

        Raises:
            ValueError: Error if VAT Number is not valid

        Returns:
            str: valid VAT Number
        """
        if len(value) == 0:
            return value
        regex = r"^[0-9A-Z]{11}$"
        if not re.match(pattern=regex, string=value):
            raise ValueError("Invalid VAT Number")
        return value

    @field_validator("birth_date")
    @classmethod
    def check_valid_age(cls, value: date) -> date:
        """Check valid age

        Args:
            date_of_birth (date): date of birth

        Raises:
            ValueError: Error if date of birth is minor of 18 age

        Returns:
            date: valid date
        """
        today = date.today()
        eighteen_years_ago = date(today.year - 18, today.month, today.day)

        if value > eighteen_years_ago:
            raise ValueError("Distributor must be at least 18 years old.")

        return value


class Company(BaseModel, table=True, extend_existing=True):
    """Company SQL model

    Args:
        BaseModel (SQL base model): SQL model
        table (bool, optional): define if is table. Defaults to True.
        extend_existing (bool, optional): extend exist. Defaults to True.
    """

    __tablename__ = "companies"

    # company info
    fiscal_code: str = Field(title="Fiscal Code", min_length=11, max_length=16)
    company_name: str = Field(
        index=True, unique=True, min_length=1, title="Company Name"
    )
    email: Optional[str] = Field(title="Company Email", default="")

    # Company address
    company_address: Optional[str] = Field(title="Address", default="", max_length=100)
    company_city: Optional[str] = Field(title="City", default="", max_length=60)
    company_province: Optional[str] = Field(title="Province", default="", max_length=2)
    company_zip_code: Optional[str] = Field(title="ZIP Code", default="", max_length=5)
    company_phone_number: Optional[str] = Field(title="Phone Number", default="")

    # Company company infos
    forniture_code: str = Field(title="Forniture Code", default="", min_length=1)
    activity_code: Optional[str] = Field(title="Activity Code", default="")
    activity_type: Optional[str] = Field(title="Activity Type", default="")

    @field_validator("fiscal_code")
    @classmethod
    def check_valid_fiscal_code(cls, value: str) -> str:
        """Check valid fiscal code

        Args:
            value (str): fiscal code

        Raises:
            ValueError: Error if fiscal code is not valid

        Returns:
            str: valid fiscal code
        """
        regex = r"^([A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1})$|([0-9]{11})$"
        if not re.match(pattern=regex, string=value):
            regex_2 = r"^[0-9A-Z]{11}$"
            if not re.match(pattern=regex_2, string=value):
                raise ValueError("Invalid Fiscal Code")
        return value

    @field_validator("email")
    @classmethod
    def check_valid_email(cls, value: str) -> str:
        """Check valid email

        Args:
            email (str): email

        Raises:
            ValueError: Error if email is not valid

        Returns:
            str: valid email
        """
        if len(value) == 0:
            return value
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern=regex, string=value):
            raise ValueError("Invalid email address")
        return value

    @field_validator("company_phone_number")
    @classmethod
    def check_valid_phone_number(cls, value: str) -> str:
        """Check valid phone number

        Args:
            value (str): phone number

        Raises:
            ValueError: Error if phone number is not valid

        Returns:
            str: valid phone number
        """
        if len(value) == 0:
            return value
        regex = r"^(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
        if not re.match(pattern=regex, string=value):
            raise ValueError("Invalid phone number")
        return value


class Invoice(BaseModel, table=True, extend_existing=True):
    """Invoice SQL Model

    Args:
        BaseModel (SQL base model): Base SQL model
        table (bool, optional): define if is table. Defaults to True.
        extend_existing (bool, optional): extend existing. Defaults to True.

    Returns:
         model: SQL model
    """

    __tablename__ = "invoices"

    number: Optional[str] = ""
    year: int
    mb_type: Optional[str] = "I"

    invoice_date: date
    distributor_number: str = Field(index=True, min_length=1)

    taxable_amount: Optional[float] = 0.0
    vat_amount: Optional[float] = 0.0
    inps_amount: Optional[float] = 0.0
    rit_amount: Optional[float] = 0.0
    total_amount: Optional[float] = 0.0

    aliquota_iva: Optional[float] = 0.0

    distributor_id: Optional[int] = Field(
        default=None, foreign_key="distributors.id", index=True
    )
    distributor: Optional[Distributor] = Relationship(back_populates="invoices")

    def __repr__(self):
        return f"{self.__class__.__qualname__}: ({self.id=!r}, {self.number=!r})"
