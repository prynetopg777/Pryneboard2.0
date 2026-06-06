import express from "express";
import cors from "cors";
import { askQuestion } from "./index";
import { pc } from "./services/embedding";

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.post("/api/ask", async (req, res) => {
    const { question, history, namespace } = req.body;

    if (!question) {
        return res.status(400).json({ error: "Question is required" });
    }
    try {
        console.log(`Received question: ${question}`);
        const answer = await askQuestion(question, history ?? [], namespace ?? "__default__");
        res.json({ answer });
    } catch (error) {
        console.error("Error processing question:", error);
        res.status(500).json({ error: "Failed to process question" });
    }
});

app.get("/api/namespaces", async (req, res) => {
    try {
        const stats = await pc.index({ name: process.env.INDEX_NAME! }).describeIndexStats();
        const namespaces = Object.keys(stats.namespaces || {});
        res.json({ namespaces });
    } catch (error) {
        console.error("Error fetching namespaces:", error);
        res.status(500).json({ error: "Failed to fetch namespaces" });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});