import { faChartLine, faGear, faMemory, faMicrochip } from "@fortawesome/free-solid-svg-icons"
import SidebarItem from "./SidebarItem"
import { NavLink } from "react-router-dom"

const Navigation = () => {
    return (
        <nav className="flex-1 p-4 space-y-2">
            <NavLink to="/" end>
                {({ isActive }) => (
                    <SidebarItem
                        icon={faChartLine}
                        label="Dashboard"
                        active={isActive}
                    />
                )}
            </NavLink>
            <NavLink to="/cpu-details">
                {({ isActive }) => (
                    <SidebarItem
                        icon={faMicrochip}
                        label="CPU"
                        active={isActive}
                    />
                )}
            </NavLink>
            <NavLink to="/memory">
                {({ isActive }) => (
                    <SidebarItem
                        icon={faMemory}
                        label="Memory"
                        active={isActive}
                    />
                )}
            </NavLink>
            <NavLink to="/settings">
                {({ isActive }) => (
                    <SidebarItem
                        icon={faGear}
                        label="Settings"
                        active={isActive}
                    />
                )}
            </NavLink>
        </nav>
    )
}

export default Navigation