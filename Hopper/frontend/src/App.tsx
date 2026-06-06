import { useState, useRef, useEffect } from 'react'
import { useContextStore } from './store/contextStore';
import parser from 'html-react-parser'

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hello! I'm Hopper, your helpful assistant. How can I help you today?",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [namespaces, setNamespaces] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const selectedNamespace = useContextStore((s) => s.selectedNamespace)
  const setSelectedNamespace = useContextStore((s) => s.setSelectedNamespace)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const fetchNamespaces = async () => {
      try {
        const PORT = import.meta.env.PORT || 3000;
        const res = await fetch(`http://localhost:${PORT}/api/namespaces`);
        const data = await res.json();
        setNamespaces(data.namespaces);
      } catch (error) {
        console.error('Failed to fetch namespaces:', error);
      }
    };
    fetchNamespaces();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const PORT = import.meta.env.PORT || 3000;

      const history = messages
        .filter((m) => m.id !== '1')
        .slice(-4) // Limit chat history to the last 10 messages
        .map(({ role, content }) => ({ role, content }));

      const response = await fetch(`http://localhost:${PORT}/api/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input, history, namespace: selectedNamespace }),
      });

      if (!response.ok) throw new Error('Failed to fetch response');

      const data = await response.json();

      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.answer,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: "Sorry, I encountered an error while trying to reach the server. Please make sure the backend is running.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto shadow-2xl bg-white dark:bg-slate-900 overflow-hidden sm:rounded-xl sm:my-4">
      {/* Header */}
      <header className="px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between glass sticky top-0 z-10">
        <div className="flex items-center justify-between w-full gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-indigo-200 dark:shadow-none">
              H
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-800 dark:text-white">Hopper</h1>
              <p className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">Document Assistant • Online</p>
            </div>
          </div>
          <select
            value={selectedNamespace}
            onChange={(e) => setSelectedNamespace(e.target.value)}
            className="px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {namespaces.map((namespace) => (
              <option key={namespace} value={namespace}>{namespace}</option>
            ))}
          </select>
        </div>
      </header>

      {/* Message List */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50 dark:bg-slate-950">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] px-5 py-3 rounded-2xl text-sm leading-relaxed shadow-sm ${message.role === 'user'
                ? 'bg-indigo-600 text-white rounded-br-none'
                : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 rounded-bl-none border border-slate-100 dark:border-slate-700'
                }`}
            >
              {parser(message.content)}

              <div
                className={`text-[10px] mt-2 opacity-60 ${message.role === 'user' ? 'text-right' : 'text-left'
                  }`}
              >
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-slate-800 px-5 py-3 rounded-2xl rounded-bl-none border border-slate-100 dark:border-slate-700 shadow-sm">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-slate-300 dark:bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-slate-300 dark:bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-slate-300 dark:bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <footer className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <form onSubmit={handleSubmit} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Hopper anything..."
            className="w-full px-5 py-4 pr-16 bg-slate-100 dark:bg-slate-800 border-none rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-slate-800 dark:text-white transition-all placeholder:text-slate-400 dark:placeholder:text-slate-500"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-md"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
          </button>
        </form>
        <p className="text-[10px] text-center mt-3 text-slate-400 dark:text-slate-600 font-medium tracking-tight">
          Hopper can make mistakes. Verify important info.
        </p>
      </footer>
    </div>
  );
}

export default App;