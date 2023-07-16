# SimonIT-Share-Automation
An app that helps automate the recording uploading process for the Simon IT Help Desk

This code takes a list of class recording URL's pasted into the GUI and publishes them according to Simon IT Help Desk formatting
Due to ECHO's built-in share automation, I don't imagine many other people will find a use for this code, but if this is something
that you want to do for your own project, I imagine you could minimally alter the code and still have it work

DO NOT add in extra blank lines between URLs, nor more than 1 blank line after the last URL

config.txt must be formatted correctly and present in the directory the code runs from. See the example config file and the formatting
instructions in the comments at the top of the source code for further detail

## What Will Break This App Now?

  o If the email that a student uses to get into echo is not of the
form ADusername@u.rochester.edu.

  o If two empty lines are in the ‘Start each class recording URL on
a new line’ field after the last URL.

  o If there is an empty line between two URLs in the ‘Start each
class recording URL on a new line’ field.
  
  o If “config.txt” is not formatted correctly. See the
formatting specifications in the comment at the top of the
source code for more specifications

  o If the professor emails in “config.txt” do not appear
EXACTLY (i.e. case-sensitive) as the professor’s email
appears in Echo (see the “Users” tab in Echo)

  o The app will still run and function perfectly even if the
dictionary of classes and professor emails is not
maintained. HOWEVER, if “config.txt” is not longer
maintained, be sure to delete all references to classes and
emails in config.txt in order to avoid conflicts.

  o If the term line in config.txt is not maintained

  o If “config.txt” is not located in the directory from which
the app runs

  o If a class has been recorded in the wrong zoom room (e.g.
CIS414.92 is recorded in CIS404.92’s Personal Zoom Room)

  o Unforeseen oversights.
  
## What Will Break This App in the Future?

  o If Echo changes its web design substantially (beyond cosmetic
changes) it is very likely that this app will no longer work. I
anticipate, however, that we will stop using zoom recordings
before Echo redesigns its website (This turned out to not be true).

  o If the titles of zoom recording pages stop having apostrophes
immediately following the course number.

  o If a course title ever contains a space.
  
  o If the title of the page linked to at echo360.org/home is ever
titled something without ‘o’ as its second character.

  o If echo ever includes ‘`’ in their URLs. This is not a generally
accepted URL character, so I think this is unlikely, but
possible.
