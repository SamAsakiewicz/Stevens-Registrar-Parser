import Parser
import Datastore
import webapp2
import script
import datetime

class DatastoreUpdate(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('starting parse')
        
        day = datetime.datetime.today().weekday()
        if (day == 2) or (day == 4):
            script.update_current_semester()
            script.update_current_year()
        if day == 3:
            try:
                Datastore.delete_aggr()
            except:
                pass
            script.update_aggregates(1)
        if day == 5:
            script.update_aggregates(2)
        
application = webapp2.WSGIApplication([
    ('/scripts/update', DatastoreUpdate),
], debug=True)
        




