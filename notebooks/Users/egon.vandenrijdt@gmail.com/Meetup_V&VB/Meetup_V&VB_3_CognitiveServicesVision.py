# Databricks notebook source
import requests
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO

# COMMAND ----------

# Add your Computer Vision subscription key and endpoint to your environment variables.
import os

if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "/vision/v2.0/analyze"

# Set image_path to the local path of an image that you want to analyze.
#image_path = "dbfs:/mnt/upload/Images/Small_Joke.JPG"
#image_path = "file:/databricks/driver/Small_Joke.JPG"
image_path = "Small_Joke.JPG"


# COMMAND ----------

#dbutils.fs.ls("dbfs:/mnt/upload/Images")
dbutils.fs.cp("dbfs:/mnt/upload/Images/Small_Joke.JPG", "file:/databricks/driver/Small_Joke.JPG")

dbutils.fs.ls("file:/databricks/driver")


# COMMAND ----------

image_data = open(image_path, "rb").read()
# Read the image into a byte array
image_data = open(image_path, "rb").read()
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
params = {'visualFeatures': 'Categories,Description,Color'}
response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
response.raise_for_status()


# COMMAND ----------

# MAGIC %md
# MAGIC #Analyse the image

# COMMAND ----------

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.

analysis = response.json()
print(analysis)
image_caption = analysis["description"]["captions"][0]["text"].capitalize()


# COMMAND ----------


# Display the image and overlay it with the caption.
image = Image.open(BytesIO(image_data))
plt.imshow(image)
plt.axis("off")
_ = plt.title(image, size="x-large", y=-0.1)

plt.show()
display()

#display(plt.imshow(image))

# COMMAND ----------

# MAGIC %md
# MAGIC #Extract text from Image

# COMMAND ----------

import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

text_recognition_url = endpoint + "/vision/v2.0/read/core/asyncBatchAnalyze"

print(subscription_key)
print(endpoint)
print(text_recognition_url)


# COMMAND ----------

# Set image_url to the URL of an image that you want to analyze.
image_url = "https://upload.wikimedia.org/wikipedia/commons/d/dd/Cursive_Writing_on_Notebook_paper.jpg"

#headers = {'Ocp-Apim-Subscription-Key': subscription_key}
#data = {'url': image_url}
data = open(image_path, "rb").read()

headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
params = {'visualFeatures': 'Categories,Description,Color'}
response = requests.post(
    text_recognition_url, headers=headers, params=params, data=data)
response.raise_for_status()

#------------
'''response = requests.post(
    text_recognition_url, headers=headers, json=data)
response.raise_for_status()
'''


# COMMAND ----------

# MAGIC %md
# MAGIC #OCR

# COMMAND ----------

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

ocr_url = endpoint + "/vision/v2.0/ocr"


# COMMAND ----------

# MAGIC %md
# MAGIC #From URL

# COMMAND ----------

# Set image_url to the URL of an image that you want to analyze.

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/" + \
    "Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png"

#https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png

#image_url = "https://upload.wikimedia.org/wikipedia/commons/d/dd/Cursive_Writing_on_Notebook_paper.jpg"
  
headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {'language': 'unk', 'detectOrientation': 'true'}
data = {'url': image_url}
response = requests.post(ocr_url, headers=headers, params=params, json=data)
response.raise_for_status()

analysis = response.json()

print(analysis)


# COMMAND ----------

import json

json.dumps(analysis, indent=4)

with open('analysis.json', 'w') as json_file:
  json.dump(analysis, json_file)
  


# COMMAND ----------

dbutils.fs.ls("file:/databricks/driver")

#dbutils.fs.rm("file:/databricks/driver/croduct.json")

dbutils.fs.cp("file:/databricks/driver/analysis.json", "dbfs:/mnt/upload/analysis.json")

# COMMAND ----------

df = spark.read.format("json").option("inferSchema", "true").option("multiline", "true").option("header","true").load("dbfs:/mnt/upload/analysis.json")

display(df)

# COMMAND ----------

dfTextDetail = df.select("language","orientation","regions")

display(dfTextDetail)


# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

dfRegions = dfTextDetail.select(explode("regions").alias("regions"))
display(dfRegions)


# COMMAND ----------

dfWords = dfRegions.select(explode("regions.lines.words").alias("words"))
display(dfLines)


# COMMAND ----------

dfText = dfWords.select("words.text")
display(dfText)


# COMMAND ----------

# MAGIC %md
# MAGIC #From local path

# COMMAND ----------

#image_path = "<path-to-local-image-file>"
image_path = "Small_Joke.JPG"

# Read the image into a byte array
image_data = open(image_path, "rb").read()
# Set Content-Type to octet-stream
headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}


#print(ocr_url)
#print(headers)
#print(image_data)

# put the byte array into your post request
response = requests.post(ocr_url, headers=headers, params=params, data = image_data)

ocr_analysis = response.json()

print(ocr_analysis)

