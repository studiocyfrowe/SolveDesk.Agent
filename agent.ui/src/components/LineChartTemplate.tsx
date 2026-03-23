import React from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'
import { ChartItem } from "../interfaces/ChartItem"

interface LineChartTemplateProps {
    data: ChartItem[]
}

const LineChartTemplate: React.FC<LineChartTemplateProps> = ({ data }) => {
    return (
        <LineChart
            style={{
                width: '100%',
                maxWidth: '700px',
                height: '100%',
                maxHeight: '70vh',
                aspectRatio: 1.618
            }}
            data={data}
        >
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-3)" />
            <XAxis dataKey="label" stroke="var(--color-text-3)" />
            <YAxis stroke="var(--color-text-3)" />

            <Tooltip />
            <Legend />

            <Line
                type="monotone"
                dataKey="data"
                stroke="#3b82f6"
            />
        </LineChart>
    )
}

export default LineChartTemplate