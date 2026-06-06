import { getEmbedding, getIndex, pc } from "../services/embedding";
import { getTopK, getTopN } from "../utils/getTopK"

export async function querySimilar(text: string, namespace: string) {
    const vector = await getEmbedding(text)
    const currentIndex = getIndex(namespace)
    const results = await currentIndex.query({ vector, topK: getTopK(namespace), includeMetadata: true })
    return results.matches
}

export async function querySimilarWithReranker(text: string, namespace?: string) {
    const vector = await getEmbedding(text)
    const currentIndex = getIndex(namespace)
    const candidateK = Math.max(getTopK(namespace) * 10, 50);
    const results = await currentIndex.query({ vector, topK: candidateK, includeMetadata: true })
    const matches = results.matches;
    if (matches.length === 0) return [];

    // Rerank the candidates using Pinecone's built-in reranker
    // We pass the metadata 'text' field for reranking
    const reranked = await pc.inference.rerank({
        model: "bge-reranker-v2-m3",
        query: text,
        documents: matches.map(m => (m.metadata as any)?.text || ""),
        topN: getTopN(namespace),
        returnDocuments: false // We already have the metadata in 'matches'
    });

    // Map reranked indices back to original matches and update scores
    const finalResults = reranked.data.map(item => {
        const originalMatch = matches[item.index];
        return {
            ...originalMatch,
            score: item.score // Use the reranker score
        };
    });

    return finalResults;
}