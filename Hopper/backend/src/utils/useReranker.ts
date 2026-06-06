

export const useReranker = (namespace: string = "__default__") => {
 
    const RERANKER = {
        "__default__": true,
        "bir": true,
        "sss": true,
        "dost": false,
        "discord_daily": false,
        "snr": true
    } as Record<string, boolean>

    return RERANKER[namespace] || true
}