"""
Web3 API - REST endpoints for cryptocurrency management.

Phase 51: Provides endpoints for wallet balances, LP tracking,
and gas optimization.

Endpoints:
    GET  /api/v1/web3/portfolio/<user_id>        - Aggregated portfolio
    GET  /api/v1/web3/balance/<address>/<chain>  - Single wallet balance
    GET  /api/v1/web3/gas/<chain>                - Current gas prices
    POST /api/v1/web3/gas/queue                  - Queue transaction
    GET  /api/v1/web3/lp/<user_id>               - LP positions
    POST /api/v1/web3/lp/il                      - Calculate impermanent loss
"""

from flask import Blueprint, jsonify, request
from services.crypto.wallet_service import WalletService
from services.crypto.lp_tracker_service import LPTrackerService, LPPosition
from services.crypto.gas_service import GasService
import logging

logger = logging.getLogger(__name__)

web3_bp = Blueprint('web3', __name__)
_wallet_service = WalletService()
_lp_service = LPTrackerService()
_gas_service = GasService()


@web3_bp.route('/portfolio/<user_id>', methods=['GET'])
async def get_portfolio(user_id: str):
    """Get aggregated crypto portfolio for a user."""
    try:
        portfolio = await _wallet_service.get_aggregated_portfolio(user_id)
        
        return jsonify({
            "success": True,
            "data": {
                "user_id": portfolio.user_id,
                "total_usd_value": portfolio.total_usd_value,
                "balances": [
                    {
                        "token": b.token,
                        "chain": b.chain.value,
                        "amount": b.amount,
                        "usd_value": b.usd_value,
                        "price": b.price
                    }
                    for b in portfolio.balances
                ],
                "wallets": portfolio.wallets,
                "last_updated": portfolio.last_updated
            }
        })
        
    except Exception as e:
        logger.error(f"Portfolio fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@web3_bp.route('/balance/<address>/<chain>', methods=['GET'])
async def get_balance(address: str, chain: str):
    """Get balance for a specific wallet on a chain."""
    try:
        balance = await _wallet_service.get_wallet_balance(address, chain)
        
        return jsonify({
            "success": True,
            "data": {
                "token": balance.token,
                "chain": balance.chain.value,
                "amount": balance.amount,
                "usd_value": balance.usd_value,
                "price": balance.price
            }
        })
        
    except Exception as e:
        logger.error(f"Balance fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@web3_bp.route('/chains', methods=['GET'])
def get_chains():
    """Get supported blockchain networks."""
    chains = _wallet_service.get_supported_chains()
    return jsonify({"success": True, "data": chains})


@web3_bp.route('/gas/<chain>', methods=['GET'])
async def get_gas(chain: str):
    """Get current gas prices for a chain."""
    try:
        gas = await _gas_service.get_current_gas(chain)
        stats = _gas_service.get_24h_stats(chain)
        is_spike = await _gas_service.detect_spike(chain)
        
        return jsonify({
            "success": True,
            "data": {
                "chain": gas.chain,
                "base_fee_gwei": gas.base_fee_gwei,
                "priority_fee_gwei": gas.priority_fee_gwei,
                "estimated_usd": gas.estimated_usd,
                "trend": gas.trend,
                "is_spike": is_spike,
                "stats_24h": stats,
                "updated_at": gas.updated_at
            }
        })
        
    except Exception as e:
        logger.error(f"Gas fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@web3_bp.route('/gas/optimal-window', methods=['GET'])
async def get_optimal_window():
    """Get optimal execution time window."""
    try:
        window = await _gas_service.get_optimal_execution_window()
        
        return jsonify({
            "success": True,
            "data": {
                "start_time": window.start_time,
                "end_time": window.end_time,
                "expected_savings_percent": window.expected_savings_percent,
                "confidence": window.confidence
            }
        })
        
    except Exception as e:
        logger.error(f"Optimal window fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@web3_bp.route('/gas/queue', methods=['POST'])
async def queue_transaction():
    """Queue transaction for optimal gas execution."""
    try:
        data = request.get_json()
        chain = data.get('chain', 'ethereum')
        target_gas = data.get('target_gas_gwei', 20)
        ttl_hours = data.get('ttl_hours', 24)
        
        tx = await _gas_service.queue_transaction(chain, target_gas, ttl_hours)
        
        return jsonify({
            "success": True,
            "data": {
                "id": tx.id,
                "chain": tx.chain,
                "target_gas_gwei": tx.target_gas_gwei,
                "expires_at": tx.expires_at,
                "status": tx.status
            }
        })
        
    except Exception as e:
        logger.error(f"Queue transaction failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@web3_bp.route('/lp/<user_id>', methods=['GET'])
async def get_lp_positions(user_id: str):
    """Get LP positions for a user."""
    try:
        positions = await _lp_service.get_lp_positions(user_id)
        
        results = []
        for pos in positions:
            il_result = await _lp_service.calculate_impermanent_loss(pos)
            drain_alert = await _lp_service.detect_pool_drain(pos.pool_address)
            
            results.append({
                "pool_address": pos.pool_address,
                "token0": pos.token0,
                "token1": pos.token1,
                "token0_amount": pos.token0_amount,
                "token1_amount": pos.token1_amount,
                "pool_share": pos.pool_share,
                "impermanent_loss": {
                    "hodl_value_usd": il_result.hodl_value_usd,
                    "lp_value_usd": il_result.lp_value_usd,
                    "loss_usd": il_result.impermanent_loss_usd,
                    "loss_percent": il_result.impermanent_loss_percent,
                    "fees_earned_usd": il_result.fees_earned_usd,
                    "net_gain_usd": il_result.net_gain_usd
                },
                "drain_alert": {
                    "severity": drain_alert.severity,
                    "recommendation": drain_alert.recommendation
                } if drain_alert else None
            })
        
        return jsonify({"success": True, "data": results})
        
    except Exception as e:
        logger.error(f"LP positions fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@web3_bp.route('/lp/il', methods=['POST'])
async def calculate_impermanent_loss():
    """Calculate impermanent loss for a given position."""
    try:
        data = request.get_json()
        
        position = LPPosition(
            pool_address=data.get('pool_address', 'custom'),
            token0=data.get('token0', 'ETH'),
            token1=data.get('token1', 'USDC'),
            token0_amount=data.get('token0_amount', 1.0),
            token1_amount=data.get('token1_amount', 3000.0),
            entry_price_ratio=data.get('entry_price_ratio', 3000.0),
            current_price_ratio=data.get('current_price_ratio', 3250.0),
            pool_share=data.get('pool_share', 0.001)
        )
        
        result = await _lp_service.calculate_impermanent_loss(position)
        
        return jsonify({
            "success": True,
            "data": {
                "hodl_value_usd": result.hodl_value_usd,
                "lp_value_usd": result.lp_value_usd,
                "impermanent_loss_usd": result.impermanent_loss_usd,
                "impermanent_loss_percent": result.impermanent_loss_percent,
                "fees_earned_usd": result.fees_earned_usd,
                "net_gain_usd": result.net_gain_usd,
                "break_even_fee_apr": result.break_even_fee_apr
            }
        })
        
    except Exception as e:
        logger.error(f"IL calculation failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@web3_bp.route('/liquidity/depth/<pool_address>', methods=['GET'])
async def get_liquidity_depth(pool_address: str):
    """Get liquidity depth map for a pool."""
    try:
        depth = await _lp_service.get_liquidity_depth(pool_address)
        return jsonify({"success": True, "data": depth})
    except Exception as e:
        logger.error(f"Liquidity depth fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
