"use client"

import { useState, useEffect } from "react"
import axios from "axios"

export default function CreateContainerDropdown({ onDropdownClicked }) {
  const [isOpen, setIsOpen] = useState(false)
  const [name, setName] = useState("")
  const [image, setImage] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  const toggleDropdown = () => {
    setIsOpen(!isOpen)
    if (!isOpen) {
      setError("")
      setSuccess("")
      setName("")
      setImage("")
    }
  }

  const handleClickOutside = (e) => {
    if (isOpen && !e.target.closest(".dropdown-container")) {
      setIsOpen(false)
    }
  }

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [isOpen])

  const handleCreateContainer = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")
    setSuccess("")

    try {
      const token = localStorage.getItem("authToken")
      await axios.post(
        "http://localhost:5000/containers",
        { name, image },
        { headers: { Authorization: `Bearer ${token}` } },
      )
      setSuccess("Container created successfully!")
      setName("")
      setImage("")
      if (onDropdownClicked) onDropdownClicked()
    } catch (err) {
      setError(err.response?.data?.message || "Failed to create container")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dropdown-container">
      <button onClick={toggleDropdown} className="btn-green dropdown-button">Create Container</button>

      {isOpen && (
        <div className="dropdown-menu">
          <div className="dropdown-content">
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}

            <form onSubmit={handleCreateContainer}>
              <div className="form-group">
                <label className="form-label" htmlFor="name">Container Name</label>
                <input id="name" type="text" value={name} onChange={(e) => setName(e.target.value)} required />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="image">Docker Image</label>
                <input
                  id="image"
                  type="text"
                  value={image}
                  onChange={(e) => setImage(e.target.value)}
                  placeholder="e.g., nginx:latest"
                  required
                />
              </div>

              <button type="submit" disabled={loading}>
                {loading ? "Creating..." : "Create Container"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
