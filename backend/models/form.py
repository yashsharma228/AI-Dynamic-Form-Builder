from datetime import UTC, datetime

from extensions import db


class Form(db.Model):
    __tablename__ = "forms"
    __table_args__ = (
        db.Index("idx_forms_created_at", "created_at"),
        db.Index("idx_forms_is_active", "is_active"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    fields = db.relationship(
        "Field",
        back_populates="form",
        cascade="all, delete-orphan",
        order_by="Field.sort_order",
        lazy=True,
    )
    responses = db.relationship(
        "Response",
        back_populates="form",
        cascade="all, delete-orphan",
        lazy=True,
    )
