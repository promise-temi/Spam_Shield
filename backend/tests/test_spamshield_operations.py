# import os
# import re
# import re
# import sys
# import pytest
# import pandas as pd



# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
# from SpamShield_Operations import SpamShield_Operations

# def test_new_message(monkeypatch):
#     class FakeDB:
#         def save_message(self, *args, **kwargs):
#             return None
#     message = pd.DataFrame([{'text':'Je teste mon propre outil de détection de spam, je trouve qu\'il est très efficace !', 'label':1}])
#     metadata = {
#     "name":"Promise",
#     "surname":"John",
#     "email":"Promise.john@gmail.com",
#     "phone":"0653389212",
#     "subject":"Je teste mon propre outil de détection de spam :)",
#     }
#     SpamShield_Operations().New_Message(message, metadata)