import { useNavigate } from "react-router-dom"
import CreateContainerDropdown from "../components/ContainerDropdown"

export default function Navbar({ onDropdownClicked }) {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem("authToken")
    navigate("/login")
  }

  return (
    <div className="navbar">
      <div className="navbar-side left">
        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="navbar-side right">
        <CreateContainerDropdown onDropdownClicked={onDropdownClicked} />
      </div>
    </div>
  )
}
