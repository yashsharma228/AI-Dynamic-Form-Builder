from extensions import db


class Field(db.Model):
    __tablename__ = "fields"
    __table_args__ = (
        db.Index("idx_fields_form_id", "form_id"),
        db.Index("idx_fields_sort_order", "form_id", "sort_order"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_id = db.Column(db.Integer, db.ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # text, email, number, date, time, select, checkbox, textarea
    placeholder = db.Column(db.String(255), nullable=True)
    is_required = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    options = db.Column(db.JSON, nullable=True)  # for select/radio/checkbox fields
    validation_rules = db.Column(db.JSON, nullable=True)  # e.g. {"min": 1, "max": 100, "pattern": "..."}

    form = db.relationship("Form", back_populates="fields")
