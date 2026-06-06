import fs from "fs";
import crypto from "crypto";
import * as cheerio from "cheerio";
import { Document } from "@langchain/core/documents";
import { getIndex, getEmbedding } from "../services/embedding";

import { PDFParse } from "pdf-parse";

function splitText(text: string, chunkSize = 1000, chunkOverlap = 200): string[] {
    const chunks: string[] = [];
    let start = 0;
    while (start < text.length) {
        const end = Math.min(start + chunkSize, text.length);
        chunks.push(text.slice(start, end));
        start += chunkSize - chunkOverlap;
    }
    return chunks;
}

function toDocuments(chunks: string[], source: string): Document[] {
    return chunks.map((text, i) =>
        new Document({ pageContent: text, metadata: { source, chunk: i } })
    );
}

function loadJSON(path: string): Document[] {
    const raw = fs.readFileSync(path, "utf-8");
    const json = JSON.parse(raw);
    const text = typeof json === "string" ? json : JSON.stringify(json, null, 2);
    return [new Document({ pageContent: text, metadata: { source: path } })];
}

async function loadURL(url: string): Promise<Document[]> {
    const res = await fetch(url, {
        headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    });
    const html = await res.text();
    const $ = cheerio.load(html);
    $("script, style, nav, footer, head").remove();
    const text = $("body").text().replace(/\s+/g, " ").trim();
    return [new Document({ pageContent: text, metadata: { source: url } })];
}

export async function processFile(path: string): Promise<{ chunks: Document[]; hash: string }> {
    let docs: Document[] = [];

    if (path.endsWith(".pdf")) {
        const parser = new PDFParse({ data: fs.readFileSync(path) });
        try {
            const result = await parser.getText();
            docs = [new Document({ pageContent: result.text, metadata: { source: path } })];
        } finally {
            await parser.destroy();
        }
    } else if (path.endsWith(".json")) {
        docs = loadJSON(path);
    } else if (path.endsWith(".txt")) {
        const text = fs.readFileSync(path, "utf-8");
        if (path.includes("discord")) {
            const messages = text.split("---").map(m => m.trim()).filter(Boolean);
            docs = messages.map((msg, i) =>
                new Document({ pageContent: msg, metadata: { source: path, chunk: i } })
            );
        } else {
            docs = [new Document({ pageContent: text, metadata: { source: path } })];
        }
    } else if (path.startsWith("http")) {
        docs = await loadURL(path);
    } else {
        throw new Error("Unsupported file format or URL");
    }

    const fullContent = docs.map((doc) => doc.pageContent).join("\n");
    const hash = calculateHash(fullContent);

    const chunks = docs.flatMap((doc) => {
        if (doc.metadata.source?.toString().includes("discord")) {
            return [doc]; // already chunked by the harvest bot
        }
        return toDocuments(splitText(doc.pageContent, 1000, 200), doc.metadata.source);
    });

    return { chunks, hash };
}

/**
 * Calculates a SHA-256 hash of the given content string.
 */
export function calculateHash(content: string): string {
    return crypto.createHash("sha256").update(content).digest("hex");
}

/**
 * Checks if a document with the given content hash already exists in the database.
 * If no hash match is found, it fallbacks to a semantic search to check for identical content
 * (useful for documents ingested before the hashing system was implemented).
 */
export async function isDocumentDuplicate(contentHash: string, firstChunkText?: string, namespace?: string): Promise<boolean> {
    const currentIndex = getIndex(namespace);

    const hashQuery = await currentIndex.query({
        vector: Array(1024).fill(0),
        filter: { contentHash: { "$eq": contentHash } },
        topK: 1,
        includeMetadata: true
    });

    if (hashQuery.matches.length > 0) {
        return true;
    }

    if (firstChunkText) {
        const vector = await getEmbedding(firstChunkText, "passage");
        const simQuery = await currentIndex.query({
            vector,
            topK: 1,
            includeMetadata: true
        });

        if (simQuery.matches.length > 0) {
            const match = simQuery.matches[0];
            if (match.score !== undefined && match.score > 0.95) {
                const metadata = match.metadata as any;
                if (metadata?.text === firstChunkText) {
                    return true;
                }
            }
        }
    }

    return false;
}