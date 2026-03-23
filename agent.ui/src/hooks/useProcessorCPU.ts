import { useEffect, useState } from "react"
import { ProcessorCPU } from "../interfaces/ProcessorCPU"

const useProcessorCPU = () => {
    const [data, setData] = useState<ProcessorCPU[]>([])
    const [loading, setLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)

    const fetchData = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8080/api/stats/cpu")

            if (!response.ok) {
                throw new Error("Błąd pobierania danych")
            }

            const json = await response.json()
            setData(json)
        } catch (err: any) {
            console.error(err)
            setError(err.message || "Unknown error")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()

        const interval = setInterval(() => {
            fetchData()
        }, 2500)

        return () => clearInterval(interval)
    }, [])

    return {
        data,
        loading,
        error
    }
}

export default useProcessorCPU