import React, { useState, useEffect, useRef } from "react";
import { io } from "socket.io-client";
import TopicList from "../../components/admin/TopicList";
import MessageFlowChart from "../../components/admin/MessageFlowChart";
import MessageInspector from "../../components/admin/MessageInspector";
import "./EventBusMonitor.css";

const EventBusMonitor = () => {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [messages, setMessages] = useState([]);
  const [stats, setStats] = useState({});
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef(null);

  useEffect(() => {
    fetchTopics();
    fetchStats();
    setupWebSocket();

    const statsInterval = setInterval(fetchStats, 5000);
    return () => {
      clearInterval(statsInterval);
      if (socketRef.current) socketRef.current.disconnect();
    };
  }, []);

  const fetchTopics = async () => {
    try {
      const response = await fetch("/api/v1/admin/event-bus/topics");
      const data = await response.json();
      setTopics(data);
    } catch (error) {
      console.error("Error fetching topics:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch("/api/v1/admin/event-bus/stats");
      const data = await response.json();
      setStats(data.topics || {});
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const setupWebSocket = () => {
    // Connect to the specific mount point
    socketRef.current = io("/ws/admin/event-bus", {
      path: "/ws/admin/event-bus/socket.io",
    });

    socketRef.current.on("connect", () => setIsConnected(true));
    socketRef.current.on("disconnect", () => setIsConnected(false));
    socketRef.current.on("event", (event) => {
      setMessages((prev) => [event, ...prev].slice(0, 100));
      // Update local stats incrementaly
      setStats((prev) => ({
        ...prev,
        [event.topic]: {
          ...prev[event.topic],
          publish_count: (prev[event.topic]?.publish_count || 0) + 1,
          last_published: event.timestamp,
        },
      }));
    });
  };

  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic);
  };

  return (
    <div className="event-bus-monitor-container">
      <header className="monitor-header">
        <div className="header-title">
          <h1>EVENT_BUS_NERVE_CENTER</h1>
          <div
            className={`status-indicator ${isConnected ? "online" : "offline"}`}
          >
            {isConnected ? "LIVE_STREAM_ACTIVE" : "STREAM_DISCONNECTED"}
          </div>
        </div>
      </header>

      <div className="monitor-grid">
        <aside className="monitor-sidebar">
          <TopicList
            topics={topics}
            stats={stats}
            onSelect={handleTopicSelect}
            selectedTopic={selectedTopic}
          />
        </aside>

        <main className="monitor-main">
          <section className="chart-section">
            <MessageFlowChart stats={stats} />
          </section>
          <section className="inspector-section">
            <MessageInspector
              topic={selectedTopic}
              messages={messages.filter(
                (m) => !selectedTopic || m.topic === selectedTopic,
              )}
            />
          </section>
        </main>
      </div>
    </div>
  );
};

export default EventBusMonitor;
