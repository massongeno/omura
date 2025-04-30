"use client"

import { useState, useEffect, useRef } from "react"
import axios from "axios"
import Navbar from "./Navbar"

export default function Home() {
  const [containers, setContainers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [selectedIds, setSelectedIds] = useState([]);

  const previousContainers = useRef([]);

  const fetchContainers = async () => {
    try {
      setLoading(true)
      const token = localStorage.getItem("authToken")
      const response = await axios.get("http://localhost:5000/containers", {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (JSON.stringify(response.data) !== JSON.stringify(previousContainers.current)) {
        setContainers(response.data)
        previousContainers.current = response.data
      }
      console.log(response.data)
      setError("")
    } catch (err) {
      setError("Failed to fetch containers")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const formatPort = (port) => {
    if (!port) return '';
    const cleanPort = port.replace(/[{}\s]/g, '');
    return cleanPort.replace(/,/g, '\n');         
  };

  const handleContainerClick = (id) => {
    setSelectedIds((prevSelectedIds) => {
      if (prevSelectedIds.includes(id)) {
        return prevSelectedIds.filter((selectedId) => selectedId !== id);
      } else {
        return [...prevSelectedIds, id];
      }
    });
  };

  const startContainer = async () => {
    const token = localStorage.getItem("authToken");
    try {
      await Promise.all(selectedIds.map(async (id) => {
        await axios.post("http://localhost:5000/start_container", 
          new URLSearchParams({ action: id }), {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: `Bearer ${token}`
          }
        });
      }));
      fetchContainers();
    } catch (error) {
      console.error("Failed to start container:", error);
    }
  };
  

  const stopContainer = async () => {
    const token = localStorage.getItem("authToken");
    try {
      await Promise.all(selectedIds.map(async (id) => {
        await axios.post("http://localhost:5000/stop_container", 
          new URLSearchParams({ action: id }), {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: `Bearer ${token}`
          }
        });
      }));
      fetchContainers();
    } catch (error) {
      console.error("Failed to stop container:", error);
    }
  };
  

  const deleteContainer = async () => {
    const token = localStorage.getItem("authToken");
    try {
      await Promise.all(selectedIds.map(async (id) => {
        await axios.post("http://localhost:5000/remove_container", 
          new URLSearchParams({ action: id }), {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: `Bearer ${token}`
          }
        });
      }));
      fetchContainers();
    } catch (error) {
      console.error("Failed to delete container:", error);
    }
  };
  
  useEffect(() => {
    fetchContainers()
    const intervalId = setInterval(fetchContainers, 3000)
    return () => clearInterval(intervalId)
  }, [])

  return (
    <div>
      <Navbar onContainerCreated={fetchContainers} />
      <div className="container">
        <div className="home-header">
          <div className="left-buttons">
            <button onClick={fetchContainers} style={{ position: 'relative' }}>
              Refresh
            </button>
          </div>
          <div className="right-buttons">
            <button onClick={startContainer} className="start-button" style={{ position: 'relative' }}>
              Start
            </button>
            <button onClick={stopContainer} className="stop-button" style={{ position: 'relative' }}>
              Stop
            </button>
            <button onClick={deleteContainer} className="delete-button" style={{ position: 'relative' }}>
              Delete
            </button>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="container-grid">
          {containers.length > 0 ? (
            containers.map((container) => (
              <div 
                key={container.id}
                className={`container-card ${selectedIds.includes(container.id) ? 'selected' : ''}`}
                onClick={() => handleContainerClick(container.id)}
              >

                <div className={`status-dot ${container.status === 'running' ? 'running' : 'stopped'}`}></div>

                <div className="container-labels">
                  <div>Name</div>
                  <div>Ports</div>
                  <div></div> {/* gap */}
                  <div>Image</div>
                  <div></div> {/* gap */}
                  <div>Command</div>
                  <div>Date Created</div>
                  <div></div> {/* gap */}
                  <div>CPU</div>
                  <div>Memory</div>
                </div>

                <div className="container-values">
                  <div className="container-name">{container.name}</div>
                  <div className="container-ports">{formatPort(container.ports)}</div>
                  <div></div> {/* gap */}
                  <div className="container-image">{container.image}</div>
                  <div></div> {/* gap */}
                  <div className="container-command">{container.cmd}</div>
                  <div className="container-created">{container.created}</div>
                  <div></div> {/* gap */}
                  <div className="container-cpu">{parseFloat(container.cpu_usage).toFixed(2) + "%"}</div>
                  <div className="container-mem">{parseFloat(container.memory_usage).toFixed(2) + "%"}</div>
                </div>

              </div>
            ))
          ) : (
            <div className="empty-message">
              <p style={{ color: "#666" }}>No containers found. </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
