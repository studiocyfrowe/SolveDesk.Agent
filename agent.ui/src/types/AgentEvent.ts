export type AgentEvent =
    | { type: "action"; tool: string; args?: any }
    | { type: "observation"; content: any }
    | { type: "final_answer"; content: string }
    | { type: "model_response"; content: string }
    | { type: "error"; content: string }