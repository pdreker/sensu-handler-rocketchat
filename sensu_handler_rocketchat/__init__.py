from sensu_plugin import SensuHandler
import pprint
import urllib2, json, os

ROCKETCHAT_URL = "https://team.proact.de/hooks/iPw6s7YNc72QKCk5e/Xm8MqwrQodKp6rgDbKo5swv4QGYsiiN5ukAGP2bsWCzxHTSK"
NICK = "Sensu"
CHANNEL = "openstack-events"
DASHBOARD_URL = "http://10.43.8.4:3000"

class RocketHandler(SensuHandler):
    def handle(self):
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(self.event)
        #pp.pprint(self.settings)
        #print "Client:         " + self.event["client"]["name"]
        #print "Client Address: " + self.event["client"]["address"]
        #print "Subscriptions:  " + ", ".join(self.event["client"]["subscriptions"])
        #print "Severity:       " + self.translate_status(self.event["check"]["status"])
        #print "Output:         " + self.event["check"]["output"]
        title = "%s (%s): %s" % (self.translate_status(self.event["check"]["status"]),
                                 self.event["check"]["name"],
                                 self.event["client"]["name"])

        thresholds = ""
        for key,value in self.event["check"]["thresholds"].iteritems():
            thresholds = thresholds + "*" + key + "*: " + str(value) + " - "

        text = "%s\n%s" % (self.event["check"]["output"], thresholds)

        self.post_message(title, text, self.status_to_color(self.event["check"]["status"]))

    def post_message(self, title, text, color):
        url = ROCKETCHAT_URL

        data = {}
        data['username'] = NICK
        #data['icon_url'] = icon_url
        data['text'] = ""
        data['channel'] = CHANNEL
        data['attachments'] = []
        attachment = {}
        attachment["title"] = title
        attachment["title_link"] = DASHBOARD_URL
        attachment["text"] = text
        attachment["color"] = color
        data['attachments'].append(attachment)


        req = urllib2.Request(ROCKETCHAT_URL)
        req.add_header('Content-Type', 'application/json')
        payload = json.dumps(data)

        response = urllib2.urlopen(req, payload)
        if response.getcode() is not 200:
        	print "Posting to Mattermost failed!"


    def translate_status(self, status):
        return ["OK", "WARNING", "CRITICAL", "UNKNOWN"][status]

    def status_to_color(self, status):
        return ["#36a64f", "#FFCC00", "#FF0000", "#6600CC"][status]

if __name__ == "__main__":
  f = RocketHandler()