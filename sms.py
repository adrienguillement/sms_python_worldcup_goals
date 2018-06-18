import urllib, json
import datetime
import os.path
from jsondiff import diff
from twilio.rest import Client

account_sid = ''
auth_token = ''

myPhone = '+'
TwilioNumber = '+'

now = datetime.datetime.now()
url = "http://worldcup.sfg.io/matches/country?fifa_code=ENG"
response = urllib.urlopen(url)
data = json.loads(response.read())

if os.path.isfile('data.txt'):
  with open('data.txt') as json_file:  
      data_old = json.load(json_file)

  with open('data.txt', 'w') as outfile:
      json.dump(data, outfile)

  for i in range(0, len(data_old)):
    if data_old[i]["datetime"].split("T")[0] == now.strftime("%Y-%m-%d"):
      today_id = i

  try:
    if diff(data_old, data):
      domicile = data_old[today_id]["home_team"]["country"]
      exterieur = data_old[today_id]["away_team"]["country"]

      domicile_goals = []
      for each in data_old[today_id]["home_team_events"]:
        if "goal" in each["type_of_event"]:
          del each["id"]
          del each["type_of_event"]
          domicile_goals.append(each)
      
      exterieur_goals = []
      for each in data_old[today_id]["away_team_events"]:
        if "goal" in each["type_of_event"]:
          del each["id"]
          del each["type_of_event"]
          exterieur_goals.append(each)

      domicile_detail = ""
      for each in domicile_goals:
        domicile_detail += " ".join(each.values()) + "\n"

      exterieur_detail = ""
      for each in exterieur_goals:
        exterieur_detail += " ".join(each.values()) + "\n"

      #ENVOI DU SMS
      client = Client(account_sid, auth_token)

      client.messages.create(
        to=myPhone,
        from_=TwilioNumber,
        body="\n{domicile} {domicile_score}-{exterieur_score} {exterieur} \n {domicile} : \n {domicile_detail} \n \n {exterieur} : \n {exterieur_detail}".format(domicile=domicile,
                                                                                                                                                              exterieur=exterieur,
                                                                                                                                                              domicile_score=len(domicile_goals),
                                                                                                                                                              exterieur_score=len(exterieur_goals),
                                                                                                                                                              domicile_detail=domicile_detail,
                                                                                                                                                              exterieur_detail=exterieur_detail) + u'\U0001f680')
  except Exception as e:
    print e

else:
  with open('data.txt', 'w') as outfile:
      json.dump(data, outfile)
