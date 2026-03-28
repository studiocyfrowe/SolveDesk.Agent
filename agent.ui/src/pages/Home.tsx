import React, { useState } from "react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import MainLayout from "../layouts/MainLayout"
import RunAgent from "../services/RunAgent"
import { faPlay, faRobot } from "@fortawesome/free-solid-svg-icons"
import LogsContainer from "../components/LogsContainer"
import StatusComponent from "../components/StatusComponent"

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
                        {loading ? "Running..." : "Start"}
                    </button>
                </div>
                {loading && <StatusComponent logs={logs} loading={loading}/>}
                <LogsContainer logs={logs} loading={loading}/>
            </div>
        </MainLayout>
    )
}

export default Home