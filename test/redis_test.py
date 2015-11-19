_author__ = 'xebin'

#from ..dao import av_dao
import redisco
from redisco import models
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# r = redis.StrictRedis(host='120.27.30.239',port='6379')
# pool = redis.ConnectionPool(host='120.27.30.239', port=6379, db=0)
# r = redis.Redis(connection_pool=pool)
#
redisco.connection_setup(host='127.0.0.1', port=6379, db=10)


class Upoi(models.Model):
    latitude= models.FloatField(required=True)
    longitude= models.FloatField(required=True)
    upoiid=models.Attribute(required=True,unique=True)
    user_id=models.Attribute(required=True)
    cluster_type=models.Attribute(required=True)
    poi_address=models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True)


def insert_upois (userid,upois):
    for upoione in upois:
        upoi=Upoi(latitude=upoione.get('location').latitude,
                        longitude=upoione.get('location').longitude,
                        upoiid=upoione.id,
                        user_id=userid,
                        cluster_type=upoione.get('cluster_type'),
                        poi_address=upoione.get('poi_address')
                        )
        if upoi.is_valid():
            upoi.save()


def get_upois(uid):
    upois=Upoi.objects.filter(user_id=uid)
    return upois
def get_upois_cluster_type(clusterType):
    upois=Upoi.objects.filter(cluster_type=clusterType)
    return upois

def get_upois_By_uid_cluster_type(uid,clusterType):
    upois=Upoi.objects.filter(user_id=uid,cluster_type=clusterType)
    return upois
if __name__=="__main__":
    # from .. import config as conf
  #  import leancloud
 #   leancloud.init('u7jwfvuoi3to87qtkmurvxgjdm5tmzvgpooo0d8wfm0dfdko', 'w6llno78ayu4fewyvgwr6h3v7zjqpz4g262g4htrtvw7jgdg')

    user_id='560388c100b09b53b59504d2'
    ups=get_upois_By_uid_cluster_type(user_id,'density_based') #storm_poi_ba
    for up in ups:
        print 'density size:'+str(len(ups))
        print "upoiid:"+str(up)
        # up.delete()
