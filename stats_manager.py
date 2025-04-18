import logging
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models.user import User

class StatsManager:
    def __init__(self, user_tracker):
        self.logger = logging.getLogger("StatsManager")
        self.user_tracker = user_tracker
        self.db_url = os.environ.get("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL 环境变量未设置")
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_stats(self):
        try:
            today = datetime.today()
            today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
            week_start = today - timedelta(days=today.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            today_users = self.user_tracker.get_users_by_date_range(today_start, today_end)
            week_users = self.user_tracker.get_users_by_date_range(week_start, today_end)
            month_users = self.user_tracker.get_users_by_date_range(month_start, today_end)

            session = self.Session()
            all_users = set(user[0] for user in session.query(User.id).all())
            session.close()

            new_today = self.user_tracker.get_new_users_today()
            active_today = self.user_tracker.get_active_users_today()
            sources = self.user_tracker.get_sources_count()

            top_sources = sources.most_common(5)
            top_sources_text = "\n".join([f"{i+1}. {s}: {c} 用户" for i, (s, c) in enumerate(top_sources)])

            return {
                "today_count": len(today_users),
                "week_count": len(week_users),
                "month_count": len(month_users),
                "total_users_count": len(all_users),
                "new_today_count": new_today,
                "active_today_count": active_today,
                "top_sources": top_sources_text or "暂无来源数据"
            }
        except Exception as e:
            return {
                "today_count": 0,
                "week_count": 0,
                "month_count": 0,
                "total_users_count": 0,
                "new_today_count": 0,
                "active_today_count": 0,
                "top_sources": "获取统计信息时出错"
            }
