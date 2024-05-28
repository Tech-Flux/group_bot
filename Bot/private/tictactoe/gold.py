# gold_manager.py
def get_user_gold(user_id, db):
    user = db['users'].find_one({'user_id': user_id})
    if user:
        return user.get('gold', 0)
    else:
        return 0

def add_user_gold(user_id, amount, db):
    db['users'].update_one(
        {'user_id': user_id},
        {'$inc': {'gold': amount}},
        upsert=True
    )

def set_user_gold(user_id, amount, db):
    db['users'].update_one(
        {'user_id': user_id},
        {'$set': {'gold': amount}},
        upsert=True
    )
