## An Arma 3 Steam community recruitment watcher

This program is created to allow automatic watching and posting of new applications on https://steamcommunity.com/app/107410/discussions/21/

### How to use

Using the RecruitmentWatcher is simple.
1. Create a discord webhook on the channel you want new applications to be posted to.
2. Next clone the repository, then open the recruitmentWatcher.py file.
3. Open a Git Bash terminal in the cloned repository directory, then run pip install -r requirements.txt to ensure you have all required libraries
4. You will need to change the value of the url variable to the url of your created webhook.
5. Optionally you can edit the time between checking for new applications by changing the refreshInterval (In Seconds)
6. Lastly run the program, log into steam through the program (Ensure 2FA is enabled) then it will automatically begin posting the newest applications.
