
import os
import logging
from typing import Dict, Any, Optional
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class PaymentService:
    """
    Service for managing subscriptions and payments via Stripe.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PaymentService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        sm = get_secret_manager()
        self._api_key = sm.get_secret('STRIPE_SECRET_KEY')
        self._webhook_secret = sm.get_secret('STRIPE_WEBHOOK_SECRET')
        self._is_simulated = True
        
        if self._api_key:
            try:
                import stripe
                stripe.api_key = self._api_key
                self._is_simulated = False
                logger.info("PaymentService initialized with Stripe.")
            except ImportError:
                logger.error("Stripe library missing. Operating in SIMULATION mode.")
        else:
            logger.warning("Stripe credentials missing. Operating in SIMULATION mode.")

    def create_checkout_session(self, user_id: str, tier: str) -> Dict[str, Any]:
        """
        Creates a Stripe Checkout Session for a specific tier.
        """
        if self._is_simulated:
            logger.info(f"Simulating checkout session for user {user_id} tier {tier}")
            return {
                "url": f"https://checkout.stripe.com/pay/sim_{user_id}_{tier}",
                "id": f"cs_test_{user_id}",
                "simulated": True
            }

        import stripe
        try:
            # Map tier names to Stripe Price IDs (In a real app, these are in config/env)
            price_map = {
                "pro": os.getenv("STRIPE_PRICE_PRO"),
                "institutional": os.getenv("STRIPE_PRICE_INST")
            }
            price_id = price_map.get(tier.lower())
            
            if not price_id:
                raise ValueError(f"Invalid tier: {tier}")

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=os.getenv('FRONTEND_URL', 'http://localhost:5173') + '/settings/billing?success=true',
                cancel_url=os.getenv('FRONTEND_URL', 'http://localhost:5173') + '/settings/billing?canceled=true',
                client_reference_id=user_id
            )
            return {"url": session.url, "id": session.id}
        except Exception as e:
            logger.error(f"Failed to create Stripe session: {e}")
            raise

    def get_subscription_status(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieves current subscription information for a user.
        """
        # Mock logic for demo/simulation
        # In a real app, this queries the local DB which is updated by webhooks
        return {
            "tier": "FREE",
            "status": "active",
            "next_billing": "N/A",
            "features": ["Education Mode", "Basic Scanner"]
        }

    def handle_webhook(self, payload: bytes, sig_header: str) -> Dict[str, Any]:
        """
        Processes incoming Stripe Webhooks.
        """
        if self._is_simulated:
            return {"status": "ignored", "reason": "simulation"}

        import stripe
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self._webhook_secret
            )
            
            # Handle specific events
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                user_id = session.get('client_reference_id')
                logger.info(f"Payment successful for user: {user_id}")
                # Update user tier in DB here...
            
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Webhook Error: {e}")
            raise

def get_payment_service():
    return PaymentService()
