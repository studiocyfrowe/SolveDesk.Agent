export type AgentEvent =
    | { type: "plan"; tool: string; args?: any }
    | { type: "action"; tool: string; args?: any }
    | { type: "observation"; content: any }
    | { type: "summary"; content: string }
    | { type: "model_response"; content: string }
    | { type: "error"; content: string }