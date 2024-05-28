from telebot.types import Message
import datetime
from bson import ObjectId
from .admin import is_user_admin, is_bot_admin

def handle_report(message: Message, db, bot):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command can only be used in group chats.")
        return

    if message.reply_to_message:
        reported_user = message.reply_to_message.from_user
        reported_user_info = f"@{reported_user.username}" if reported_user.username else f"{reported_user.first_name} {reported_user.last_name}"
        report_text = message.text[len('/report '):].strip()

        if not report_text:
            bot.reply_to(message, "Please provide a reason for the report.")
            return

        report_details = {
            "group_id": message.chat.id,
            "reported_user_id": reported_user.id,
            "reported_user_info": reported_user_info,
            "reporter_user_id": message.from_user.id,
            "reporter_user_info": f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name,
            "report_text": report_text,
            "timestamp": datetime.datetime.now()
        }

        # Save the report to the database
        reports_collection = db["reports"]
        reports_collection.insert_one(report_details)

        # Prepare the report message
        report_message = (
            f"🚨 <b>Report</b> 🚨\n"
            f"Reported User: {reported_user_info}\n"
            f"Reported By: {report_details['reporter_user_info']}\n"
            f"Reason: {report_text}"
        )

        # Send the report to all admins
        for admin in bot.get_chat_administrators(message.chat.id):
            try:
                bot.send_message(admin.user.id, report_message, parse_mode='HTML')
            except Exception as e:
                print(f"Could not send report to {admin.user.id}")

        bot.reply_to(message, "The report has been sent to the admins.")
    else:
        bot.reply_to(message, "Please reply to the message of the user you want to report.")

        #See reports
def handle_view_reports(message: Message, db, bot):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "This command can only be used in group chats.")
        return

    if not is_user_admin(bot, message.chat, message.from_user.id):
        bot.reply_to(message, "You need to be an admin to use this command.")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "Please reply to a message to view its reports.")
        return

    reported_user_id = message.reply_to_message.from_user.id
    group_id = message.chat.id  # Get the group ID
    reports_collection = db["reports"]
    user_reports = reports_collection.find({"reported_user_id": reported_user_id, "group_id": group_id})

    user_reports_list = list(user_reports)
    if len(user_reports_list) == 0:
        bot.reply_to(message, "No reports found for this user in this group.")
        return

    report_info = ""
    for report in user_reports_list:
        report_info += (
            f"Report ID: <code>{report['_id']}</code>\n"
            f"Reported By: {report['reporter_user_info']}\n"
            f"Reason: {report['report_text']}\n"
            f"Timestamp: {report['timestamp']}\n\n"
        )

    bot.reply_to(message, f"{report_info}", parse_mode='HTML')
