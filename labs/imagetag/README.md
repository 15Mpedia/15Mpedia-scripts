
Steps to run this bot:

# virtualenv -p python3 bot-etiquetas
# cd bot-etiquetas;source bin/activate
# pip install twython
# Create app at https://apps.twitter.com. In the "API keys" tab you will find the API key and the API secret, write both in a file named .twitter_keys with the following structure: API_KEY = xxxxxx (newline) API_SECRET = xxxxxxxxxxxx
# python login.py to generate .twitter_tokens file
# git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git
# cp 15mpedia-family.py core/pywikibot/families (Example here https://github.com/15Mpedia/15Mpedia-scripts/blob/master/15mpedia_family.py)
# cp user-config.py core (Example here https://github.com/15Mpedia/15Mpedia-scripts/blob/master/user-config.py)
# python imagetag.py
# python imagetag-wiki.py
# deactivate
 
You can use cron for periodical executions:

* */15 0,8-23     * * *   cd bot-etiquetas && . bin/activate && python imagetag.py --tweet && deactivate && cd ..
* 0 0-1,9-23      * * *   cd bot-etiquetas && . bin/activate && python imagetag.py --get-replies && deactivate && cd ..
* 5 0-1,9-23      * * *   cd bot-etiquetas && . bin/activate && cd core && python imagetag-wiki.py && deactivate & cd ../..
* 10 21   * * *   cd bot-etiquetas && . bin/activate && python imagetag.py --stats && deactivate && cd ..
