import React, { useState } from "react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import {
    faChartLine,
    faNoteSticky,
    faRobot,
    faTools,
    faTriangleExclamation,
    faXmark,
    faPlay,
    faBookReader
} from "@fortawesome/free-solid-svg-icons"
import MainLayout from "../layouts/MainLayout"
import RunAgent from "../services/RunAgent"
import AgentLog from "../components/AgentLog"

const Home: React.FC = () => {
    const { logs, loading, runAgent } = RunAgent()

    return (
        <MainLayout>
            <div className="max-w-5xl mx-auto space-y-6">
                <div className="bg-[#020617] border border-gray-800 rounded-2xl p-6 flex justify-between items-center">
                    <div>
                        <h1 className="text-lg font-semibold flex items-center gap-2">
                            <FontAwesomeIcon icon={faRobot} className="text-blue-500" />
                            AI Diagnostic Agent
                        </h1>
                        <p className="text-sm text-gray-400">
                            System analysis & troubleshooting
                        </p>
                    </div>

                    <button
                        onClick={runAgent}
                        disabled={loading}
                        className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg text-sm flex items-center gap-2 disabled:opacity-50"
                    >
                        <FontAwesomeIcon icon={faPlay} />
                        {loading ? "Analiza..." : "Start"}
                    </button>
                </div>
                <div className="bg-[#020617] border border-gray-800 rounded-2xl p-4 space-y-3">

                    {logs.length === 0 && !loading && (
                        <div className="text-center text-gray-500 py-10">
                            Brak danych
                        </div>
                    )}

                    {logs.map((log, i) => {

                        const base = "p-3 rounded-xl text-sm border border-gray-800"

                        if (log.type === "plan") {
                            return <AgentLog key={i} base={base} log={log} icon={faBookReader} />
                        }

                        if (log.type === "action") {
                            return <AgentLog key={i} base={base} log={log} icon={faTools} />
                        }

                        if (log.type === "observation") {
                            return <AgentLog key={i} base={base} log={log} icon={faChartLine} />
                        }

                        if (log.type === "model_response") {
                            return <AgentLog key={i} base={base} log={log} icon={faRobot} />
                        }

                        if (log.type === "summary") {
                            return <AgentLog key={i} base={base} log={log} icon={faTriangleExclamation} />
                        }

                        if (log.type === "error") {
                            return <AgentLog key={i} base={base} log={log} icon={faXmark} />
                        }

                        return null
                    })}
                </div>

                {/* STATUS */}
                <div className="flex justify-between text-xs text-gray-500">
                    <span>Status: {loading ? "Running..." : "Idle"}</span>
                    <span>Logs: {logs.length}</span>
                </div>

            </div>
        </MainLayout>
    )
}

export default Home