import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)


class ExerciseHistory(Base):
    __tablename__ = "exercise_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    module = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    parameters = Column(JSON, nullable=False)
    result_summary = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
