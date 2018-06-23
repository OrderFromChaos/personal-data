# personal-data
Tools to pull your data from tech companies and analyze it

Current analysis code covers:
+ Amazon Purchase History
+ Facebook Messenger History
+ Gmail History
+ Spotify Playlists

Future/partially-written code covers:
+ Google Calendar

### How do I install this? (No programming background)
You'll need Python 3 and a couple libraries. To get Python 3:
1. Go to https://www.python.org/downloads/
2. Click on "Download Python 3.6.5" (or any version with 3.x.x+)
3. Open the downloaded file and follow installation instructions. Be sure to choose "add Python location to PATH" (or a similar sounding checkbox).
4. [Windows] When this is done, open up Powershell (search in the bottom left start bar).
5. Type in "pip install matplotlib BeautifulSoup4". This will install the necessary dependencies.
6. Now that you can run it, download the code from this repository by going to https://github.com/OrderFromChaos/personal-data, clicking "Clone or Download", and clicking "Download ZIP". Unzip the file and put the code somewhere.
7. For each of the analysis codes, you'll need to enter relevant data for your account (so the data analyzer knows how to log in to your account to get the data or where to look for your data dump from eg Facebook). To do this, open up whichever .py file you want to run in Notepad and edit the "Hyperparameters" section at the top. It should look something like this:
![Image](https://i.imgur.com/BEhn1Uo.png)
8. When you're done entering your information into the code, go back to powershell. There's a command called "cd" which allows you to change the "active directory" you're in. We want to use this to navigate to where our code will run. Here are the commands if you left the unzipped folder inside your Downloads folder:
+ cd Downloads
+ cd personal-data
9. Now that you have the correct active directory, type the following command, with the name being correct for whichever piece of code you want to run:
python3 messenger_portable.py
10. You're done!
