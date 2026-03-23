const RenderContent = (content: any) => {
    if (Array.isArray(content) && content.length > 0 && content[0].name) {
        return (
            <div className="space-y-1 text-gray-400">
                {content.map((proc: any, idx: number) => (
                    <div key={idx} className="flex justify-between">
                        <span>{proc.name}</span>
                        <span className="text-red-400 font-medium">
                            {proc.cpu_percent ?? proc.memory_mb ?? 0}%
                        </span>
                    </div>
                ))}
            </div>
        )
    }

    if (Array.isArray(content)) {
        return (
            <div className="space-y-1">
                {content.map((item, i) => (
                    <div key={i} className="text-gray-400 text-sm">
                        {typeof item === "object"
                            ? JSON.stringify(item)
                            : item}
                    </div>
                ))}
            </div>
        )
    }

    if (typeof content === "object") {
        return (
            <pre className="bg-black/40 p-3 rounded text-xs text-green-400 overflow-x-auto">
                {JSON.stringify(content, null, 2)}
            </pre>
        )
    }

    return <span>{String(content)}</span>
}

export default RenderContent