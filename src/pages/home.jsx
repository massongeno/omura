"use client"

import { useState, useEffect, useRef } from "react"
import axios from "axios"
import Navbar from "./Navbar"

export default function Home() {
  const [containers, setContainers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

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

  useEffect(() => {
    fetchContainers()
    const intervalId = setInterval(fetchContainers, 10000)
    return () => clearInterval(intervalId)
  }, [])

  return (
    <div>
      <Navbar onContainerCreated={fetchContainers} />
      <div className="container">
        <div className="home-header">
          <button onClick={fetchContainers} style={{ position: 'relative' }}>
            Refresh
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="container-grid">
          {containers.length > 0 ? (
            containers.map((container) => (
              <div key={container.id} className="container-card">

                <div className={`status-dot ${container.status === 'running' ? 'running' : 'stopped'}`}></div>

                <div className="container-labels">
                  <div>Name</div>
                  <div>Image</div>
                  <div>CPU</div>
                  <div>Disk</div>
                  <div>Memory</div>
                </div>

                <div className="container-values">
                  <div className="container-name">{container.name}</div>
                  <div className="container-image">{container.image}</div>
                  <div className="container-cpu">{container.cpu}</div>
                  <div className="container-disk">{container.disk}</div>
                  <div className="container-mem">{container.mem}</div>
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
