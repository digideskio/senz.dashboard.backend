from leancloud import init, Object, Query
from datetime import datetime, date, timedelta

Log = Object.extend("Log")
UserLocation = Object.extend("UserLocation")

if __name__ == '__main__':
    init(u'9ra69chz8rbbl77mlplnl4l2pxyaclm612khhytztl8b1f9o',
         u'1zohz2ihxp9dhqamhfpeaer8nh1ewqd9uephe9ztvkka544b')
    log_query = Query(Log)
    location_query = Query(UserLocation)

    today = datetime.strptime(date.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
    tommorow = datetime.strptime((date.today() + timedelta(days=1)).strftime('%Y-%m-%d'), '%Y-%m-%d')

    log_query.equal_to('type', 'location')
    log_query.greater_than_or_equal_to("createdAt", today)
    log_query.less_than_or_equal_to("createdAt", tommorow)
    log_count = log_query.count()

    location_query.greater_than_or_equal_to("createdAt", today)
    location_query.less_than_or_equal_to("createdAt", tommorow)
    location_count = location_query.count()

    print "Today's Log of location: ", log_count
    print "Today's Location count: ", location_count
    print "Rate: ", location_count * 1.0 / log_count

