from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import pandas as pd
import csv
import numpy as np
from locationsharinglib import Service
import smtplib

app = Flask(__name__)
useremail = "noreply.ser531@gmail.com"

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_the_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      email = request.form.get('email')
    #   useremail = email
      setup_and_generate_rdf(email=email)
      data = open("rdf_files/crimeLocation.rdf").read()
      headers = {'Content-Type' : 'application/rdf+xml'}
      r = requests.put('http://18.144.65.192:3030/ds/data', data = data , headers = headers )
    #   print(email)
      return main(email=email)


@app.route('/', methods = ['GET'])
def main(email = useremail):
    
    data = {
        'query': open('query/query.rq').read(),
    }

    response = requests.post('http://18.144.65.192:3030/ds/query', data=data)

    res = response.json()
    # print(res.text)
    bindings = res['results']['bindings']
    if len(bindings) > 0:
        bindings = bindings[0]
        friendName = bindings['friendName']['value']
        crimeLocName = bindings['crimeLocName']['value']
        friendLocName = bindings['friendLocName']['value']
        crimeName = bindings['crimeName']['value']
        body = f"A crime: {crimeName}  has occured at {crimeLocName}  and your friend : {friendName} might be in danger as they are currently at {friendLocName}, which is less than 2 KM away from {crimeLocName}"
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
            email_address = 'noreply.ser531@gmail.com'
            email_password = 'vdcghwnhgdhqliqj'
            connection.login(email_address, email_password )
            connection.sendmail(from_addr=email_address,
                                to_addrs=email,
            msg="subject:INCIDENT ALERT \n\n " + body)
        # print(email, body)


    return response.json()


