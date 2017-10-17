# coding=utf-8

import json
import boto3
from django.conf import settings


class SNS(object):
    def __init__(self):

        self.client = boto3.client('sns', aws_access_key_id=settings.AWS_SNS_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_SNS_SECRET_ACCESS_KEY, )

        self.platform_arn = settings.AWS_SNS_PLATFORM_APP_ARN

        self.resource = boto3.resource(service_name="sns",
                                       aws_access_key_id=settings.AWS_SNS_ACCESS_KEY_ID,
                                       aws_secret_access_key=settings.AWS_SNS_SECRET_ACCESS_KEY,
                                       )

    def create_gcm_endpoint(self, token):
        response = self.client.create_platform_endpoint(
            PlatformApplicationArn=self.platform_arn,
            Token=token,
            Attributes={
                'Enabled': 'true'
            }
        )
        return response

    def delete_gcm_endpoint(self, arn):
        response = self.client.delete_endpoint(
                    EndpointArn=arn
                )
        return response

    def send_message(self, arn, message, extra_data=None):
        data_dict = {'message':message}
        if extra_data:
            data_dict.update(extra_data)
        apns_dict = {'data':data_dict}
        apns_string = json.dumps(apns_dict,ensure_ascii=False)
        message = {'default':message,'GCM':apns_string}
        messageJSON = json.dumps(message,ensure_ascii=False)
        response = self.client.publish(
                    TargetArn=arn,
                    MessageStructure='json',
                    Message=messageJSON
                )
        return response

