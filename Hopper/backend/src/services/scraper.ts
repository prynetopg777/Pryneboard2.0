import fs from "fs";
import path from "path";
import * as cheerio from "cheerio";

/**
 * Scrapes HTML from a given URL and saves it to the `data` folder.
 * 
 * @param url The URL to scrape
 * @param extractText If true, extracts and saves only the clean text instead of raw HTML.
 * @returns The absolute path where the file was saved
 */
export async function scrapeAndSave(url: string, extractText: boolean = false): Promise<string> {
    console.log(`Fetching: ${url}`);

    const response = await fetch(url, {
        headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
        }
    });
    
    if (!response.ok) {
        throw new Error(`Failed to fetch ${url}: ${response.status} ${response.statusText}`);
    }

    const contentType = response.headers.get("content-type") || "";
    let content = await response.text();
    let extension = ".html";

    // Auto-detect JSON response
    if (contentType.includes("application/json") || url.includes("format=json")) {
        try {
            content = JSON.stringify(JSON.parse(content), null, 2);
            extension = ".json";
        } catch (e) {
            console.warn("Warning: URL suggested JSON but content was not valid JSON.");
            extension = ".txt";
        }
    } else if (extractText) {
        const $ = cheerio.load(content);
        $("script, style, nav, footer, head").remove();
        content = $("body").text().replace(/\s+/g, " ").trim();
        extension = ".txt";
    }

    // Generate a safe filename based on the URL
    const urlObj = new URL(url);
    let safeName = urlObj.hostname + urlObj.pathname;
    // Replace non-alphanumeric characters with underscores
    safeName = safeName.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    // Trim trailing underscores
    safeName = safeName.replace(/_+$/, '');

    const filename = `${safeName || 'index'}${extension}`;

    // Ensure the `data` directory exists at the root of the project
    const dataDir = path.resolve(process.cwd(), "data");
    if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
    }

    const filePath = path.join(dataDir, filename);
    fs.writeFileSync(filePath, content, "utf-8");

    console.log(`Saved content to: ${filePath}`);
    return filePath;
}

// ==========================================
// CLI Execution (if run directly)
// ==========================================
if (require.main === module) {
    const url = process.argv[2];
    const extractText = process.argv.includes("--text");

    if (!url) {
        console.error("Usage: npx tsx src/services/scraper.ts <url> [--text]");
        process.exit(1);
    }

    scrapeAndSave(url, extractText).catch(console.error);
}
