import { IconDefinition } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

interface SidebarItemProps {
    icon: IconDefinition
    label: string
    active: boolean
}

const SidebarItem : React.FC<SidebarItemProps> = ({ icon, label, active = false }) => (
    <div className={`flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 ${active && `bg-gray-300`} cursor-pointer transition`}>
        <FontAwesomeIcon icon={icon} className="text-gray-400" />
        <span className="text-sm">{label}</span>
    </div>
)

export default SidebarItem