import { useState } from "react"
import { AgentEvent } from "../types/AgentEvent"

const useRunAgent = () => {
    const [logs, setLogs] = useState<AgentEvent[]>([])
    const [loading, setLoading] = useState(false)

    const runAgent = async (query: string) => {
        setLogs([])
        setLoading(true)

        try {
            const response = await fetch("http://127.0.0.1:8080/api/diagnose", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    problem: query
                })
            })

            if (!response.body) {
                setLoading(false)
                return
            }

            const reader = response.body.getReader()
            const decoder = new TextDecoder()
            let buffer = ""

            while (true) {
                const { done, value } = await reader.read()
                if (done) break

                buffer += decoder.decode(value)
                const lines = buffer.split("\n")
                buffer = lines.pop() || ""

                for (const line of lines) {
                    if (!line.trim()) continue

                    try {
                        const json: AgentEvent = JSON.parse(line)
                        setLogs(prev => [...prev, json])
                    } catch (err) {
                        console.error("JSON parse error", err)
                    }
                }
            }
        } catch (err) {
            console.error("Request error:", err)
        } finally {
            setLoading(false)
        }
    }

    return {
        logs,
        loading,
        runAgent
    }
}

export default useRunAgent