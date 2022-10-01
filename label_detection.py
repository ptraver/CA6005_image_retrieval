#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from json import dump, load
from os import getcwd, listdir

with open('text_surrogate.json') as json_file:
   txt_surrogates = load(json_file)

path = getcwd() + '/eligible_imgs/'
fls = listdir(path)
fls.remove('.DS_Store')

# add a labels key to every dict
for key in txt_surrogates:
    txt_surrogates[key]['labels'] = ''

def detect_labels(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MinConfidence=75)

    lbls = []

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'Received labels for {photo}')

        print()   
        for label in response['Labels']:
            lbls.append(label['Name'])
            print ("Label: " + label['Name'])
            print ("Confidence: " + str(label['Confidence']))
            print ("Instances:")
            for instance in label['Instances']:
                print ("  Bounding box")
                print ("    Top: " + str(instance['BoundingBox']['Top']))
                print ("    Left: " + str(instance['BoundingBox']['Left']))
                print ("    Width: " +  str(instance['BoundingBox']['Width']))
                print ("    Height: " +  str(instance['BoundingBox']['Height']))
                print ("  Confidence: " + str(instance['Confidence']))
                print()

            print ("Parents:")
            for parent in label['Parents']:
                print ("   " + parent['Name'])
            print ("----------")
            print ()

        txt_surrogates[photo]['labels'] = (' ').join(lbls)
        
        return len(response['Labels'])
    else:
        print(f'ERROR DID NOT RECEIVE LABELS FOR {photo}')
        return 0


def main():

    #photo='A_fire_helicopter_with_helicopter_bucket.jpg'
    bucket='mos22'

    for photo in fls:
        if photo in txt_surrogates.keys():
            label_count=detect_labels(photo, bucket)
            print("Labels detected: " + str(label_count))

    with open('text_surrogate_labels.json', 'w') as fp:
        dump(txt_surrogates, fp)

if __name__ == "__main__":
    main()