async def validate(user_date):
    try:
        return int(user_date)
    except:
        if user_date[:4] == "http":
            return user_date[13:]
        else:
            return user_date