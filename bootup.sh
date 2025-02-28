#!/bin/bash

helm install rabbitmq-app ./helm-rabbitmq-application

helm install rabbitmq-producer ./helm-producer-application
helm install rabbitmq-consumer ./helm-consumer-application