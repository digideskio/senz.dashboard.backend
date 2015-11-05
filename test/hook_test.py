from leancloud import Object, Query, init

if __name__ == '__main__':
    init('pin72fr1iaxb7sus6newp250a4pl2n5i36032ubrck4bej81',
         'qs4o5iiywp86eznvok4tmhul360jczk7y67qj0ywbcq35iia')

    event_table = Object.extend('UserEvent')
    query = Query(event_table)
    result_list = query.find()
    event_obj = result_list[0]

    event = event_table()
    event.set('user', event_obj.get('user'))
    event.set('event', event_obj.get('event'))
    event.set('startTime', event_obj.get('startTime'))
    event.set('endTime', event_obj.get('endTime'))
    event.save()
