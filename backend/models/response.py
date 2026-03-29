from datetime import UTC, datetime

from extensions import db


class Response(db.Model):
    __tablename__ = "responses"
    __table_args__ = (
        db.Index("idx_responses_form_id", "form_id"),
        db.Index("idx_responses_submitted_at", "submitted_at"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_id = db.Column(db.Integer, db.ForeignKey("forms.id", ondelete="CASCADE"), nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    respondent_email = db.Column(db.String(255), nullable=True)  # optional for tracking
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    form = db.relationship("Form", back_populates="responses")
