'use client';

import React, { useEffect, useState } from 'react';

interface Tool {
  id: string;
  name: string;
  description: string;
  parameters: string[];
}

export default function ToolsPage() {
  const [tools, setTools] = useState<Tool[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const [showLLMForm, setShowLLMForm] = useState(false);
  const [newToolCode, setNewToolCode] = useState('');
  const [newToolName, setNewToolName] = useState('');
  const [newToolDescription, setNewToolDescription] = useState('');
  // LLM tool (no-code) state
  const [llmName, setLlmName] = useState('');
  const [llmDescription, setLlmDescription] = useState('');

  const fetchTools = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/tools', { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      // data is a mapping: toolId -> { class, description, parameters }
      const items: Tool[] = Object.entries<any>(data).map(([id, meta]) => ({
        id,
        name: id.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
        description: meta.description || '',
        parameters: Array.isArray(meta.parameters) ? meta.parameters : [],
      }));
      setTools(items);
    } catch (e: any) {
      setError('Failed to load tools. Ensure backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterLLM = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const payload = { name: llmName.trim(), description: llmDescription.trim() };
      const endpoints = [
        '/api/tools/register_llm',
        '/api/tools/register_llm/',
        '/api/tools/register-llm',
        'http://127.0.0.1:8000/api/tools/register_llm',
        'http://127.0.0.1:8000/api/tools/register_llm/',
        'http://127.0.0.1:8000/api/tools/register-llm',
      ];
      let lastErr: string | null = null;
      let success = false;
      for (const url of endpoints) {
        try {
          const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });
          if (res.ok) { success = true; break; }
          let msg = `HTTP ${res.status}`;
          try { const j = await res.json(); if (j?.detail) msg = j.detail; } catch {}
          lastErr = `${url}: ${msg}`;
        } catch (err: any) {
          lastErr = `${url}: ${err?.message || err}`;
        }
      }
      if (!success) throw new Error(lastErr || 'Unknown error');
      await fetchTools();
      // reset
      setShowLLMForm(false);
      setLlmName('');
      setLlmDescription('');
    } catch (e: any) {
      setError(`Failed to register LLM tool: ${e?.message || e}`);
    }
  };

  useEffect(() => {
    fetchTools();
  }, []);

  const handleRegisterTool = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch('/api/tools/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool_name: newToolName.trim(), description: newToolDescription.trim(), code: newToolCode }),
      });
      if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try { 
          const j = await res.json(); 
          if (j?.detail) msg = j.detail; 
        } catch {} // Ignore if body is not JSON
        throw new Error(msg);
      }

      // Apply returned tools to avoid stale UI, then refresh in background
      try {
        const j = await res.json();
        if (j && j.tools) {
          const items: Tool[] = Object.entries<any>(j.tools).map(([id, meta]) => ({
            id,
            name: id.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
            description: meta.description || '',
            parameters: Array.isArray(meta.parameters) ? meta.parameters : [],
          }));
          setTools(items);
        }
      } catch {}
      // Also refresh list to be safe
      await fetchTools();
      // Reset form and hide it
      setNewToolCode('');
      setNewToolName('');
      setNewToolDescription('');
      setShowRegisterForm(false);
    } catch (e: any) {
      setError(`Failed to register tool: ${e?.message || e}`);
    }
  };

  const quickAddChatbot = async () => {
    // Pre-fill and submit an OpenAI-based chatbot function tool
    const name = 'chatbot_fn';
    const description = 'Lightweight OpenAI-powered chatbot (async function)';
    const code = [
      'async def chatbot_fn(query: str) -> str:',
      '    from openai import OpenAI',
      '    client = OpenAI()',
      '    resp = client.chat.completions.create(',
      '        model="gpt-4o-mini",',
      '        messages=[',
      '            {"role": "system", "content": "You are helpful and concise."},',
      '            {"role": "user", "content": query},',
      '        ],',
      '        temperature=0.2,',
      '    )',
      '    return (resp.choices[0].message.content or "").strip()',
    ].join('\n');

    setNewToolName(name);
    setNewToolDescription(description);
    setNewToolCode(code);

    try {
      const res = await fetch('/api/tools/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool_name: name, description, code }),
      });
      if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try { const j = await res.json(); if (j?.detail) msg = j.detail; } catch {}
        throw new Error(msg);
      }
      await fetchTools();
      setShowRegisterForm(false);
      setNewToolCode('');
      setNewToolName('');
      setNewToolDescription('');
    } catch (e: any) {
      setError(`Failed to quick-add chatbot: ${e?.message || e}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6 flex items-center justify-between gap-3 flex-wrap">
          <h1 className="text-2xl font-bold text-gray-900">Tools</h1>
          <div className="flex gap-2">
            <button 
              onClick={() => { setShowRegisterForm(!showRegisterForm); if (!showRegisterForm) setShowLLMForm(false); }}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {showRegisterForm ? 'Cancel' : 'Register Code Tool'}
            </button>
            <button 
              onClick={() => { setShowLLMForm(!showLLMForm); if (!showLLMForm) setShowRegisterForm(false); }}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {showLLMForm ? 'Cancel' : 'Create LLM Tool (no-code)'}
            </button>
          </div>
        </div>

        {showRegisterForm && (
          <div className="bg-white shadow sm:rounded-lg mb-6">
            <div className="px-6 py-5 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Register New Tool</h2>
            </div>
            <div className="px-6 py-5">
              <form onSubmit={handleRegisterTool} className="space-y-4">
                {error && (
                  <div className="text-sm text-red-600">{error}</div>
                )}
                <div>
                  <label htmlFor="toolName" className="block text-sm font-medium text-gray-700">
                    Tool Name
                  </label>
                  <input
                    type="text"
                    id="toolName"
                    value={newToolName}
                    onChange={(e) => setNewToolName(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="toolDescription" className="block text-sm font-medium text-gray-700">
                    Description
                  </label>
                  <input
                    type="text"
                    id="toolDescription"
                    value={newToolDescription}
                    onChange={(e) => setNewToolDescription(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="5-120 chars describing what the tool does"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="toolCode" className="block text-sm font-medium text-gray-700">
                    Tool Code (Python)
                  </label>
                  <textarea
                    id="toolCode"
                    rows={8}
                    value={newToolCode}
                    onChange={(e) => setNewToolCode(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm font-mono"
                    placeholder={'Enter Python code for your custom tool...\nExample (must be async):\nasync def reverse_string(text: str) -> str:\n    return text[::-1]'}
                    required
                  />
                  <p className="mt-1 text-xs text-gray-500">Tip: define an <strong>async</strong> function like <code>async def my_tool(text: str) -&gt; str:</code>. Avoid importing os/sys/subprocess. Name must match <code>{'^[a-zA-Z_][a-zA-Z0-9_]{2,30}$'}</code>.</p>
                </div>
                <div className="flex justify-between">
                  <button
                    type="button"
                    onClick={quickAddChatbot}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Quick Add: Chatbot
                  </button>
                  <button
                    type="submit"
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Register Tool
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {showLLMForm && (
          <div className="bg-white shadow sm:rounded-lg mb-6">
            <div className="px-6 py-5 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Create LLM Tool (no code)</h2>
            </div>
            <div className="px-6 py-5">
              <form onSubmit={handleRegisterLLM} className="space-y-4">
                {error && (
                  <div className="text-sm text-red-600">{error}</div>
                )}
                <div>
                  <label htmlFor="llmName" className="block text-sm font-medium text-gray-700">
                    Tool Name
                  </label>
                  <input
                    type="text"
                    id="llmName"
                    value={llmName}
                    onChange={(e) => setLlmName(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="llmDescription" className="block text-sm font-medium text-gray-700">
                    Description
                  </label>
                  <input
                    type="text"
                    id="llmDescription"
                    value={llmDescription}
                    onChange={(e) => setLlmDescription(e.target.value)}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="What should this tool do? (5-120 chars)"
                    required
                  />
                </div>
                <div>
                  <p className="mt-1 text-xs text-gray-500">This tool will accept a single parameter <code>input</code> when executed. The description is used as the system prompt.</p>
                </div>
                <div className="flex justify-end">
                  <button
                    type="submit"
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Create LLM Tool
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {loading && (
              <li className="px-6 py-4 text-sm text-gray-500">Loading tools...</li>
            )}
            {!loading && tools.map((tool) => (
              <li key={tool.id}>
                <div className="px-6 py-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <h2 className="text-lg font-medium text-gray-900">{tool.name}</h2>
                      <p className="text-sm text-gray-500">{tool.description}</p>
                      <div className="mt-2">
                        <span className="text-xs font-medium text-gray-500">Parameters:</span>
                        <div className="mt-1 flex flex-wrap gap-2">
                          {tool.parameters.map((param, index) => (
                            <span 
                              key={index} 
                              className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                            >
                              {param}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                    {/* Test button removed: tools are tested by attaching them to agents */}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
