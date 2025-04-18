import os
from telegram.ext import Updater, CommandHandler

# 定义异步的处理函数
async def start_handler(update, context):
    user = update.message.from_user
    data = {
        'today_count': 123,
        'new_today_count': 10,
        'active_today_count': 45,
        'top_sources': 'Telegram, Website'
    }

    # 使用 await 来发送异步消息
    await update.message.reply_text(
        f"""👋 欢迎你, {user.full_name}!
📊 今日访问用户数: {data['today_count']}
🆕 新用户数: {data['new_today_count']}
📈 活跃用户数: {data['active_today_count']}
🌍 来源排行:
{data['top_sources']}"""
    )

def main():
    # 获取 Render 分配的端口
    port = int(os.environ.get("PORT", 8080))

    # 使用 token 创建 Updater 对象
    updater = Updater("YOUR TELEGRAM BOT TOKEN", use_context=True)
    
    # 获取调度器
    dispatcher = updater.dispatcher
    
    # 添加命令处理器
    dispatcher.add_handler(CommandHandler("start", start_handler))
    
    # 启动机器人并绑定端口
    updater.start_polling(poll_interval=5, timeout=10)
    
    # 使用指定的端口
    updater.start_webhook(listen="0.0.0.0", port=port)
    
    updater.idle()

if __name__ == '__main__':
    main()
