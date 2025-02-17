from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    requested_data = Column(JSON)
    response_data = Column(JSON)
    meeting_url = Column(String, nullable=True)
    event_id = Column(String, nullable=True)
    attendees = relationship("Attendee", back_populates="meeting")