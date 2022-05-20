
"""
    Final AWS Lambda function skeleton. 
    
    Author: Explore Data Science Academy.
    
    Note:
    ---------------------------------------------------------------------
    The contents of this file should be added to a AWS  Lambda function 
    created as part of the EDSA Cloud-Computing Predict. 
    For further guidance around this process, see the README instruction 
    file which sits at the root of this repo.
    ---------------------------------------------------------------------

"""

# Lambda dependencies
import boto3    # Python AWS SDK
import json     # Used for handling API-based data.
import base64   # Needed to decode the incoming POST data
import numpy as np # Array manipulation
# <<< You will need to add additional libraries to complete this script >>> 

# ** Insert key phrases function **
# --- Insert your code here ---

# -----------------------------

# ** Insert sentiment extraction function **
# --- Insert your code here ---
 
# -----------------------------

# ** Insert email responses function **
# --- Insert your code here ---
 
# -----------------------------

# Lambda function orchestrating the entire predict logic
def lambda_handler(event, context):
    
    # Perform JSON data decoding 
    body_enc = event['body']
    dec_dict = json.loads(base64.b64decode(body_enc))
    

    # ** Insert code to write to dynamodb **
    # <<< Ensure that the DynamoDB write response object is saved 
    #    as the variable `db_response` >>> 
    # --- Insert your code here ---


    # Do not change the name of this variable
    db_response = None
    # -----------------------------
    

    # --- Amazon Comprehend ---
    comprehend = boto3.client(service_name='comprehend')
    
    #From json string generate our sentiment dictionary
    sentiment_string = json.dumps(comprehend.detect_sentiment(Text=dec_dict['message'], LanguageCode='en'), sort_keys=True, indent=4)
    sentiment_dictionary = json.loads(sentiment_string)
    
    #Call our 'find_max_sentiment()' function
    #find_max_sentiment(sentiment_dictionary)
    
    
    #From json string generate our key phrase dictionary
    key_phrase_string = json.dumps(comprehend.detect_key_phrases(Text=dec_dict['message'], LanguageCode='en'), sort_keys=True, indent=4)
    key_phrase_dictionary = json.loads(key_phrase_string)
    
    #Call our 'key_phrase_finder()' function passing the appropriate parameters. Save in 'phrases' variable (returned as a tuple)
    phrases = key_phrase_finder(important_words, key_phrase_dictionary)[0]
    print(phrases)
    
    enquiry_text = None # <--- Insert code to place the website message into this variable
    # -----------------------------
    
    # --- Insert your code here ---
    sentiment = None # <---Insert code to get the sentiment with AWS comprehend
    # -----------------------------
    
    # --- Insert your code here ---
    key_phrases = None # <--- Insert code to get the key phrases with AWS comprehend
    # -----------------------------
    
    # Get list of phrases in numpy array
    phrase = []
    for i in range(0, len(key_phrases['KeyPhrases'])-1):
        phrase = np.append(phrase, key_phrases['KeyPhrases'][i]['Text'])


    # ** Use the `email_response` function to generate the text for your email response **
    # <<< Ensure that the response text is stored in the variable `email_text` >>> 
    # --- Insert your code here ---
    # Do not change the name of this variable
    email_text = None 

    
    # -----------------------------
            

    # ** SES Functionality **

    # Insert code to send an email, using AWS SES, with the above defined 
    # `email_text` variable as it's body.
    # <<< Ensure that the SES service response is stored in the variable `ses_response` >>> 
   SENDER = 'vincechinedu392@gmail.com'
    RECIPIENT = dec_dict['email']
    SUBJECT = f"Data Science Portfolio Project Website - Hello {dec_dict['name']}"
    BODY_TEXT = (email_text)
    CHARSET = "UTF-8"
    client = boto3.client('ses')
     # Try to send the email.
    try:
        #Provide the contents of the email.
        ses_response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                    'edsa.predicts@explore-ai.net', # <--- Uncomment this line once you have successfully tested your predict end-to-end
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(ses_response['MessageId'])

    # Do not change the name of this variable
    ses_response = None
    
    # ...

    # Do not modify the email subject line
    SUBJECT = f"Data Science Portfolio Project Website - Hello {dec_dict['name']}"

    # -----------------------------


    # ** Create a response object to inform the website that the 
    #    workflow executed successfully. Note that this object is 
    #    used during predict marking and should not be modified.**
    # --- DO NOT MODIFY THIS CODE ---
    lambda_response = {
        'statusCode': 200,
        'body': json.dumps({
        'Name': dec_dict['name'],
        'Email': dec_dict['email'],
        'Cell': dec_dict['phone'], 
        'Message': dec_dict['message'],
        'DB_response': db_response,
        'SES_response': ses_response,
        'Email_message': email_text
        })
    }
    # -----------------------------
    
    return lambda_response   
    




