"""
M-Pesa Daraja API Integration for Elleden Hotel
Implements STK Push (Lipa Na M-Pesa Online)
"""
import base64
import json
import requests
from datetime import datetime
from django.conf import settings


class MpesaClient:
    """
    M-Pesa Daraja API Client for STK Push payments
    """
    
    def __init__(self):
        self.env = getattr(settings, 'MPESA_ENVIRONMENT', 'sandbox')
        
        if self.env == 'production':
            self.base_url = 'https://api.safaricom.co.ke'
        else:
            self.base_url = 'https://sandbox.safaricom.co.ke'
        
        self.consumer_key = getattr(settings, 'MPESA_CONSUMER_KEY', '')
        self.consumer_secret = getattr(settings, 'MPESA_CONSUMER_SECRET', '')
        self.shortcode = getattr(settings, 'MPESA_SHORTCODE', '')
        self.passkey = getattr(settings, 'MPESA_PASSKEY', '')
        self.callback_url = getattr(settings, 'MPESA_CALLBACK_URL', '')
    
    def get_access_token(self):
        """
        Generate OAuth access token from Daraja API
        """
        url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
        
        # Create base64 encoded credentials
        credentials = f'{self.consumer_key}:{self.consumer_secret}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result.get('access_token')
        except requests.exceptions.RequestException as e:
            raise MpesaError(f'Failed to get access token: {str(e)}')
    
    def generate_password(self, timestamp):
        """
        Generate the password for STK Push
        Password = Base64(Shortcode + Passkey + Timestamp)
        """
        data_to_encode = f'{self.shortcode}{self.passkey}{timestamp}'
        return base64.b64encode(data_to_encode.encode()).decode('utf-8')
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """
        Initiate STK Push request (Lipa Na M-Pesa Online)
        
        Args:
            phone_number: Customer phone number (format: 254XXXXXXXXX)
            amount: Amount to charge
            account_reference: Unique reference for the transaction (e.g., booking reference)
            transaction_desc: Description of the transaction
        
        Returns:
            dict: API response with CheckoutRequestID
        """
        access_token = self.get_access_token()
        
        url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        
        # Format phone number (remove leading 0 or +, ensure 254 prefix)
        phone = self.format_phone_number(phone_number)
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone,
            'PartyB': self.shortcode,
            'PhoneNumber': phone,
            'CallBackURL': self.callback_url,
            'AccountReference': account_reference[:12],  # Max 12 chars
            'TransactionDesc': transaction_desc[:13]  # Max 13 chars
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            if result.get('ResponseCode') == '0':
                return {
                    'success': True,
                    'checkout_request_id': result.get('CheckoutRequestID'),
                    'merchant_request_id': result.get('MerchantRequestID'),
                    'response_description': result.get('ResponseDescription'),
                    'customer_message': result.get('CustomerMessage')
                }
            else:
                return {
                    'success': False,
                    'error_code': result.get('errorCode'),
                    'error_message': result.get('errorMessage', result.get('ResponseDescription'))
                }
        except requests.exceptions.RequestException as e:
            raise MpesaError(f'STK Push request failed: {str(e)}')
    
    def query_stk_status(self, checkout_request_id):
        """
        Query the status of an STK Push transaction
        """
        access_token = self.get_access_token()
        
        url = f'{self.base_url}/mpesa/stkpushquery/v1/query'
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MpesaError(f'STK Query failed: {str(e)}')
    
    @staticmethod
    def format_phone_number(phone):
        """
        Format phone number to 254XXXXXXXXX format
        """
        phone = str(phone).strip().replace(' ', '').replace('-', '')
        
        if phone.startswith('+'):
            phone = phone[1:]
        
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        
        if phone.startswith('7') or phone.startswith('1'):
            phone = '254' + phone
        
        return phone


class MpesaError(Exception):
    """Custom exception for M-Pesa API errors"""
    pass


def process_mpesa_callback(callback_data):
    """
    Process M-Pesa callback data from STK Push
    
    Returns:
        dict with transaction details or error
    """
    try:
        body = callback_data.get('Body', {})
        stk_callback = body.get('stkCallback', {})
        
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')
        merchant_request_id = stk_callback.get('MerchantRequestID')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        
        if result_code == 0:
            # Successful transaction - extract callback metadata
            callback_metadata = stk_callback.get('CallbackMetadata', {})
            items = callback_metadata.get('Item', [])
            
            # Extract transaction details
            transaction_data = {}
            for item in items:
                name = item.get('Name')
                value = item.get('Value')
                if name == 'Amount':
                    transaction_data['amount'] = value
                elif name == 'MpesaReceiptNumber':
                    transaction_data['mpesa_receipt'] = value
                elif name == 'TransactionDate':
                    transaction_data['transaction_date'] = value
                elif name == 'PhoneNumber':
                    transaction_data['phone_number'] = value
            
            return {
                'success': True,
                'result_code': result_code,
                'result_desc': result_desc,
                'merchant_request_id': merchant_request_id,
                'checkout_request_id': checkout_request_id,
                **transaction_data
            }
        else:
            # Failed or cancelled transaction
            return {
                'success': False,
                'result_code': result_code,
                'result_desc': result_desc,
                'merchant_request_id': merchant_request_id,
                'checkout_request_id': checkout_request_id
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
