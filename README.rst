python kafka sample
=====

This is a sample project demonstrating a kafka producer and consumer with python3.

Description
-------------
This has a simple producer that will monitor a website for availability and stream this information
to the consumer via kafka.

Uses Aiven's Postgresql and Kafka databases.

The code can be run in the producer and the consumer modes.

When run in the producer mode, it will check the status of the configured sites and send message to Kafka

Crontab can be used to run the check periodically. Benefits of using crontab:
* No additional process running in the background.
* Less memory usage and issues of memory leaks.

When run in the consumer mode, it will block and listen for messages to process. Once a message is recieved,
it will write the results to a Postgresql database and log the metrics for the site.

The currently reported metrics are the availability, average response time in ms and the down times recorded.


Running the example
=====

Dependencies
-------------
#. Ensure you have python 3.8 installed
#. Needs an Aiven Kafka and Postgresql instance running

Then install dependencies as below
::
  pip install -r requirments.txt

Commands
-------------
This can run in two modes - kafka producer and kafka consumer

#. Download the kafka certificate(ca.pem), service key(service.key) and service certificate(service.cert)
#. Update ``config.py``
#. Update ``kafka_config`` with the server url, the paths to the above files and the topic name on Kafka
#. Update the postgresql database credentials in the ``database_config`` property. This is used by the consumer
#. Update the ``site_config`` list with a list of sites that need to be checked. This is used by the producer

Kafka Producer
^^^^^^^^^^^^^^^^^^^^
To run this as a producer execute
::
  ./app.py --operation check_site

Kafka Consumer
^^^^^^^^^^^^^^^^^^^^
To run this as a consumer execute
::
  ./app.py --operation consume_site

CTRL-C should be used to stop the consumer


References
---------------
#. https://aiven.io/blog/getting-started-with-aiven-kafka
