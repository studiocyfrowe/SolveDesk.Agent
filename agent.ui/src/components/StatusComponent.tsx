import React from "react"
import { AgentEvent } from "../types/AgentEvent"

interface StatusComponentProps {
    loading: boolean
    logs: AgentEvent[]
}

const StatusComponent: React.FC<StatusComponentProps> = ({ loading, logs }) => {
    return (
        <div className="w-full">
            <div className="flex items-center justify-between text-xs bg-green-900/40 border border-green-700 px-4 py-3 rounded-md">
                <div className="flex items-center gap-2">
                    <div
                        className={`w-2 h-2 rounded-full ${
                            loading ? "bg-green-400 animate-pulse" : "bg-gray-400"
                        }`}
                    />

                    <span
                        className={`font-medium ${
                            loading ? "text-green-300" : "text-gray-400"
                        }`}
                    >
                        {loading ? "Running..." : "Idle"}
                    </span>

                    {loading && (
                        <span className="text-green-400 animate-pulse">
                            analizowane...
                        </span>
                    )}
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-green-300/70">Logs</span>
                    <span className="bg-green-800 px-2 py-0.5 rounded text-green-200">
                        {logs.length}
                    </span>
                </div>
            </div>
            {loading && (
                <div className="h-1 w-full bg-green-900/30 rounded-b-md overflow-hidden">
                    <div className="h-full bg-green-400 animate-[loading_1.5s_infinite] w-1/3" />
                </div>
            )}
        </div>
    )
}

export default StatusComponent