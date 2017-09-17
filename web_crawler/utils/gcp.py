# -*- coding: utf-8 -*-
import os
from google.cloud import storage

class GCPWrapper:
    """
    A simple gcp wrapper implemented by singleton
    """
    __single = None
    def __new__(clz):
        if not GCPWrapper.__single:
            GCPWrapper.__single = object.__new__(clz)
        return GCPWrapper.__single

    def __init__(self):
        self.client = storage.Client()
        self.bucket_prefix = 'ptt-rocks'

    def upload(self, bucket_name, blob_name):
        bucket_name = bucket_name.lower()
        bucket = self.client.get_bucket('{0}'.format(
                                        self.bucket_prefix))
        # destination blob name
        blob = bucket.blob('{0}/{1}.html'.format(
                            bucket_name,
                            blob_name))
        blob.upload_from_filename('tmp/{0}/{1}'.format(bucket_name, blob_name))

