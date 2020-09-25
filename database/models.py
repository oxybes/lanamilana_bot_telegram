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



class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Integer)
    time = Column(Integer) #Срок курса в днях.
    purchased_subscriptions = relationship("PurchasedSubscription",backref="courses")
    # users = relationship("User", backref="courses")
    # purchasedSubsriptions = relationship("purchased_subscriptions", backref='course')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    mail = Column(String)
    phone = Column(String)
    is_main_admin = Column(Boolean)
    is_admin = Column(Boolean)
    is_have_subscription = Column(Boolean)
    is_kick = Column(Boolean)
    ending_date = Column(DateTime)
    purchased_subscriptions = relationship("PurchasedSubscription", backref="users")
    # course_id = Column(Integer, ForeignKey('courses.id'))
    lng = Column(String)
    balance = Column(Float, default=0.0)
    # purchasedSubsriptions = relationship("purchased_subscriptions", backref='user')


# class PurchasedSubscription(Base):
#     __tablename__ = 'purchased_subscriptions'
#     id = Column(Integer, primary_key = True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     course_id = Column(Integer, ForeignKey('courses.id'))
#     date_start = Column(DateTime)
#     date_end = Column(DateTime)

