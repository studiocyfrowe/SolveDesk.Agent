import React from "react"
import { AgentEvent } from "../types/AgentEvent"
import AgentLog from "./AgentLog"
import {
    faChartLine,
    faRobot,
    faTools,
    faTriangleExclamation,
    faXmark,
    faBookReader
} from "@fortawesome/free-solid-svg-icons"

interface LogsContainerProps {
    logs: AgentEvent[]
    loading: boolean
}

const LogsContainer : React.FC<LogsContainerProps> = ({ logs, loading }) => {
    const base = "p-3 rounded-sm text-sm border border-gray-800"

    return (
        <div className="bg-[#020617] border border-gray-800 rounded-2xl p-4 space-y-3">

            {logs.length === 0 && !loading && (
                <div className="text-center text-gray-500 py-10">
                    Brak danych
                </div>
            )}

            {logs.map((log, i) => {

                if (log.type === "plan") return <AgentLog key={i} base={base} log={log} icon={faBookReader} />
                if (log.type === "action") return <AgentLog key={i} base={base} log={log} icon={faTools} />
                if (log.type === "observation") return <AgentLog key={i} base={base} log={log} icon={faChartLine} />
                if (log.type === "summary") return <AgentLog key={i} base={base} log={log} icon={faTriangleExclamation} />
                if (log.type === "error") return <AgentLog key={i} base={base} log={log} icon={faXmark} />

                return null
            })}
        </div>
    )
}

export default LogsContainer