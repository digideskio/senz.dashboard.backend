import leancloud
from random import randrange
from leancloud import Object, Query

query_limit = 100


def get_userid_list():
    query = Query(Object.extend('User'))
    query.not_equal_to('type', 'developer')
    total_count = query.count()
    query_times = (total_count + query_limit - 1) / query_limit
    user_list = []
    for index in range(query_times):
        query.limit(query_limit)
        query.skip(index * query_limit)
        user_list.extend(query.find())

    tracker_id_set = set()
    for user in user_list:
        if user.id not in tracker_id_set:
            tracker_id_set.add(user.id)
    return list(tracker_id_set)


def set_fake_data_to_db(app_id, user_id):
    # gender_list = ['male', 'female', '']
    # age_list = ['16down', '16to35', '35to55', '55up', '']
    event_list = ["contextAtHome", "contextCommutingWork", "contextAtWork", "contextCommutingHome",
                  "contextWorkingInCBD", "contextStudyingInSchool", "contextWorkingInSchool",
                  "contextOutdoorExercise", "contextIndoorExercise", "contextDinningOut", "contextTravelling",
                  "contextShortTrip", "contextInParty", "contextWindowShopping", "contextAtCinema",
                  "contextAtExhibition", "contextAtPopsConcert", "contextAtTheatre", "contextAtClassicsConcert"]
    # consumption_list = ['5000down', '5000to10000', '10000to20000', '20000up']
    # occupation_list = ['official', 'freelancer', 'teacher', 'student', 'supervisor', 'salesman',
    #                  'engineer', 'others', 'soldier', '']
    # field_list = ['infotech', 'law', 'commerce', 'athlete', 'medical', 'human_resource',
    #              'financial', 'architecture', 'humanities', 'natural', 'manufacture',
    #              'agriculture', 'service']
    # sport_list = ['jogging', 'bicycling', 'fitness', 'basketball', 'football', 'table_tennis'
    #              'badminton']
    # hascar_list = ['yes', 'no', '']
    # haspet_list = ['yes', 'no', '']
    marriage_list = ['yes', 'no', '']
    pregnant_list = ['yes', 'no', '']
    # home_offic_status_list = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome', '']
    # interest_list = ["jogging", "fitness", "basketball", "football", "badminton", "bicycling", "table_tennis",
    #                  'social', 'online_shopping', 'offline_shoppng', 'tech_news', 'entertainment_news',
    #                  'current_news', 'business_news', 'sports_news', 'game_news', 'study', 'gamer', 'health',
    #                  'sports_show', 'game_show', 'variety_show', 'tvseries_show', 'acg', 'indoorsman', '']
    dashdatasource = Object.extend('DashDataSource')
    query = Query(dashdatasource)
    query.equal_to('app_id', app_id)
    query.equal_to('user_id', user_id)
    dst_record = query.find()
    if not dst_record:
        dst_record = dashdatasource()
    else:
        dst_record = dst_record[0]

    # content = {}
    # for t in range(24):
    #     status = 'status' + str(t)
    #     content[status] = home_offic_status_list[randrange(0, len(home_offic_status_list))]
    # dst_record.set('home_office_status', content)
    dst_record.set('pregnant', pregnant_list[randrange(0, len(pregnant_list))])
    dst_record.set('marriage', marriage_list[randrange(0, len(marriage_list))])
    # dst_record.set('interest', interest_list[randrange(0, len(interest_list))])
    # dst_record.set('consumption', consumption_list[randrange(0, len(consumption_list))])
    # dst_record.set('field', field_list[randrange(0, len(field_list))])
    # dst_record.set('sport', sport_list[randrange(0, len(sport_list))])
    # dst_record.set('occupation', occupation_list[randrange(0, len(occupation_list))])
    # dst_record.set('has_car', hascar_list[randrange(0, len(hascar_list))])
    # dst_record.set('has_pet', haspet_list[randrange(0, len(haspet_list))])
    # dst_record.set('app_id', app_id)
    # dst_record.set('user_id', user_id)
    # dst_record.set('gender', gender_list[randrange(0, len(gender_list))])
    # dst_record.set('age', age_list[randrange(0, len(age_list))])
    dst_record.set('event', event_list[randrange(0, len(event_list))])
    dst_record.save()
    return True


def get_tracker_of_app(app_id):
        query = Query(Object.extend('Application'))
        query.equal_to('app_id', app_id)
        app_list = query.find()
        if not app_list:
            return []
        the_app = app_list[0]

        query = Query(Object.extend('BindingInstallation'))
        query.equal_to('application', the_app)
        query.select('user')
        installation_list = query.find()
        user_set = set()
        for installation in installation_list:
            user_set.add(installation.attributes['user'].id)
        print list(user_set)

if __name__ == '__main__':
    leancloud.init('z6fhqxvpal43l238q7xzogfdls74my214o5bapm5vkwfn4xh',
                   'rb7jufb22o15nzc9ub5b6b0lx3xt845o2ofz494oc1s9esg8')
    user_list = get_userid_list()
    for item in user_list:
        print(item)
        set_fake_data_to_db('5621fb0f60b27457e863fabb', item)

    # app_id = 'demo55bc5d8e00b0cb9c40dec37b'
    # get_tracker_of_app(app_id)
