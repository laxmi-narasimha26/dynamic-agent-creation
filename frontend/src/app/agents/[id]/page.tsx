'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface Agent {
  id: string;
  name: string;
  description: string;
  tools: string[];
}

export default function AgentDetailPage() {
  const params = useParams<{ id: string }>();
  const id = typeof params?.id === 'string' ? params.id : Array.isArray(params?.id) ? params.id[0] : '';
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgent = async () => {
      try {
        const res = await fetch(`/api/agents/${id}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: Agent = await res.json();
        setAgent(data);
      } catch (e) {
        setError('Failed to load agent');
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchAgent();
  }, [id]);

  if (loading) return <div className="p-6">Loading...</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;
  if (!agent) return <div className="p-6">Agent not found</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">{agent.name}</h1>
        <p className="text-gray-700 mb-4">{agent.description}</p>
        <div className="mb-6 flex flex-wrap gap-2">
          {agent.tools?.map((tool, idx) => (
            <span key={idx} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              {tool}
            </span>
          ))}
        </div>
        <div className="flex gap-2">
          <Link href={`/agents/${agent.id}/execute`} className="px-4 py-2 bg-indigo-600 text-white rounded">Execute</Link>
          <Link href="/agents" className="px-4 py-2 border rounded">Back</Link>
        </div>
      </div>
    </div>
  );
}
