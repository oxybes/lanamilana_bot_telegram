from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, Boolean, MetaData, ForeignKey, DateTime, Float

Base = declarative_base()

class PurchasedSubscription(Base):
    __tablename__ = 'purchased_subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    data_start = Column(DateTime)
    data_end = Column(DateTime)

class ChannelsInCourse(Base):
    __tablename__ = 'channels_in_courses'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    channel_id = Column(String, ForeignKey('channels.id'))

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Integer)
    time = Column(Integer) #Срок курса в днях.
    purchased_subscriptions = relationship("PurchasedSubscription",backref="courses")
    channels = relationship("ChannelsInCourse", backref="courses")
    description = Column(String)
    is_delete = Column(Boolean, default=False)

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(String, primary_key=True)
    name = Column(String)
    link = Column(String)
    courses = relationship("ChannelsInCourse", backref="channels")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    chat_id = Column(Integer)
    mail = Column(String)
    phone = Column(String)
    is_main_admin = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_have_subscription = Column(Boolean, default=False)
    is_register = Column(Boolean, default=False)
    purchased_subscriptions = relationship("PurchasedSubscription", backref="users")
    lng = Column(String, default = "Russian")
    last_payload_timestamp = Column(Float)
    last_message_id_bot = Column(Integer)
    course_id = Column(Integer)
    subscribe_end = Column(Boolean, default=False)
    notification_off = Column(Boolean, default=False)

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key = True)
    mail = Column(String)
    phone = Column(String)
    course_id = Column(Integer)
    is_register = Column(Boolean, default = False)
