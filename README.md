# Crime Alert System

The project is live on : https://crimealert-531.web.app  
Link to the YT video: https://www.youtube.com/watch?v=ehEc1Knc9nY&t=4s  



## IMPORTANT PREREQUISITES

1. To download cookies, use the `get cookies.txt` extenstion on Chrome (https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid) and download using the same account with which you are signed into in Chrome. Make sure to rename the downloaded file as `cookies.txt`  


2. Make sure that the account that you will use to create those cookies do have people sharing their location on it (in Google Maps), otherwise the app will return empty results. 

## INSTRUCTIONS TO RUN THE APP ON LOCALHOST
1. Clone the project
2. To start the Fuseki server, create a folder rdf_files and place an empty file by the name of crimeLocation.rdf. Then run the following command in the root directory 

    ` ./fuseki_server/fuseki-server --update --file= ./rdf_files/crimeLocation.rdf /ds`

3. cd into backend folder, install all the libraries for python as stated in file requirements.txt. 

    `pip install -r requirements.txt`

4. start the backend server using command 

    `python server.py` 

5. Then in new terminal cd into front-end

6. Run command 

    `yarn install`

7. and then

    `yarn start`

8. Open url for front end in Browser and enter email and cookie.txt file and click on Register.


Front end template from: https://github.com/rajshekhar26/cleanfolio



# Real-time-crime-alert-system
