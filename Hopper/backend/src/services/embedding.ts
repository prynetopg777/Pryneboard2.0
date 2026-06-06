import { Pinecone, type Index, type RecordMetadata } from "@pinecone-database/pinecone"




export const pc = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! })


const indexName = process.env.INDEX_NAME!
export const getIndex = (namespace?: string): Index<RecordMetadata> =>
    pc.index({ name: indexName, namespace: namespace || "__default__" })


export async function getEmbedding(text: string, inputType: "query" | "passage" = "query"): Promise<number[]> {
    const res = await pc.inference.embed({
        model: "multilingual-e5-large",
        inputs: [text],
        parameters: { inputType }
    })
    const embedding = res.data[0]
    if (embedding && "values" in embedding) {
        return embedding.values!
    }
    throw new Error("Failed to get dense embedding")
}


export async function upsertChunks(chunks: { id: string; text: string; metadata?: object }[], namespace?: string) {
    // Pinecone inference has a batch limit (usually 96). We'll process in chunks of 50 for safety.
    const batchSize = 50;

    for (let i = 0; i < chunks.length; i += batchSize) {
        const currentBatch = chunks.slice(i, i + batchSize);
        console.log(`Processing batch ${Math.floor(i / batchSize) + 1} of ${Math.ceil(chunks.length / batchSize)}...`);


        const embeddings = await pc.inference.embed({
            model: "multilingual-e5-large",
            inputs: currentBatch.map((c) => c.text),
            parameters: { inputType: "passage" },
        });


        const currentIndex = getIndex(namespace);

        await currentIndex.upsert({
            records: currentBatch.map((chunk, j) => ({
                id: chunk.id,
                values: (embeddings.data[j] as any).values!,
                metadata: { text: chunk.text, ...chunk.metadata },
            }))
        });
    }
}



