The "Shelterstatus.py" can be run on a server to process info updates from twitter and update it into an Amazon AWS RDS database everyhour. Withou some validation and error checking, it is able to process and update tweets satisfying certain format requirments.

#Sample msg format
column name: latitude, 	Longitude,	shelter info,	food info,	msid,	                 lan class,	    weather

sample msg:  40.8072,    -73.9488,   yes,   	       yes, 	    720970246908219000.00,	eng wed 3pm, 	rainy



It also checks for the total amount of tweet updates received everyday(rate) and a warnning would be produced if there's too few tweet updates on shelter status by the end of each day.

The shelter status data in the database will be later used for visualiztion on the website to provide homeless people latest shelter statuses in NYC

