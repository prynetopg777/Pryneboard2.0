/**
 * Knowledge Dashboard
 * Handles UI for ingestion and source management.
 */

export default class KnowledgeDashboard {
    constructor() {
        this.modal = document.getElementById('knowledge-dashboard');
        this.body = document.getElementById('knowledge-dashboard-body');
        document.getElementById('tool-knowledge-btn').addEventListener('click', () => this.open());
        document.getElementById('close-knowledge-dashboard').addEventListener('click', () => this.close());
    }

    open() {
        this.modal.classList.remove('hidden');
        this.loadSources();
    }

    close() {
        this.modal.classList.add('hidden');
    }

    async loadSources() {
        try {
            const resp = await fetch('/api/knowledge/sources');
            const data = await resp.json();
            this.renderSources(data.sources);
        } catch (e) {
            this.body.innerHTML = `Error: ${e.message}`;
        }
    }

    renderSources(sources) {
        if (!sources || !sources.length) {
            this.body.innerHTML = '<p>No sources indexed yet.</p>';
            return;
        }
        let html = '<ul>';
        sources.forEach(s => {
            html += `<li>${s.source_path || 'Unknown'} (${s.source_type || 'N/A'})</li>`;
        });
        html += '</ul>';
        this.body.innerHTML = html;
    }
}
