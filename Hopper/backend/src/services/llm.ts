import { ChatGroq } from "@langchain/groq";
import { HumanMessage, AIMessage } from "@langchain/core/messages";
import { prompts } from "../core/prompts";

export interface ChatHistoryEntry {
    role: "user" | "assistant";
    content: string;
}

const model = new ChatGroq({
    model: "openai/gpt-oss-120b",
    apiKey: process.env.GROQ_API_KEY,
    temperature: 1.5,
    reasoningEffort: "low",
    maxTokens: undefined,
});

const promptSelector = (namespace: string) => {
    if (namespace.toLowerCase().includes("discord")) {
        return prompts.discord;
    }

    if (namespace.toLowerCase().includes("snr")) {
        return prompts.product;
    }

    return prompts.default;
}

export async function generateResponse(
    prompt: string,
    context: string,
    history: ChatHistoryEntry[] = [],
    namespace: string = "__default__"
) {
    if (!process.env.GROQ_API_KEY) {
        throw new Error("GROQ_API_KEY is not defined in environment variables");
    }

    const template = promptSelector(namespace);

    // Map history to BaseMessage objects (HumanMessage, AIMessage)
    const chatHistoryMessages = history.map((entry) =>
        entry.role === "user"
            ? new HumanMessage(entry.content)
            : new AIMessage(entry.content)
    );

    // Format the template with dynamic values
    const formattedMessages = await template.formatMessages({
        chat_history: chatHistoryMessages,
        context: context,
        question: prompt,
    });

    try {
        const result = await model.invoke(formattedMessages);
        return result.content.toString();
    } catch (error) {
        console.error("Error invoking Groq model:", error);
        throw new Error("Failed to generate response from LLM");
    }
}



