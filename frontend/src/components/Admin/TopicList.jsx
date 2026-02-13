import React from 'react';
import './TopicList.css';

const TopicList = ({ topics, stats, onSelect, selectedTopic }) => {
    return (
        <div className="topic-list-container">
            <h3 className="section-title">ACTIVE_TOPICS</h3>
            <div className="topics-scroll">
                <div 
                    className={`topic-card ${!selectedTopic ? 'active' : ''}`}
                    onClick={() => onSelect(null)}
                >
                    <div className="topic-name">ALL_TOPICS</div>
                    <div className="topic-meta">
                        <span>VIEW ALL EVENTS</span>
                    </div>
                </div>
                {topics.map(topic => {
                    const topicStats = stats[topic.topic] || {};
                    const isActive = selectedTopic === topic.topic;
                    
                    return (
                        <div 
                            key={topic.topic} 
                            className={`topic-card ${isActive ? 'active' : ''}`}
                            onClick={() => onSelect(topic.topic)}
                        >
                            <div className="topic-name">{topic.topic}</div>
                            <div className="topic-meta">
                                <span>SUBS: {topic.subscriber_count}</span>
                                <span>MSGS: {topicStats.publish_count || 0}</span>
                            </div>
                            <div className="last-seen">
                                {topicStats.last_published ? 
                                    new Date(topicStats.last_published).toLocaleTimeString() : 
                                    'NEVER'}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default TopicList;
