# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC #imports and configurations

# COMMAND ----------

import requests
# pprint is used to format the JSON response
from pprint import pprint


# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #Configure connection to Azure Cognitive Services

# COMMAND ----------

import os

key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]


# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #Add languages to the EndPoint

# COMMAND ----------

language_api_url = endpoint + "/text/analytics/v2.1/languages"

print(language_api_url)
print(subscription_key)




# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #Create list with "Documents"

# COMMAND ----------

documents = {"documents": [
    {"id": "1", "text": "This is a document written in English."},
    {"id": "2", "text": "Este es un document escrito en Español."},
    {"id": "3", "text": "这是一个用中文写的文件"},
    {"id": "4", "text": "Dit document is in het Nederlands geschreven."},
    {"id": "5", "text": "C'est nouveau undocument."}
]}

print(documents)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #Call the "Languages" library to send the API request

# COMMAND ----------

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(language_api_url, headers=headers, json=documents)
languages = response.json()
pprint(languages)


# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #Call the "KeyPhrases" library

# COMMAND ----------

language_api_url = endpoint + "/text/analytics/v2.1/keyPhrases"

print(language_api_url)
print(subscription_key)

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(language_api_url, headers=headers, json=documents)
keyPhrases = response.json()
pprint(keyPhrases)


# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #Analyse "Sentiment"

# COMMAND ----------

sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"

documents = {"documents": [
    {"id": "1", "language": "en",
        "text": "I had a wonderful experience! The rooms were wonderful and the staff was helpful."},
    {"id": "2", "language": "en",
        "text": "I had a terrible time at the hotel. The staff was rude and the food was awful."},
    {"id": "3", "language": "es",
        "text": "Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos."},
    {"id": "4", "language": "es",
     "text": "La carretera estaba atascada. Había mucho tráfico el día de ayer."}
]}

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(sentiment_url, headers=headers, json=documents)
sentiments = response.json()
pprint(sentiments)


# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #Identify Entities

# COMMAND ----------

entities_url = endpoint + "/text/analytics/v2.1/entities"

documents = {"documents": [
    {"id": "1", "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800."}
]}

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(entities_url, headers=headers, json=documents)
entities = response.json()
pprint(entities)


# COMMAND ----------

entities_url = endpoint + "/text/analytics/v2.1/entities"

documents = {"documents": [
    {"id": "1", "text": "Egon Consulting is gesticht op 1/5/2011 door Egon Vandenrijdt."}
]}

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(entities_url, headers=headers, json=documents)
entities = response.json()
pprint(entities)
