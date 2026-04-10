import React, { useEffect, useState } from "react"
import { AgentEvent } from "../types/AgentEvent"
import AgentLog from "./AgentLog"
import {
    faChartLine,
    faTools,
    faXmark,
    faBookReader
} from "@fortawesome/free-solid-svg-icons"

interface LogsContainerProps {
    logs: AgentEvent[]
    loading: boolean
}

// 🔥 typ dla summary (czytelniej)
type SummaryEvent = Extract<AgentEvent, { type: "summary" }>

const LogsContainer: React.FC<LogsContainerProps> = ({ logs, loading }) => {
    const base = "p-3 rounded-sm text-sm border border-gray-800 max-h-[50vh] overflow-y-scroll"

    // ✅ TYPE GUARD
    const summaryLog = logs.find(
        (log): log is SummaryEvent => log.type === "summary"
    )

    const filteredLogs = logs.filter(log => log.type !== "summary").reverse()

    const logConfig = {
        plan: {
            icon: faBookReader,
            label: "Plan działania"
        },
        action: {
            icon: faTools,
            label: "Akcja"
        },
        observation: {
            icon: faChartLine,
            label: "Obserwacja"
        },
        error: {
            icon: faXmark,
            label: "Błąd"
        }
    } as const

    // 🔥 STATE SolveDesk
    const [solutions, setSolutions] = useState<string[]>([])
    const [loadingSolutions, setLoadingSolutions] = useState(false)

    // 🌐 FETCH po pojawieniu się summary
    useEffect(() => {
        if (!summaryLog) return

        const fetchSolutions = async () => {
            try {
                setLoadingSolutions(true)

                const res = await fetch("https://localhost:60038/api/Issue/GetSearchResult", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6ImZjMjMzZmQxLTJlZjgtNGY0YS05MDBjLTI2NmI3MmE0OTM0OSIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiJ0ZXN0LnVzZXIiLCJleHAiOjE3NzUyOTI3MzYsImlzcyI6IlNvbHZlRGVzay5hcGkiLCJhdWQiOiJTb2x2ZURlc2sudXNlcnMifQ.WqC68Lp3fc8mUBl6nK7qQ-U9XQ99NqP8q_ebbFzNldw"
                    },
                    body: JSON.stringify({
                        query: summaryLog.content,
                        top_k: 3
                    })
                })

                const data = await res.json()

                setSolutions(data.explanation || "")
            } catch (err) {
                console.error("SolveDesk error:", err)
            } finally {
                setLoadingSolutions(false)
            }
        }

        fetchSolutions()
    }, [summaryLog])

    return (
        <div className="bg-[#020617] border border-gray-800 rounded-2xl p-4 flex flex-col space-y-4">

            {/* HEADER */}
            <div className="bg-green-900/30 border border-green-700 rounded-xl p-4">
                <div className="text-xs text-green-400 uppercase tracking-wide mb-1">
                    SolveDesk
                </div>
                <div>Item</div>
            </div>

            {/* 🔥 SOLVEDESK OUTPUT */}
            {summaryLog && (
                <div className="bg-green-900/30 border border-green-700 rounded-xl p-4">
                    <div className="text-xs text-green-400 uppercase tracking-wide mb-2">
                        Proponowane rozwiązania
                    </div>

                    {loadingSolutions ? (
                        <div className="text-gray-400 text-sm">Ładowanie...</div>
                    ) : solutions.length === 0 ? (
                        <div className="text-gray-500 text-sm">Brak rozwiązań</div>
                    ) : (
                        <ul className="list-disc pl-5 space-y-1 text-sm text-gray-200">
                            {solutions.map((s, i) => (
                                <li key={i}>{s}</li>
                            ))}
                        </ul>
                    )}
                </div>
            )}

            {summaryLog && (
                <div className="bg-green-900/30 border border-green-700 rounded-xl p-4">
                    <div className="text-xs text-green-400 uppercase tracking-wide mb-2">
                        Proponowane rozwiązania
                    </div>

                    <AgentLog
                            base={base}
                            log={summaryLog}
                            icon={faBookReader}
                        />
                </div>
            )}

            {/* BRAK DANYCH */}
            {logs.length === 0 && !loading && (
                <div className="text-center text-gray-500 py-10">
                    Brak danych
                </div>
            )}

            {/* LOGI */}
            {filteredLogs.map((log, i) => {
                const config = logConfig[log.type as keyof typeof logConfig]

                if (!config) return null

                return (
                    <div key={i} className="space-y-1">
                        <div className="text-xs text-gray-400 uppercase tracking-wide">
                            {config.label}
                        </div>

                        <AgentLog
                            base={base}
                            log={log}
                            icon={config.icon}
                        />
                    </div>
                )
            })}
        </div>
    )
}

export default LogsContainer