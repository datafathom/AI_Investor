"""
Alert Manager Service
Handles real-time alerting for critical errors and system issues
"""

import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertManager:
    """Manages alerts and notifications."""
    
    _instance = None
    _channels: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlertManager, cls).__new__(cls)
            cls._instance._init_channels()
        return cls._instance
    
    def _init_channels(self):
        """Initialize alert channels."""
        # Slack
        self._channels['slack'] = os.getenv('SLACK_WEBHOOK_URL')
        
        # PagerDuty
        self._channels['pagerduty'] = os.getenv('PAGERDUTY_ROUTING_KEY')
        
        # Email (SendGrid)
        self._channels['email'] = os.getenv('SENDGRID_API_KEY')
        
        # SMS (Twilio)
        self._channels['sms'] = {
            'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
            'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
            'from_number': os.getenv('TWILIO_FROM_NUMBER'),
        }
    
    def send_alert(self, message: str, level: AlertLevel = AlertLevel.ERROR,
                   channels: Optional[List[str]] = None, **kwargs):
        """Send alert to configured channels."""
        if channels is None:
            # Default channels based on level
            if level == AlertLevel.CRITICAL:
                channels = ['slack', 'pagerduty', 'email']
            elif level == AlertLevel.ERROR:
                channels = ['slack', 'email']
            else:
                channels = ['slack']
        
        alert_data = {
            'message': message,
            'level': level.value,
            'timestamp': datetime.utcnow().isoformat(),
            **kwargs
        }
        
        for channel in channels:
            try:
                if channel == 'slack' and self._channels.get('slack'):
                    self._send_slack_alert(alert_data)
                elif channel == 'pagerduty' and self._channels.get('pagerduty'):
                    self._send_pagerduty_alert(alert_data)
                elif channel == 'email' and self._channels.get('email'):
                    self._send_email_alert(alert_data)
                elif channel == 'sms' and self._channels.get('sms', {}).get('account_sid'):
                    self._send_sms_alert(alert_data, kwargs.get('phone_number'))
            except Exception as e:
                logger.error(f"Failed to send alert via {channel}: {e}")
    
    def _send_slack_alert(self, alert_data: Dict[str, Any]):
        """Send alert to Slack."""
        try:
            import requests
            
            webhook_url = self._channels['slack']
            color_map = {
                'info': '#36a64f',
                'warning': '#ff9900',
                'error': '#ff0000',
                'critical': '#8B0000'
            }
            
            payload = {
                'attachments': [{
                    'color': color_map.get(alert_data['level'], '#ff0000'),
                    'title': f"Alert: {alert_data['level'].upper()}",
                    'text': alert_data['message'],
                    'fields': [
                        {'title': 'Timestamp', 'value': alert_data['timestamp'], 'short': True},
                    ],
                    'footer': 'AI Investor',
                    'ts': int(datetime.fromisoformat(alert_data['timestamp']).timestamp())
                }]
            }
            
            # Add additional fields
            for key, value in alert_data.items():
                if key not in ['message', 'level', 'timestamp']:
                    payload['attachments'][0]['fields'].append({
                        'title': key.replace('_', ' ').title(),
                        'value': str(value),
                        'short': True
                    })
            
            response = requests.post(webhook_url, json=payload, timeout=5)
            response.raise_for_status()
            logger.debug("Slack alert sent successfully")
        except ImportError:
            logger.warning("requests library not available for Slack alerts")
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            raise
    
    def _send_pagerduty_alert(self, alert_data: Dict[str, Any]):
        """Send alert to PagerDuty."""
        try:
            import requests
            
            routing_key = self._channels['pagerduty']
            severity_map = {
                'info': 'info',
                'warning': 'warning',
                'error': 'error',
                'critical': 'critical'
            }
            
            payload = {
                'routing_key': routing_key,
                'event_action': 'trigger',
                'payload': {
                    'summary': alert_data['message'],
                    'severity': severity_map.get(alert_data['level'], 'error'),
                    'source': 'ai-investor-backend',
                    'custom_details': {
                        'timestamp': alert_data['timestamp'],
                        **{k: v for k, v in alert_data.items() 
                           if k not in ['message', 'level', 'timestamp']}
                    }
                }
            }
            
            response = requests.post(
                'https://events.pagerduty.com/v2/enqueue',
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            logger.debug("PagerDuty alert sent successfully")
        except ImportError:
            logger.warning("requests library not available for PagerDuty alerts")
        except Exception as e:
            logger.error(f"Failed to send PagerDuty alert: {e}")
            raise
    
    def _send_email_alert(self, alert_data: Dict[str, Any]):
        """Send alert via email."""
        try:
            from services.communication.email_service import get_email_service
            email_service = get_email_service()
            
            subject = f"[{alert_data['level'].upper()}] AI Investor Alert"
            body = f"""
            Alert: {alert_data['level'].upper()}
            Message: {alert_data['message']}
            Timestamp: {alert_data['timestamp']}
            
            Additional Details:
            {chr(10).join(f'{k}: {v}' for k, v in alert_data.items() if k not in ['message', 'level', 'timestamp'])}
            """
            
            # Send to admin email
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
            email_service.send_email(
                to=admin_email,
                subject=subject,
                body=body
            )
            logger.debug("Email alert sent successfully")
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            raise
    
    def _send_sms_alert(self, alert_data: Dict[str, Any], phone_number: Optional[str] = None):
        """Send alert via SMS."""
        if not phone_number:
            phone_number = os.getenv('ADMIN_PHONE_NUMBER')
        
        if not phone_number:
            logger.warning("No phone number provided for SMS alert")
            return
        
        try:
            from twilio.rest import Client
            
            twilio_config = self._channels['sms']
            client = Client(twilio_config['account_sid'], twilio_config['auth_token'])
            
            message = f"[{alert_data['level'].upper()}] {alert_data['message']}"
            
            client.messages.create(
                body=message,
                from_=twilio_config['from_number'],
                to=phone_number
            )
            logger.debug("SMS alert sent successfully")
        except ImportError:
            logger.warning("twilio library not available for SMS alerts")
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")
            raise


def get_alert_manager() -> AlertManager:
    """Get the alert manager instance."""
    return AlertManager()
