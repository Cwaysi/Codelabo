from django.conf import settings
import requests

def send_message(to_: str, msg: str, sender: str):
    """ 
    get sender name, message, and receipient number
    to send sms
    """
    url = 'https://sms.arkesel.com/sms/api'
    api_key = settings.ARKSMS
    from_ = 'Codelabo'
    sms = msg + ' ' + 'From ' + sender
    
    query_params = {
    'action': 'send-sms',
    'api_key': api_key,
    'to': to_,
    'from': from_,
    'sms': sms
    }
    requests.get(url, params=query_params)