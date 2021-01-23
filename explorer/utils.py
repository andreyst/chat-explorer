from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

def fill_sparse_stats(sparse_stats):
  if len(sparse_stats) == 0:
    return []

  stats = []
  date_cursor = None

  fill_roles = set([0, 1, 2])
  for entry in sparse_stats:
    date = datetime.strptime(entry[1], "%Y-%m-%d")

    if date_cursor is None:
      date_cursor = date

    while date_cursor < date:
      for fill_role in fill_roles:
        stats.append( (fill_role, date_cursor.strftime("%Y-%m-%d"), 0, 0) )
      date_cursor += timedelta(days=1)
      fill_roles = set([0, 1, 2])

    fill_roles.remove(entry[0])
    stats.append(entry)

  for fill_role in fill_roles:
    stats.append( (fill_role, date_cursor.strftime("%Y-%m-%d"), 0, 0) )
  date_cursor += timedelta(days=1)

  today = datetime.now()
  while date_cursor <= today:
    for fill_role in [0, 1, 2]:
      stats.append( (fill_role, date_cursor.strftime("%Y-%m-%d"), 0, 0) )
    date_cursor += timedelta(days=1)

  return stats

def generate_dates(start_date, group):
  date = start_date
  res = []
  delta = None
  format_string = ""

  if group == "d":
    delta = timedelta(days=1)
    format_string = "%Y-%m-%d"
  elif group == "w":
    delta = timedelta(weeks=1)
    format_string = "%Y-%W"
  elif group == "m":
    delta = relativedelta(months=1)
    format_string = "%Y-%m"
  else:
    raise RuntimeError("Unsupported group value")

  now = datetime.now(pytz.utc)
  while date <= now:
    res.append(date.strftime(format_string))
    date += delta

  return res