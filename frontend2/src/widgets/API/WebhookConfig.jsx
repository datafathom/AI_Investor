import React from 'react';
import { Webhook, Send, Settings, Code } from 'lucide-react';
import './WebhookConfig.css';

const WebhookConfig = () => {
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
                <div className="target-item">
                    <div className="target-info">
                        <span className="target-name">Slack #trading-alerts</span>
                        <span className="target-url">https://hooks.slack.com/...</span>
                    </div>
                    <div className="target-actions">
                        <button className="test-send"><Send size={12} /> Test</button>
                        <div className="toggle active">ON</div>
                    </div>
                </div>
                 <div className="target-item">
                    <div className="target-info">
                        <span className="target-name">Discord #general</span>
                        <span className="target-url">https://discord.com/api/...</span>
                    </div>
                    <div className="target-actions">
                        <button className="test-send"><Send size={12} /> Test</button>
                        <div className="toggle">OFF</div>
                    </div>
                </div>
            </div>
            
            <div className="response-log">
                <span className="text-secondary">Last Test Response:</span> <span className="text-green-400">200 OK (14ms)</span>
            </div>
        </div>
    );
};

export default WebhookConfig;
