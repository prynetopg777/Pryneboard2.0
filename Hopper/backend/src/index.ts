import "dotenv/config";
import crypto from "crypto";
import { processFile, isDocumentDuplicate } from "./core/documentProcessor";
import { upsertChunks } from "./services/embedding";
import { querySimilar, querySimilarWithReranker } from "./core/retriever";
import { generateResponse, ChatHistoryEntry } from "./services/llm";
import { useReranker } from "./utils/useReranker"

/**
 * Ingests a document from a file path or URL, processes it into chunks,
 * and upserts the chunks into the vector database.
 * 
 * @param path - The file path (e.g., .pdf, .json) or URL to ingest
 */
export async function ingestDocument(path: string, namespace?: string) {
    console.log(`Processing document: ${path}...`);
    const { chunks: docs, hash } = await processFile(path);

    if (docs.length === 0) {
        console.log("No content extracted from the document.");
        return;
    }

    console.log("Checking if document already exists in database...");
    const firstChunkText = docs[0]?.pageContent;
    const isDuplicate = await isDocumentDuplicate(hash, firstChunkText, namespace);
    if (isDuplicate) {
        console.log("Document already exists in database. Skipping ingestion.");
        return;
    }

    const chunks = docs.map((doc) => ({
        id: crypto.randomUUID(),
        text: doc.pageContent,
        metadata: { ...doc.metadata, contentHash: hash }
    }));

    console.log(`Upserting ${chunks.length} chunks into vector database...`);
    await upsertChunks(chunks, namespace);
    console.log(`Successfully ingested ${chunks.length} chunks from ${path}`);
}

/**
 * Queries the vector database for context similar to the user's question,
 * and generates a response using the LLM.
 * 
 * @param question - The user's question
 */
export async function askQuestion(question: string, history: ChatHistoryEntry[] = [], namespace: string) {
    console.log(`\nSearching context for: "${question}"...`);

    const followUpPhrases = [
        "summarize that", "summarize this", "can u summarize", "can you summarize",
        "elaborate", "explain that", "explain more", "tell me more",
        "what do you mean", "expand on that", "clarify"
    ];

    const isFollowUp = followUpPhrases.some(phrase =>
        question.toLowerCase().includes(phrase)
    );

    if (isFollowUp) {
        console.log("Follow-up question detected, skipping Pinecone retrieval...");
        const lastAssistantMessage = [...history].reverse().find(m => m.role === "assistant");
        const context = lastAssistantMessage ? lastAssistantMessage.content : "";
        const answer = await generateResponse(question, context, history);
        console.log(`\nAnswer:\n${answer}\n`);
        return answer;
    }

    let matches;
    if (useReranker(namespace)) {
        matches = await querySimilarWithReranker(question, namespace);
    } else {
        matches = await querySimilar(question, namespace);
    }
    const contextLines = matches
        .map((match: any) => {
            const metadata = match.metadata as any;
            const text = metadata?.text || "";
            if (!text.trim()) return null;
            const source = metadata?.source || "unknown";
            const score = match.score ?? 0;
            const dataLabel = source.toLowerCase().includes("discord")
                ? "DISCORD CHAT LOG"
                : "FORMAL DOCUMENT";
            // Extract server/channel from chunk content if discord
            let displaySource = source;
            if (dataLabel === "DISCORD CHAT LOG") {
                const serverMatch = text.match(/Server:\s*([^|]+)/);
                const channelMatch = text.match(/Channel:\s*([^|]+)/);
                if (serverMatch && channelMatch) {
                    displaySource = `${serverMatch[1].trim()}: ${channelMatch[1].trim()}`;
                }
            }
            return `### DATA TYPE: ${dataLabel} | SOURCE: ${displaySource} | CONFIDENCE: ${score.toFixed(2)}\n${text}`;
        })
        .filter((entry: string | null): entry is string => entry !== null);
    const context = contextLines.join("\n\n");
    if (!context) {
        const fallbackMessage = "I could not find any relevant context to answer your question.";
        console.log(`\nAnswer: ${fallbackMessage}`);
        return fallbackMessage;
    }
    console.log("Generating response from LLM...");
    const answer = await generateResponse(question, context, history, namespace);

    console.log(`\nAnswer:\n${answer}\n`);
    return answer;
}

// ==========================================
// CLI Execution (if run directly)
// ==========================================
if (require.main === module) {
    const args = process.argv.slice(2);
    const command = args[0];
    const input = args[1];
    const namespace = args[2];

    if (command === "ingest" && input) {
        ingestDocument(input, namespace).catch(console.error);
    } else if (command === "ask" && input) {
        askQuestion(input, [], namespace).catch(console.error);
    } else {
        console.log(`
Usage:
  npx tsx src/index.ts ingest ../<path-or-url>
  npx tsx src/index.ts ask <your-question> <namespace>

Examples:
  npx tsx src/index.ts ingest https://example.com
  npx tsx src/index.ts ask "What is this document about?" __default__
        `);
    }
}
