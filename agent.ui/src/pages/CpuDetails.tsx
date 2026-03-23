import React from "react"
import MainLayout from "../layouts/MainLayout"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faChartDiagram } from "@fortawesome/free-solid-svg-icons"
import LineChartTemplate from "../components/LineChartTemplate"
import { ChartItem } from "../interfaces/ChartItem"
import { StatsMock } from "../mocks/StatsMock"
import { data } from "react-router-dom"
import useProcessorCPU from "../hooks/useProcessorCPU"

const CpuDetails = () => {
    const { data, loading, error } = useProcessorCPU()

    const chartData: ChartItem[] = data.map(p => ({
        label: p.Name,
        data: p.LoadPercent
    }))

    console.log(chartData)

    return (
        <MainLayout>
            <div className="max-w-5xl mx-auto space-y-6">
                <div className="bg-[#020617] border border-gray-800 rounded-2xl p-6 flex justify-between items-center">
                    <div>
                        <h1 className="text-lg font-semibold flex items-center gap-2">
                            <FontAwesomeIcon icon={faChartDiagram} className="text-blue-500" />
                            Procesor CPU
                        </h1>
                        <p className="text-sm text-gray-400">
                            Statystyki wydajności
                        </p>
                    </div>
                </div>
                <div className="bg-[#020617] border border-gray-800 rounded-2xl p-4 space-y-3">
                    <h3>charts</h3>
                    <LineChartTemplate data={chartData}/>
                </div>
            </div>
        </MainLayout>
    )
}

export default CpuDetails