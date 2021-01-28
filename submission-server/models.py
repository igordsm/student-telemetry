from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    lms_user = Column(String)
    is_prof = Column(Boolean, default=False)
    token = Column(String, default='')

    courses = relationship('Course', back_populates='responsible')
    submissions = relationship('Submission', back_populates='sender')

    def __init__(self, **kwargs):
        kwargs['token'] = str(uuid.uuid4())
        super().__init__(**kwargs)
        


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    name = Column(String)
    responsible_id = Column(Integer, ForeignKey('users.id'))

    responsible = relationship('User', back_populates='courses')
    activities = relationship('Activity', back_populates='course')


class ActivityType(enum.Enum):
    multiple_choice = 'multiple_choice'
    code = 'code'


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, Sequence('activity_id_seq'), primary_key=True)
    course_specific_id = Column(String)
    course_id = Column(Integer, ForeignKey('courses.id'))
    type = Column(Enum(ActivityType), default=ActivityType.multiple_choice)

    course = relationship('Course', back_populates='activities')
    submissions = relationship('Submission', back_populates='activity')

    UniqueConstraint(course_specific_id, course_id, name='unique_course_specific_id_by_course')


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, Sequence('submission_id_seq'), primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    activity_id = Column(Integer, ForeignKey('activities.id'))
    content = Column(String)

    sender = relationship('User', back_populates='submissions')
    activity = relationship('Activity', back_populates='submissions') 