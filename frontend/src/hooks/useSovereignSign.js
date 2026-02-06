/**
 * useSovereignSign - WebAuthn Command Signing Hook
 * Phase 1 Implementation: The Sovereign Kernel
 * 
 * This hook provides the "Biometric Gateway" for all write operations.
 * It interfaces with the browser's WebAuthn API to obtain cryptographic
 * signatures for commands before they are sent to the backend.
 * 
 * ACCEPTANCE CRITERIA from Phase_1_ImplementationPlan.md:
 * - C1: Successfully triggers a native OS biometric prompt (navigator.credentials.get)
 */

import { useState, useCallback } from 'react';

const API_BASE = '/api/v1';

/**
 * @typedef {Object} SovereignSignState
 * @property {boolean} isPending - Whether a signing operation is in progress
 * @property {boolean} isSuccess - Whether the last signing was successful
 * @property {string|null} error - Error message if signing failed
 * @property {string|null} challengeId - Current challenge ID from backend
 */

/**
 * @typedef {Object} SignedCommand
 * @property {string} challengeId - The challenge that was signed
 * @property {string} signature - Hex-encoded signature
 * @property {Object} payload - The original command payload
 */

/**
 * Hook for WebAuthn command signing.
 * 
 * Usage:
 * ```jsx
 * const { signCommand, isPending, error } = useSovereignSign();
 * 
 * const handleTrade = async () => {
 *   const signed = await signCommand({ action: 'BUY', ticker: 'AAPL', qty: 10 });
 *   if (signed) {
 *     await executeTradeWithSignature(signed);
 *   }
 * };
 * ```
 * 
 * @returns {Object} Signing utilities and state
 */
export function useSovereignSign() {
  const [state, setState] = useState({
    isPending: false,
    isSuccess: false,
    error: null,
    challengeId: null,
  });

  /**
   * Request a challenge from the backend for a specific command.
   * @param {Object} commandPayload - The command to be signed
   * @returns {Promise<Object|null>} Challenge data or null on error
   */
  const requestChallenge = useCallback(async (commandPayload) => {
    try {
      const response = await fetch(`${API_BASE}/auth/challenge`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: commandPayload }),
      });

      if (!response.ok) {
        throw new Error(`Challenge request failed: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.error('[useSovereignSign] Challenge request error:', err);
      return null;
    }
  }, []);

  /**
   * Trigger the WebAuthn biometric prompt and sign a command.
   * 
   * This is the core function that:
   * 1. Requests a challenge from the backend
   * 2. Triggers the browser's WebAuthn credential.get
   * 3. Returns the signed command ready for API submission
   * 
   * @param {Object} commandPayload - The command to be cryptographically signed
   * @returns {Promise<SignedCommand|null>} Signed command or null if cancelled/failed
   */
  const signCommand = useCallback(async (commandPayload) => {
    setState(prev => ({ ...prev, isPending: true, error: null }));

    try {
      // Step 1: Get challenge from backend
      const challengeData = await requestChallenge(commandPayload);
      if (!challengeData) {
        throw new Error('Failed to obtain challenge from server');
      }

      setState(prev => ({ ...prev, challengeId: challengeData.challenge_id }));

      // Step 2: Prepare WebAuthn options
      const challengeBuffer = hexToBuffer(challengeData.challenge);
      
      // Check if WebAuthn is supported
      if (!window.PublicKeyCredential) {
        throw new Error('WebAuthn is not supported in this browser');
      }

      // Step 3: Trigger biometric prompt
      const publicKeyCredentialRequestOptions = {
        challenge: challengeBuffer,
        timeout: 60000, // 60 seconds
        userVerification: 'required', // Require biometric/PIN
        rpId: window.location.hostname,
      };

      const credential = await navigator.credentials.get({
        publicKey: publicKeyCredentialRequestOptions,
      });

      if (!credential) {
        throw new Error('User cancelled the authentication');
      }

      // Step 4: Extract and encode signature
      const signature = bufferToHex(credential.response.signature);
      const authenticatorData = bufferToHex(credential.response.authenticatorData);
      const clientDataJSON = bufferToHex(credential.response.clientDataJSON);

      setState(prev => ({ ...prev, isPending: false, isSuccess: true }));

      return {
        challengeId: challengeData.challenge_id,
        signature,
        authenticatorData,
        clientDataJSON,
        payload: commandPayload,
      };

    } catch (err) {
      console.error('[useSovereignSign] Signing error:', err);
      setState(prev => ({
        ...prev,
        isPending: false,
        isSuccess: false,
        error: err.message || 'Unknown signing error',
      }));
      return null;
    }
  }, [requestChallenge]);

  /**
   * Check if WebAuthn is available in this browser.
   * @returns {boolean}
   */
  const isWebAuthnAvailable = useCallback(() => {
    return !!window.PublicKeyCredential;
  }, []);

  /**
   * Reset the signing state (clear errors, etc.)
   */
  const reset = useCallback(() => {
    setState({
      isPending: false,
      isSuccess: false,
      error: null,
      challengeId: null,
    });
  }, []);

  return {
    signCommand,
    isWebAuthnAvailable,
    reset,
    isPending: state.isPending,
    isSuccess: state.isSuccess,
    error: state.error,
    challengeId: state.challengeId,
  };
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Convert a hex string to an ArrayBuffer.
 * @param {string} hex 
 * @returns {ArrayBuffer}
 */
function hexToBuffer(hex) {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
  }
  return bytes.buffer;
}

/**
 * Convert an ArrayBuffer to a hex string.
 * @param {ArrayBuffer} buffer 
 * @returns {string}
 */
function bufferToHex(buffer) {
  const bytes = new Uint8Array(buffer);
  return Array.from(bytes)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

export default useSovereignSign;
