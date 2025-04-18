import logging
import os
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.user import User

class UserTracker:
    def __init__(self):
        self.logger = logging.getLogger("UserTracker")
        self.db_url = os.environ.get("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL 环境变量未设置")
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

    def log_user_visit(self, user_id, username, full_name, source):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            now = datetime.now()
            if user:
                user.last_active = now
                user.visit_count += 1
                user.username = username
                user.full_name = full_name
            else:
                new_user = User(
                    id=user_id,
                    username=username,
                    full_name=full_name,
                    source=source,
                    first_seen=now,
                    last_active=now,
                    visit_count=1
                )
                session.add(new_user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
        finally:
            session.close()

    def get_users_by_date_range(self, start, end):
        session = self.Session()
        result = set()
        try:
            users = session.query(User).filter(User.last_active.between(start, end)).all()
            for user in users:
                result.add(user.id)
        finally:
            session.close()
        return result

    def get_new_users_today(self):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        session = self.Session()
        try:
            return session.query(func.count(User.id)).filter(User.first_seen.between(today, tomorrow)).scalar() or 0
        finally:
            session.close()

    def get_active_users_today(self):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        session = self.Session()
        try:
            return session.query(func.count(User.id)).filter(User.last_active.between(today, tomorrow)).scalar() or 0
        finally:
            session.close()

    def get_sources_count(self):
        session = self.Session()
        counter = Counter()
        try:
            rows = session.query(User.source, func.count(User.id)).group_by(User.source).all()
            for source, count in rows:
                counter[source] = count
        finally:
            session.close()
        return counter
