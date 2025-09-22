from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean, CheckConstraint, UniqueConstraint, Index, Numeric, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from app import db

class Trainer(db.Model):
    """Represents a trainer - main user of the system."""
    
    __tablename__ = "trainers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)

    # For displaying sessions in calendars/exports
    timezone = Column(String(50), default="Europe/Kyiv", server_default="Europe/Kyiv")
    
    # Default is UAH, extendable in the future
    currency = Column(
        Enum("UAH", "USD", "EUR", name="currency_enum"),
        nullable=False,
        default="UAH",
        server_default="UAH"
    )
    
    # One-to-many: a trainer can have many clients
    clients = relationship(
        "Client",
        back_populates="trainer",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # One-to-many: each trainer have own exercises list
    exercises = relationship(
        "Exercise",
        back_populates="trainer",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Client(db.Model):
    """Represents a client - no own login, all data operated an added by the trainer"""

    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    trainer_id = Column(
        Integer, 
        ForeignKey("trainers.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    name = Column(String(100), nullable=False)
    contact = Column(String(100))
    notes = Column(Text)
    price = Column(Integer, nullable=False)
    status = Column(
        Enum("active", "pause", "archive", name="status_enum"),
        nullable=False,
        default="active",
        server_default="active"
    )

    # Many-to-one: each client can have only one trainer
    trainer = relationship("Trainer", back_populates="clients")
    
    # One-to-many: delete all sessions if client deleted
    sessions = relationship(
        "Session", 
        back_populates="client",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # UniqueConstraint - client names must be unique per trainer
    # Docs: https://docs.sqlalchemy.org/en/20/core/constraints.html
    __table_args__ = (
        UniqueConstraint('trainer_id', 'name', name='uq_client_name_per_trainer'),
        CheckConstraint("price >= 0", name="ck_client_price_nonnegative"),
    )

class Session(db.Model):
    """Represents a training session - schedule, result, payment status."""

    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    client_id = Column(
        Integer, 
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    start_dt = Column(DateTime(timezone=True), nullable=False, index=True)
    duration_min = Column(Integer, nullable=False, default=60, server_default="60")
    mode = Column(
        Enum("online", "offline", name="session_format"),
        nullable=False,
        default="offline",
        server_default="offline"
    )

    # no_show - trainer has the right to charge a fee.
    status = Column(
        Enum("planned","done","cancelled","no_show", name="session_status"),
        nullable=False,
        default="planned",
        server_default="planned"
    )
    price = Column(Integer, nullable=False)

    # is_paid default False - on db level for any db type
    # Docs: https://docs.sqlalchemy.org/en/20/core/sqlelement.html
    is_paid = Column(Boolean, nullable=False, default=False, server_default=expression.false())
    payment_date = Column(DateTime(timezone=True))
    notes = Column(Text)

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_session_price_nonnegative"),
        CheckConstraint("duration_min > 0", name="ck_session_duration_positive"),
    )

    client = relationship("Client", back_populates="sessions")
    session_exercises = relationship(
        "SessionExercise",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Exercise(db.Model):
    """Represents an exercise - reusable, can be linked to multiple sessions."""

    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True)
    trainer_id = Column(
        Integer, 
        ForeignKey("trainers.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    name = Column(String(100), nullable=False)
    description = Column(Text)

    trainer = relationship("Trainer", back_populates="exercises")

    # UniqueConstraint - exercise names must be unique per trainer
    __table_args__ = (
        UniqueConstraint('trainer_id', 'name', name='uq_exercise_name_per_trainer'),
    )

class SessionExercise(db.Model):
    """Represents an exercise performed in a specific session with details."""

    __tablename__ = "session_exercises"
    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer, 
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    exercise_id = Column(
        Integer, 
        ForeignKey("exercises.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    client_id = Column(
        Integer, 
        ForeignKey("clients.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    # Weight in kg, can be decimal
    weight = Column(Numeric(5, 2), nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        CheckConstraint("sets > 0", name="ck_session_exercise_sets_positive"),
        CheckConstraint("reps > 0", name="ck_session_exercise_reps_positive"),
        CheckConstraint("weight >= 0", name="ck_session_exercise_weight_nonnegative"),
        Index("ix_se_client_exercise", "client_id", "exercise_id")
    )

    session = relationship("Session", back_populates="session_exercises")