# FlightFinder-in-python
Created a small script in python to find out cheapest prices at any time
Firstly I appologize for the unclean code.I will be working on it to make it better.
Wrote a script just for myself to keep track of flight prices at different times. The goal was to find a time when flights were cheapest and book them during that time.
It uses Google Flights Rest API to search flights based on their price (first 20 cheapest flights)
then creates a table in HTML and uses that to send and email using SMTP protocol.
To get this working you need to have a key associated with your google APIs account. They will ask for your credit card because they have a tab on the amount of requests each day.
To take care of that I created two keys from my differnt gmail accounts and sent requests to google by loadbalacing the keys.
There is a specific format of Json which needs to be sent which one can see in json1 nested dictionary.

Also you need to enter your email and the email you want to recieve the emails. More imporantly you need to find out your SMTP server.
You don't need to enter your email password(Why? because it is kind of using the insecurity in our email system for a good cause.) 

It also requires installation of following 3rd party python API in your system
--json2html
--html
Their installion is very easily done using pip.
