from telegram import Update
from telegram.ext import ContextTypes
from user_tracker import UserTracker
from stats_manager import StatsManager

tracker = UserTracker()
stats = StatsManager(tracker)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    source = args[0] if args else "unknown"

    tracker.log_user_visit(user.id, user.username, user.full_name, source)

    data = stats.get_all_stats()

    await update.message.reply_text(
        f"👋 欢迎你, {user.full_name}!
"
        f"📊 今日访问用户数: {data['today_count']}
"
        f"🆕 新用户数: {data['new_today_count']}
"
        f"📈 活跃用户数: {data['active_today_count']}
"
        f"🌍 来源排行:
{data['top_sources']}"
    )
