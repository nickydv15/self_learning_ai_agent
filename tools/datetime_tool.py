# ==============================
# DATE & TIME TOOL
# ==============================

from datetime import datetime


# ==============================
# CURRENT DATE
# ==============================

def get_current_date():

    now = datetime.now()

    return now.strftime("%d %B %Y")


# ==============================
# CURRENT TIME
# ==============================

def get_current_time():

    now = datetime.now()

    return now.strftime("%I:%M:%S %p")