import fs from "fs";
import path from "path";
import { PDFParse } from "pdf-parse";

/**
 * Scrapes text from a PDF file and saves it to the `data` folder as a .txt file.
 * 
 * @param relativePath Path to the PDF file relative to the project root
 * @returns The absolute path where the extracted text was saved
 */
export async function scrapePDF(relativePath: string): Promise<string> {
    const absolutePath = path.resolve(process.cwd(), relativePath);
    
    if (!fs.existsSync(absolutePath)) {
        throw new Error(`File not found: ${absolutePath}`);
    }

    const dataBuffer = fs.readFileSync(absolutePath);
    
    console.log(`Parsing PDF: ${absolutePath}`);
    
    const parser = new PDFParse({ data: dataBuffer });
    try {
        const result = await parser.getText();
        const content = result.text;

        // Generate a safe filename
        const baseName = path.basename(relativePath, path.extname(relativePath));
        const safeName = baseName.replace(/[^a-z0-9]/gi, '_').toLowerCase();
        const filename = `${safeName}.txt`;

        const dataDir = path.resolve(process.cwd(), "data");
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }

        const savePath = path.join(dataDir, filename);
        fs.writeFileSync(savePath, content, "utf-8");

        console.log(`Saved extracted text to: ${savePath}`);
        return savePath;
    } catch (error: any) {
        throw new Error(`Failed to parse PDF: ${error.message}`);
    } finally {
        await parser.destroy();
    }
}

// ==========================================
// CLI Execution (if run directly)
// ==========================================
if (require.main === module) {
    const filePath = process.argv[2];

    if (!filePath) {
        console.error("Usage: npx tsx src/services/pdfScraper.ts <path-to-pdf>");
        process.exit(1);
    }

    scrapePDF(filePath).catch((err) => {
        console.error(err);
        process.exit(1);
    });
}
