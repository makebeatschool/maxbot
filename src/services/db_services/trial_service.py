from db.repos.trial_repo import upsert_trial_reminder, delete_trial_reminder, get_all_trial_reminders


async def write_trial_time( user_id, send_time ):
    await upsert_trial_reminder(user_id, send_time)
    return True

async def get_all_trials():
    await get_all_trial_reminders()
    return True

async def delete_trial_for_user(user_id):
    await delete_trial_reminder(user_id)
    return True