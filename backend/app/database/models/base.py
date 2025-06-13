from sqlalchemy import Column, Integer, DateTime, String, text
from sqlalchemy.sql import func
from sqlalchemy.types import TypeDecorator, VARCHAR
import uuid
from ..connection import Base


class EnumAsStr(TypeDecorator):
    """Persist Python enums as their string values in a VARCHAR column."""

    impl = VARCHAR
    cache_ok = True

    def __init__(self, enum_class, length=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class
        # Use length provided or default to 50 for the VARCHAR
        self.impl = VARCHAR(length if length is not None else 50)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_class):
            return value.value
        # Optionally, could raise an error if 'value' is a string not matching enum values
        # For now, assume if it's not an enum member, it might be a pre-validated string value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        try:
            return self.enum_class(
                value
            )  # This looks up by value e.g. QuestionType('multiple_choice')
        except ValueError as e:
            # This provides a more informative error if a string from DB isn't a valid enum value
            raise ValueError(
                f"Invalid value '{value}' for enum {self.enum_class.__name__}. "
                f"Possible values: {[item.value for item in self.enum_class]}"
            ) from e


class TimestampedModel(Base):
    """
    Abstract base model with common fields for all models.
    This model is not created in the database
    """

    __abstract__ = True

    # UUID primary key as String for MySQL compatibility
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteModel(TimestampedModel):
    """
    Abstract base model with soft delete functionality.
    """

    __abstract__ = True

    # Soft delete flag
    is_deleted = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    def soft_delete(self):
        """
        Soft delete the model.
        """
        self.is_deleted = func.now()
