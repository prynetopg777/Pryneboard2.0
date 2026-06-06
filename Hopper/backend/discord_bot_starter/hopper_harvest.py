import discord
from discord import app_commands
from discord.ext import commands
import os
import re
import tempfile
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

date_pattern = re.compile(
    r'^(january|february|march|april|may|june|july|august|september|october|november|december|'
    r'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
    r'\s+\d{1,2}\s*,?\s*\d{4}',
    re.IGNORECASE | re.MULTILINE
)

numeric_date_pattern = re.compile(
    r'^\d{1,2}/\d{1,2}/\d{2,4}',
    re.MULTILINE
)

def split_message(content, author, timestamp, server, channel, report_type):
    chunks = []
    header_base = f"Server: {server} | Channel: #{channel} | Report-Type: {report_type}"

    lines = content.split('\n')

    def is_bullet(line):
        return bool(re.match(r'^\s*[\*\-•]', line))

    def is_date(line):
        clean = line.strip().replace('**', '')
        return bool(date_pattern.match(clean)) or bool(numeric_date_pattern.match(clean))

    def is_client_header(clean, next_lines):
        if not clean:
            return False
        if is_bullet(clean):
            return False
        if is_date(clean):
            return False
        if len(clean.split()) > 5:
            return False
        for nl in next_lines:
            if not nl.strip():
                continue
            if is_bullet(nl):
                return True
            else:
                return False
        return False

    segments = []
    current_date = timestamp
    current_client = None
    current_bullets = []

    i = 0
    while i < len(lines):
        line = lines[i]
        clean = line.strip().replace('**', '')
        next_lines = lines[i+1:i+4]

        if not clean:
            i += 1
            continue

        if is_date(clean):
            if current_bullets:
                segments.append((current_date, current_client, current_bullets))
                current_bullets = []
                current_client = None
            current_date = clean
            i += 1

        elif is_client_header(clean, next_lines):
            if current_bullets:
                segments.append((current_date, current_client, current_bullets))
                current_bullets = []
            current_client = clean
            i += 1

        elif is_bullet(line):
            current_bullets.append(line.strip())
            i += 1

        else:
            current_bullets.append(line.strip())
            i += 1

    if current_bullets:
        segments.append((current_date, current_client, current_bullets))

    for date, client, bullets in segments:
        client_label = f"\n{client}" if client else ""
        chunk_body = '\n'.join(bullets)
        chunks.append(
            f"{header_base} | Period: {date}\n"
            f"[{timestamp}] {author}:{client_label}\n{chunk_body}"
        )

    return chunks if chunks else [
        f"{header_base} | Period: {timestamp}\n"
        f"[{timestamp}] {author}:\n{content.strip()}"
    ]

@bot.event
async def on_ready():
    guild = discord.Object(id=1502185147855011942)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="scrape", description="Scrape and chunk messages from this channel for RAG ingestion straight to PineconeDB")
@app_commands.describe(
    message_limit="Number of Discord messages to fetch. Min: 1, Max: 2000, Default: 500.",
    custom_namespace="Pinecone namespace to ingest into. Allowed: letters, numbers, hyphens, underscores. Default: channel name."
)
async def scrape(interaction: discord.Interaction, message_limit: int = 500, custom_namespace: str = None):
    await interaction.response.defer(ephemeral=True)

    if message_limit < 1 or message_limit > 2000:
        await interaction.followup.send("❌ Limit must be between 1 and 2000.", ephemeral=True)
        return

    if custom_namespace and not re.match(r'^[a-zA-Z0-9_\-]+$', custom_namespace):
        await interaction.followup.send("❌ Namespace can only contain letters, numbers, hyphens, and underscores.", ephemeral=True)
        return

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"discord_{interaction.channel.name}.txt")

    channel_name = interaction.channel.name.lower()
    target_namespace = custom_namespace if custom_namespace else channel_name
    if "daily" in channel_name:
        report_type = "DAILY"
    elif "weekly" in channel_name:
        report_type = "WEEKLY"
    else:
        report_type = "GENERAL"

    count = 0
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            async for message in interaction.channel.history(limit=message_limit, oldest_first=True):
                if message.content and message.author != bot.user:
                    if not message.content.lower().startswith("!scrape"):
                        timestamp = message.created_at.strftime('%Y-%m-%d')
                        chunks = split_message(
                            message.content,
                            message.author.name,
                            timestamp,
                            interaction.guild.name,
                            interaction.channel.name,
                            report_type
                        )
                        for chunk in chunks:
                            f.write(f"{chunk}\n\n---\n\n")
                            count += 1

        await interaction.followup.send(
            f"✅ **Scrape Complete!**\n- Scraped `{count}` chunks\n- Starting RAG ingestion into namespace `{target_namespace}`...",
            file=discord.File(file_path),
            ephemeral=True
        )

        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        command = f'npx tsx src/index.ts ingest "{file_path}" "{target_namespace}"'

        process = await asyncio.create_subprocess_shell(
            command,
            cwd=backend_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            await interaction.followup.send(f"✅ **Ingestion Complete!** Data added to namespace `{target_namespace}`.", ephemeral=True)
        else:
            err_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
            await interaction.followup.send(f"❌ **Ingestion Failed!**\n```\n{err_msg[:1900]}\n```", ephemeral=True)

        os.remove(file_path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error during scrape: {e}", ephemeral=True)

bot.run(TOKEN)