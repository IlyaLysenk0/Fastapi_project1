from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt

DATABASE_URL = "mysql+aiomysql://root:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()







class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    description = Column(String(1000))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    image_url = Column(String(250), nullable=True)
    status = Column(String(250), default="В обробці")

    user_id = Column(Integer, ForeignKey("users.id"))
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # адміністратор, що взяв у роботу

    user = relationship("User", foreign_keys=[user_id], back_populates="problems")
    admin = relationship("User", foreign_keys=[admin_id],back_populates="assigned_problems")

    response = relationship("AdminResponse", back_populates="problem", uselist=False)
    service_record = relationship("ServiceRecord", back_populates="problem", uselist=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    is_admin = Column(Boolean, default=False)

    problems = relationship("Problem", foreign_keys=[Problem.user_id],back_populates="user")
    assigned_problems = relationship("Problem", foreign_keys=[Problem.admin_id], back_populates="admin")
    responses = relationship("AdminResponse", back_populates="admin")

    def set_password(self, raw_password: str):
        hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed.decode("utf-8")  # зберігаємо як str

    def verify_password(self, raw_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password.encode("utf-8"))


class AdminResponse(Base):
    __tablename__ = "admin_responses"
    id = Column(Integer, primary_key=True)
    message = Column(String(1000))
    date_responded = Column(DateTime(timezone=True), server_default=func.now())

    admin_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("problems.id"))

    admin = relationship("User", back_populates="responses")
    problem = relationship("Problem", back_populates="response")



class ServiceRecord(Base):
    __tablename__ = "service_records"
    id = Column(Integer, primary_key=True)
    work_done = Column(String(1000))
    date_completed = Column(DateTime(timezone=True), server_default=func.now())
    parts_used = Column(String(1000), nullable=True)  # можеш пізніше зробити окрему таблицю
    warranty_info = Column(String(1000))

    problem_id = Column(Integer, ForeignKey("problems.id"))

    problem = relationship("Problem", back_populates="service_record")





class Users_in_telegram(Base):
    __tablename__ = "users_in_telegram"
    id = Column(Integer, primary_key=True)
    tg_code = Column(String(100))
    user_tg_id = Column(String(50), nullable=True)
    user_in_site = Column(Integer,ForeignKey('users.id'))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
