import React, { useState, useEffect, useRef } from "react";
import { io } from "socket.io-client";
import apiClient from "../../services/apiClient";
import TopicList from "../../components/Admin/TopicList";
import Breadcrumbs from "../../components/Navigation/Breadcrumbs";
import PriorityFilter from "../../components/Admin/PriorityFilter";
import ThroughputPulse from "../../components/Admin/ThroughputPulse";
import MessageInspector from "../../components/Admin/MessageInspector";
import "./EventBusMonitor.css";

const EventBusMonitor = () => {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [messages, setMessages] = useState([]);
  const [stats, setStats] = useState({});
  const [isConnected, setIsConnected] = useState(false);
  const [priorityFilters, setPriorityFilters] = useState(["CRITICAL", "HIGH", "MEDIUM", "LOW"]);
  const socketRef = useRef(null);
  const isFetchingRef = useRef(false);

  useEffect(() => {
    fetchTopics();
    fetchStats();
    setupWebSocket();

    const statsInterval = setInterval(() => {
      if (!isFetchingRef.current) {
        fetchStats();
      }
    }, 5000);
    return () => {
      clearInterval(statsInterval);
      if (socketRef.current) socketRef.current.disconnect();
    };
  }, []);

  const fetchTopics = async () => {
    if (isFetchingRef.current) return;
    isFetchingRef.current = true;
    try {
      const data = await apiClient.get("/admin/event-bus/topics");
      setTopics(data);
    } catch (error) {
      console.error("Error fetching topics:", error);
    } finally {
      isFetchingRef.current = false;
    }
  };

  const fetchStats = async () => {
    if (isFetchingRef.current) return;
    isFetchingRef.current = true;
    try {
      const data = await apiClient.get("/admin/event-bus/stats");
      setStats(data.topics || {});
    } catch (error) {
      console.error("Error fetching stats:", error);
    } finally {
      isFetchingRef.current = false;
    }
  };

  const setupWebSocket = () => {
    // Connect to the specific namespace on the main socket server
    socketRef.current = io("/admin/event-bus", {
      transports: ["websocket", "polling"],
      // path defaults to /socket.io, which is proxied correctly
    });

    socketRef.current.on("connect", () => {
      console.log("[EventBus] WebSocket Connected!", socketRef.current.id);
      setIsConnected(true);
    });
    
    socketRef.current.on("connect_error", (err) => {
      console.error("[EventBus] Connection Error:", err.message);
      setIsConnected(false);
    });

    socketRef.current.on("disconnect", (reason) => {
      console.warn("[EventBus] Disconnected:", reason);
      setIsConnected(false);
    });
    socketRef.current.on("event", (event) => {
      console.log("[EventBus] Received event:", event);
      setMessages((prev) => {
        const newMessages = [event, ...prev].slice(0, 100);
        console.log("[EventBus] Updated messages count:", newMessages.length);
        return newMessages;
      });
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

  const handlePriorityToggle = (priority) => {
    setPriorityFilters(prev => 
      prev.includes(priority) 
        ? prev.filter(p => p !== priority)
        : [...prev, priority]
    );
  };

  // Advanced Filtering via useMemo as requested
  const filteredMessages = React.useMemo(() => {
    return messages.filter(m => {
        const topicMatch = !selectedTopic || m.topic === selectedTopic;
        // Priority is nested in payload
        const msgPriority = m.payload?.priority || "LOW";
        const priorityMatch = priorityFilters.includes(msgPriority.toUpperCase());
        return topicMatch && priorityMatch;
    });
  }, [messages, selectedTopic, priorityFilters]);

  const [pulseHeight, setPulseHeight] = useState(250);
  const isResizingRef = useRef(false);

  const startResizing = (e) => {
    isResizingRef.current = true;
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", stopResizing);
    document.body.style.cursor = "row-resize";
    document.body.style.userSelect = "none";
  };

  const handleMouseMove = (e) => {
    if (!isResizingRef.current) return;
    const newHeight = e.clientY - 100; // Offset for header
    if (newHeight > 100 && newHeight < 600) {
      setPulseHeight(newHeight);
    }
  };

  const stopResizing = () => {
    isResizingRef.current = false;
    document.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", stopResizing);
    document.body.style.cursor = "default";
    document.body.style.userSelect = "auto";
  };

  return (
    <div className="event-bus-monitor-container">
      <header className="monitor-header">
        <div className="header-title-container">
          <div className="breadcrumb-path">
            SYSTEM ADMINISTRATION {">"} EVENT_BUS_NERVE_CENTER
          </div>
          <div className="header-main-row">
            <h1>NERVE_CENTER</h1>
            <span className="source-label">TYPE: SOCKET.IO_INTERNAL</span>
            <div className={`status-indicator ${isConnected ? "online" : "offline"}`}>
              {isConnected ? "LIVE" : "OFFLINE"}
            </div>
            {!isConnected && (
              <button className="reconnect-btn" onClick={setupWebSocket}>
                FORCE_RECONNECT
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="monitor-layout-grid">
        {/* LEFT SIDEBAR: FULL HEIGHT */}
        <aside className="monitor-sidebar-full">
          <TopicList
            topics={topics}
            stats={stats}
            onSelect={handleTopicSelect}
            selectedTopic={selectedTopic}
          />
        </aside>

        {/* RIGHT CONTENT: STACKED */}
        <main className="monitor-main-content">
          <div className="main-pulse-wrapper" style={{ height: `${pulseHeight}px` }}>
            <ThroughputPulse stats={stats} />
          </div>

          <div className="resize-handle-horizontal" onMouseDown={startResizing}>
            <div className="handle-line" />
          </div>

          <div className="main-controls-wrapper">
            <PriorityFilter 
              activeFilters={priorityFilters}
              onToggle={handlePriorityToggle}
            />
          </div>

          <section className="main-inspector-wrapper">
            <MessageInspector
              topic={selectedTopic}
              messages={filteredMessages}
            />
          </section>
        </main>
      </div>

      <div className="monitor-footer-buffer" />
    </div>
  );
};

export default EventBusMonitor;
