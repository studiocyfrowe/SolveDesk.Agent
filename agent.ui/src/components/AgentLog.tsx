import { IconDefinition } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React from "react"
import { AgentEvent } from "../types/AgentEvent"
import RenderContent from "../services/RenderContent"

interface AgentLogProps {
    base: string
    icon: IconDefinition
    log: AgentEvent
}

const AgentLog: React.FC<AgentLogProps> = ({ base, icon, log }) => {
    return (
        <div className={`${base} bg-blue-500/10 flex gap-2 items-start`}>
            <FontAwesomeIcon icon={icon} className="mt-1 text-blue-400" />

            <div className="flex-1 space-y-1">
                {"tool" in log && (
                    <div>
                        <span className="text-blue-300 font-medium mr-1">
                            Tool:
                        </span>
                        <span>{log.tool}</span>
                    </div>
                )}

                {"content" in log && (
                    <RenderContent content={log.content} />
                )}
            </div>
        </div>
    )
}

export default AgentLog