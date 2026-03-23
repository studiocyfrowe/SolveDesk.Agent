import React from "react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import {
    faRobot,
    faChartLine,
    faMicrochip,
    faMemory,
    faGear
} from "@fortawesome/free-solid-svg-icons"
import Navigation from "../components/Navigation"

const MainLayout = ({ children }: { children?: React.ReactNode }) => {
    return (
        <div className="min-h-screen bg-[#0f172a] text-gray-200 flex">
            <aside className="w-64 bg-[#020617] border-r border-gray-800 flex flex-col">
                <div className="p-5 border-b border-gray-800 flex items-center gap-3">
                    <FontAwesomeIcon icon={faRobot} className="text-blue-500 text-xl" />
                    <h1 className="text-lg font-semibold">Lumos AI</h1>
                </div>
                <Navigation/>
                <div className="p-4 border-t border-gray-800 text-xs text-gray-500">
                    Agent v1.0
                </div>
            </aside>

            <div className="flex-1 flex flex-col">

                <header className="h-16 bg-[#020617] border-b border-gray-800 flex items-center justify-between px-6">
                    <h2 className="text-sm text-gray-400">
                        AI Monitoring Agent
                    </h2>

                    <div className="flex items-center gap-4">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                        <span className="text-sm text-gray-400">Online</span>
                    </div>
                </header>

                <main className="flex-1 p-6 overflow-y-auto">
                    {children || (
                        <div className="text-center text-gray-500 mt-20">
                            <p className="text-lg">Welcome to Lumos</p>
                            <p className="text-sm">Your AI system monitoring dashboard</p>
                        </div>
                    )}
                </main>

                <footer className="h-10 bg-[#020617] border-t border-gray-800 flex items-center justify-between px-6 text-xs text-gray-500">
                    <span>© {new Date().getFullYear()} Lumos AI</span>
                    <span>Powered by AI Agent</span>
                </footer>
            </div>
        </div>
    )
}

export default MainLayout