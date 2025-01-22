from apscheduler.schedulers.background import BackgroundScheduler

from llm.chat_history import get_all_session_histories, remove_session_history

scheduler = BackgroundScheduler()


def cleanup_old_sessions():
    to_remove = []
    for session_id, chat_history in get_all_session_histories():
        if chat_history.is_outdated_hours(12):
            to_remove.append(session_id)

    for session_id in to_remove:
        remove_session_history(session_id)


scheduler.add_job(cleanup_old_sessions, "interval", hours=1)
