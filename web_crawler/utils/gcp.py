# -*- coding: utf-8 -*-
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
        self.bucket_name = 'ptt-rocks-us-west'

