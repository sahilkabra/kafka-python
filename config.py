kafkaConfig = {
    "uri": "kafka-kafkapython-sample-sahil-97de.aivencloud.com:16096",
    "ca_path": ".env/ca.pem",
    "cert_path": ".env/service.cert",
    "access_key": ".env/service.key",
    "topic": "sample-topic",
}

sitesConfig = [{
    "url": "https://google.com.au",
    "regex": "Google"
}, {
    "url": "https://simple-portfolio-manager.herokuapp.com/",
    "regex": "hello"
}, {
    "url": "http://somenonexistentsite",
    "regex": ""
}]
