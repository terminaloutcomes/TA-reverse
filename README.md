# TA-reverse

> Archived because it works and I don't want to keep running updates on packages... find me on the splunk usergroup Slack if you want help or find a bug!

Adds a command, `esrever` to Splunk which takes two fields:

* field - the name of a field to reverse
* fields - the names of fields (comma-delimited) to reverse.

It'll also try and JSON-decode _raw and modify things there, so I'm sure that'll trash your SH when you run it. Good luck!
