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

            <div className="flex-1 min-w-0 space-y-1 break-words">
                {"tool" in log && (
                    <div>
                        <span className="text-blue-300 font-medium mr-1">
                            Tool:
                        </span>
                        <span className="break-words">{log.tool}</span>
                    </div>
                )}

                {"content" in log && (
                    <div className="whitespace-pre-wrap break-words font-mono text-sm bg-black rounded-sm px-4 py-3">
                        {typeof log.content === "string"
                            ? log.content
                            : JSON.stringify(log.content, null, 2)}
                    </div>
                )}
            </div>
        </div>
    )
}

export default AgentLog