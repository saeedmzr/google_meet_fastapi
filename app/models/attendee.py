from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Attendee(Base):
    __tablename__ = "attendees"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    meeting = relationship("Meeting", back_populates="attendees")