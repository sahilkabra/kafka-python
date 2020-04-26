kafka_config = {
    "uri": "kafka-kafkapython-sample-sahil-97de.aivencloud.com:16096",
    "ca_path": ".env/ca.pem",
    "cert_path": ".env/service.cert",
    "access_key": ".env/service.key",
    "topic": "sample-topic",
}

sites_config = [{
    "name": "google",
    "url": "https://google.com.au",
    "regex": "Google"
}, {
    "name": "pm",
    "url": "https://simple-portfolio-manager.herokuapp.com/",
    "regex": "hello"
}, {
    "name": "notexist",
    "url": "http://somenonexistentsite",
    "regex": ""
}]

database_config = {
    "host": "pg-kafkapython-sample-sahil-97de.aivencloud.com",
    "port": "16094",
    "database": "defaultdb",
    "user": "",
    "password": "",
    "cert_path": ".env/postgresql.pem"
}
