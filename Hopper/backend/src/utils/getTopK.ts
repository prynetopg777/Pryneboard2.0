

export const getTopK = (namespace: string = "__default__"): number => {

    const TOP_K = {
        "__default__": 10,
        "bir": 8,
        "sss": 6,
        "dost": 5,
        "discord_daily": 5,
        "snr": 10
    } as Record<string, number>

    return TOP_K[namespace] || 5

}


export const getTopN = (namespace: string = "__default__"): number => {
    const TOP_N = {
        "__default__": 30,
        "bir": 20,
        "sss": 15,
        "dost": 15,
        "discord_daily": 10,
        "snr": 30
    } as Record<string, number>

    return TOP_N[namespace] || 20
}