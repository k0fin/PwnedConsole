< PwnedConsole >

< About >

	PwnedConsole is a Python script designed to act as an interactive tool for querying HaveIBeenPwned? for breach data through the use of the HaveIBeenPwned? API(v2).
	This script makes use of the PyPwned Python module, which was written to be implemented into Python code to query the HIBP? API.

< Dependencies >

	requests
	pypwned
	textwrap
	ndg-httpsclient
	pyasn1
	pyOpenssl

< Usage >

	Using the script is easy-

		python pwnconsole.py <email_addr/account_name>

	Running this will load the specified account into PwnedConsole, and any options executed wtihin the script will apply to the account specified.
	The user can switch accounts within the script as well, which could be needed when querying the API for data that only applies to a specific type of account.

< ToDo >

	There are a few things I had in mind to improve the functionality of the tool. These things are currently in progress, so don't get butthurt if something doesn't work. :)

