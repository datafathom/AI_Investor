import React, { useEffect } from 'react';
import { Webhook, Send, Settings, Code } from 'lucide-react';
import useAPIStore from '../../stores/apiStore';
import './WebhookConfig.css';

const WebhookConfig = () => {
    const { 
        webhooks, 
        fetchWebhooks, 
        testWebhook, 
        loading 
    } = useAPIStore();

    useEffect(() => {
        fetchWebhooks();
    }, [fetchWebhooks]);

    const handleTestWebhook = async (webhookId) => {
        try {
            const result = await testWebhook(webhookId);
            alert(`Webhook Test Result: ${result.status || 'Success'}\n(Message: ${result.message || 'Sent successfully'})`);
        } catch (error) {
            alert(`Webhook Test Failed: ${error.message}`);
        }
    };

    return (
        <div className="webhook-config-widget">
            <div className="widget-header">
                <h3><Webhook size={18} className="text-purple-400" /> Custom Webhook Triggers</h3>
                <button className="new-webhook-btn"><Settings size={12} /> Configure</button>
            </div>

            <div className="payload-builder">
                <h4><Code size={14} /> Payload Template Builder</h4>
                <div className="code-editor">
                    <div className="line-nums">1<br/>2<br/>3<br/>4<br/>5</div>
                    <pre className="code-content">
                        {`{
  "text": "Trade Alert: {{ticker}}",
  "blocks": [
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Price:* {{price}}" }
    }
  ]
}`}
                    </pre>
                </div>
                <div className="variable-picker">
                    <span>Insert Variable:</span>
                    <button className="var-chip">{'{{ticker}}'}</button>
                    <button className="var-chip">{'{{price}}'}</button>
                    <button className="var-chip">{'{{side}}'}</button>
                </div>
            </div>

            <div className="integration-targets">
                {webhooks.length > 0 ? (
                    webhooks.map((w, idx) => (
                        <div key={idx} className="target-item">
                            <div className="target-info">
                                <span className="target-name">{w.name || w.url}</span>
                                <span className="target-url">{w.url}</span>
                            </div>
                            <div className="target-actions">
                                <button 
                                    className="test-send" 
                                    onClick={() => handleTestWebhook(w.id)}
                                    disabled={loading}
                                >
                                    <Send size={12} /> Test
                                </button>
                                <div className={`toggle ${w.active ? 'active' : ''}`}>
                                    {w.active ? 'ON' : 'OFF'}
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="p-4 text-center text-zinc-500 font-mono text-xs">
                        {loading ? 'SYNCING WEBHOOK DATA...' : 'NO WEBHOOKS CONFIGURED'}
                    </div>
                )}
            </div>
            
            <div className="response-log">
                <span className="text-secondary">System Health:</span> <span className="text-green-400">Webhook Engine Active</span>
            </div>
        </div>
    );
};

export default WebhookConfig;
