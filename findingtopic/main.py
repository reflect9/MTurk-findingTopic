import re, json, os, logging, random, string
import webapp2, jinja2
from google.appengine.ext import db
from google.appengine.api import mail, taskqueue
from datetime import datetime
import csv


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

VERSION = 1

modes = ['word list','wordcloud','histogram','topic-in-a-box']
# modes = ['word list','wordcloud','histogram','topic-in-a-box']
# topicWords = [  ['research','information','university','knowledge','address','long','questions','local','important','cultural'],
#             ['development','project','data','provide','high','biology','complex','materials','including','analysis'],
#             ['participants','work','make','hci','field','researchers','students','doctoral','computer ','interaction'],
#             ['individuals','project','cognitive','understanding','social','early','children','provide','studies','individual'],
#             ['war','force','army']
        # ]
# topicFreq = [
#     [10,8,7,5,4,4,3,2,1,1],
#     [9,7,7,5,5,3,3,2,2,1],
#     [10,7,4,4,4,3,3,1,1,1],
#     [10,9,9,9,9,9,2,1,1,1],
#     [10,10,10,8,6,4,3,2,1,1]
# ]
# topicBoxes = ['topic-in-a-box-1.png','topic-in-a-box-2.png','topic-in-a-box-3.png','topic-in-a-box-4.png','topic-in-a-box-5.png'] 
file_topicJSON = open("dataset/nyt-50-topics.json","r")
topicJSON = json.loads(file_topicJSON.read())




class TopicEvaluation(db.Model):
    nickname = db.StringProperty()
    answers = db.TextProperty()


class LabelingHit(db.Model):
    usercode = db.StringProperty()
    mode = db.StringProperty()
    randomImage_idx = db.IntegerProperty()
    wordNum = db.IntegerProperty()
    answers = db.TextProperty()
    timestamp = db.TextProperty()
    version = db.IntegerProperty()

    # timestamp_start = db.DateTimeProperty(auto_now_add=False)
    # timestamp_end = db.DateTimeProperty(auto_now_add=False)
    # due_date = db.DateTimeProperty()


########################################################################################
########################################################################################
########################################################################################
########################################################################################

class SubmitHandler(webapp2.RequestHandler):
    def post(self):
        #item = self.request.get("item")
        #nextURL = "task"
        result = LabelingHit()
        result.mode = self.request.get('mode')
        result.randomImage_idx = int(self.request.get('randomImage_idx'))
        result.wordNum = int(self.request.get('wordNum'))
        result.usercode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        result.answers = self.request.get('answers')
        result.timestamp = self.request.get('timestamp')
        result.version = VERSION
        result.put()

        self.response.out.write("<div class='endMessage'>Thank you for your participation. Your survey code is <b style='color:red;'>"+result.usercode+"</b><br> Do not forget to copy and paste the code in the Amazon Mechanical Turk page.</div>");
        

class TaskHandler(webapp2.RequestHandler):
    def get(self):
        mode = random.choice(modes)
        wordNum = random.choice([5,10,20])
        sample_idx = random.sample(range(len(topicJSON['topics'])),5)
        randomImage_idx = random.choice([1,2,3,4,5]) 
        topics = {}
        for idx in sample_idx:
            topics[str(idx)]=topicJSON['topics'][idx]
        # topicsJSON = json.dumps(topics)
        # for topic in topics:
        #     freq_all = map(lambda x: x['second'], topic['terms'])
        #     topic['freq_max']= max(freq_all)
        #     for term in topic['terms']:
        #         term['freq_normalized'] = term['second']/topic['freq_max']

        template_values = {'topics':topics, 'mode':mode, 'wordNum':wordNum, 'randomImage_idx':randomImage_idx}
        template = JINJA_ENVIRONMENT.get_template('task.html')
        html = template.render(template_values)
        self.response.out.write(html)

class ReportHandler(webapp2.RequestHandler):
    def get(self):
        file_topicJSON_old = open("dataset/nyt-50-topics-without stopiwords.json","r")
        topicJSON_old = json.loads(file_topicJSON_old.read())
        query = db.GqlQuery("SELECT * FROM LabelingHit LIMIT 1000")
        hits = []
        for r in query.run():
            r.ansList = json.loads(r.answers)
            # r.ansTogether = []
            # for i in range(len(r.ansList)/2):
            #     r.ansTogether.append([r.ansList[i*2],r.ansList[i*2+1]])
            # print r.ansList
            # r.shortAnsList = ansList[0::2]
            # r.longAnsList = ansList[1::2]
            hits.append(r)
        template_values = {'hits':hits, 'topicWords':topicJSON['topics'], 'topicWordsOld':topicJSON_old['topics']}
        template = JINJA_ENVIRONMENT.get_template('report.html')
        html = template.render(template_values)
        self.response.out.write(html)

class ReportCSVHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/csv'
        writer = csv.writer(self.response.out, delimiter='|')
        query = db.GqlQuery("SELECT * FROM LabelingHit LIMIT 1000")
        writer.writerow(['usercode','mode','topicIdx','wordNum','short','long','confidence'])
        for r in query.run():
            r.ansList = json.loads(r.answers)
            for ans in r.ansList:
                if ans.has_key('topicIndex'):
                    tIdx = ans['topicIndex']
                else:
                    tIdx = "unknown"
                writer.writerow([r.usercode, r.mode, tIdx, r.wordNum, ans['short'], ans['long'], ans['conf']])
                #answers += r.usercode+"\t"+r.mode+"\t"+str(ans['topicIndex'])+"\t"+str(r.wordNum)+"\t"+ans['short']+"\t"+ans['long']+"\t"+ans['conf']+"\n"
        # self.response.out.write(answers)

class AllTasksHandler(webapp2.RequestHandler):
    def get(self):
        # show all tasks in one page
        topics = topicJSON['topics']
        for topic in topics:
            freq_all = map(lambda x: x['second'], topic['terms'])
            topic['freq_max']= max(freq_all)
            for term in topic['terms']:
                term['freq_normalized'] = term['second']/topic['freq_max']
        # print topics[0]
        template_values = {'topics':topics}
        template = JINJA_ENVIRONMENT.get_template('alltasks.html')
        html = template.render(template_values)
        self.response.out.write(html)

    # usercode = db.StringProperty()
    # mode = db.StringProperty()
    # answers = db.TextProperty()

    # timestamp = db.TextProperty()
# class SubmitAllTasksHandler(webapp2.RequestHandler):
#     def get(self):
#         eval = TopicEvaluation()
#         eval.nickname = self.request.get('nickname')
#         eval.answers = self.request.get("answers")
#         eval.put()
#         self.response.out.write("<p>Thanks! Your evaluation is submitted.</p>");


# class SendReminderHandler(webapp2.RequestHandler):
#     def get(self):
#         _id = int(self.request.get("id"))
#         todo = Log.get_by_id(_id)
#         if todo is not None and todo.completed is False:
#             html = "You have a uncompleted Log : "+todo.txt+" ["+str(_id)+"] "+str(todo.due_date)
#             msg = mail.EmailMessage()
#             msg.sender = owner_email
#             msg.subject = "Log: " + todo.txt
#             msg.to = owner_email
#             msg.html = html
#             msg.send()


app = webapp2.WSGIApplication([
    ('/', TaskHandler),
    ('/task', TaskHandler),
    ('/submit', SubmitHandler),
    ('/report', ReportHandler),
    ('/alltasks', AllTasksHandler),
    ('/reportcsv', ReportCSVHandler)
    # ('/submit_alltasks', SubmitAllTasksHandler),
    # ('/sendReminder', SendReminderHandler)
], debug=True)