def setup_and_generate_rdf(email, first = False):
    ########################FRIEND CSV GENERATION LOGIC##################################
    cookies_file = "cookies.txt"
    google_email = email
    # if first:
    #     cookies_file = "cookies/cookies.txt"
    #     email = "noreply.ser531@gmail.com"
    # # print('ljdlskjfd')

    service = Service(cookies_file=cookies_file, authenticating_account=google_email)

    people = []

    for person in service.get_shared_people():
        people.append(
            [person._full_name, person._latitude, person._longitude, person._address]
        )

    tempArray = np.array(people)

    dfFriends = pd.DataFrame(tempArray)

    dfFriends.to_csv("friendsLocation.csv", index=False)


    ########################LOCATION CSV GENERATION LOGIC##################################
    url = "https://data.montgomerycountymd.gov/resource/98cc-bc7d.json"
    headers = ["priority", "latitude", "longitude", "start_time", "initial_type", "address"]

    df = pd.read_json(url).iloc[:5]

    df.to_csv("crimeLocation.csv", columns=headers, index=False)

    ########################LOCATION RDF GENERATION#########################################
    rdf = open("rdf_files/crimeLocation.rdf", "w")
    try:

        rdf.write('<?xml version="1.0"?>\n')
        rdf.write("<!DOCTYPE rdf:RDF [\n")
        rdf.write('	<!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >\n')
        rdf.write('	<!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >\n')
        rdf.write('	<!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >\n')
        rdf.write('	<!ENTITY ca "http://www.semanticweb.org/crimeAlertSystem#" >\n')
        rdf.write("]>\n")
        rdf.write("<rdf:RDF\n")
        rdf.write('	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" \n')
        rdf.write('	xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" \n')
        rdf.write('	xmlns:xsd="http://www.w3.org/2001/XMLSchema#" \n')
        rdf.write('	xmlns:ca="http://www.semanticweb.org/crimeAlertSystem#">\n\n')

        with open("crimeLocation.csv", "r") as f:

            reader = csv.reader(f)
            x = 1
            for col in reader:
                if col[0] != "priority":
                    rdf.write('	<rdf:Description rdf:ID="&ca;Crime' + str(x) + '">\n')
                    rdf.write('	    <rdf:type rdf:resource="&ca;Crime"/>\n')
                    rdf.write(
                        '		<ca:hasPriority rdf:datatype="&rdfs;Literal">'
                        + col[0]
                        + "</ca:hasPriority>\n"
                    )
                    rdf.write(f'	 <ca:hasCrimeLocation rdf:resource="&ca;Location{x}" />\n')
                    rdf.write(
                        '		<ca:hasDateTime rdf:datatype="&rdfs;Literal">'
                        + col[3]
                        + "</ca:hasDateTime>\n"
                    )
                    rdf.write(
                        '		<ca:hasAlertName rdf:datatype="&rdfs;Literal">'
                        + col[4]
                        + "</ca:hasAlertName>\n"
                    )
                    rdf.write('	    <ca:notifies rdf:resource="&ca;Self"/>\n')
                    rdf.write("	</rdf:Description>\n\n")

                    rdf.write('	<rdf:Description rdf:ID="&ca;Location' + str(x) + '">\n')
                    rdf.write('	    <rdf:type rdf:resource="&ca;Location"/>\n')
                    rdf.write(
                        '		<ca:hasLatitude rdf:datatype="&xsd;float">'
                        + col[1]
                        + "</ca:hasLatitude>\n"
                    )
                    rdf.write(
                        '		<ca:hasLongitude rdf:datatype="&xsd;float">'
                        + col[2]
                        + "</ca:hasLongitude>\n"
                    )
                    rdf.write(
                        '		<ca:hasLocationName rdf:datatype="&rdfs;Literal">'
                        + col[5]
                        + "</ca:hasLocationName>\n"
                    )
                    rdf.write("	</rdf:Description>\n\n")
                    x = x + 1

        ########################FRIENDS RDF GENERATION#########################################

        with open("friendsLocation.csv", "r") as f:

            reader = csv.reader(f)
            y = 1
            for col in reader:
                if col[0] != "0":
                    rdf.write('	<rdf:Description rdf:ID="&ca;Friend' + str(y) + '">\n')
                    rdf.write('	    <rdf:type rdf:resource="&ca;Friend"/>\n')
                    rdf.write(
                        '		<ca:hasName rdf:datatype="&rdfs;Literal">'
                        + col[0]
                        + "</ca:hasName>\n"
                    )
                    rdf.write(f'     <ca:hasLocation rdf:resource="&ca;Location{x}" />\n')
                    rdf.write("	</rdf:Description>\n\n")

                    rdf.write('	<rdf:Description rdf:ID="&ca;Location' + str(x) + '">\n')
                    rdf.write('	    <rdf:type rdf:resource="&ca;Location"/>\n')
                    rdf.write(
                        '		<ca:hasLatitude rdf:datatype="&xsd;float">'
                        + col[1]
                        + "</ca:hasLatitude>\n"
                    )
                    rdf.write(
                        '		<ca:hasLongitude rdf:datatype="&xsd;float">'
                        + col[2]
                        + "</ca:hasLongitude>\n"
                    )
                    rdf.write(
                        '		<ca:hasLocationName rdf:datatype="&rdfs;Literal">'
                        + col[3]
                        + "</ca:hasLocationName>\n"
                    )
                    rdf.write("	</rdf:Description>\n\n")
                    x = x + 1
                    y = y + 1

        rdf.write('	<rdf:Description rdf:ID="&ca;Self1' + '">\n')
        rdf.write('     <rdf:type rdf:resource="&ca;Self"/>\n')
        rdf.write(
            '		<ca:hasName rdf:datatype="&rdfs;Literal">' + google_email + "</ca:hasName>\n"
        )
        for k in range(1, y):
            rdf.write(f'     <ca:hasFriend rdf:resource="&ca;Friend{k}"/>\n')
        rdf.write("	</rdf:Description>\n\n")

        rdf.write("</rdf:RDF>")

    finally:
        rdf.close()


### cookie code ### - from ish
setup_and_generate_rdf(email=useremail, first=True)

### friends rdf generated ###
data = open("./rdf_files/crimeLocation.rdf").read()
headers = {'Content-Type' : 'application/rdf+xml'}
# r = requests.put('http://localhost:3030/ds/data', data = data , headers = headers )
r = requests.put('http://18.144.65.192:3030/ds/data', data = data , headers = headers )

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
    