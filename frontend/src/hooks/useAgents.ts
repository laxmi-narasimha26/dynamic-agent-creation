import { useState, useEffect } from 'react';

interface Agent {
  id: string;
  name: string;
  description: string;
  tools: string[];
  createdAt?: string;
  updatedAt?: string;
}

interface UseAgentsReturn {
  agents: Agent[];
  loading: boolean;
  error: string | null;
  createAgent: (agent: Omit<Agent, 'id'>) => Promise<void>;
  updateAgent: (id: string, agent: Partial<Agent>) => Promise<void>;
  deleteAgent: (id: string) => Promise<void>;
}

export const useAgents = (): UseAgentsReturn => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await fetch('/api/agents');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data: Agent[] = await response.json();
        setAgents(data);
      } catch (err) {
        // Fallback to simulated data if backend is not reachable
        const fallback: Agent[] = [
          {
            id: '1',
            name: 'Research Assistant',
            description: 'Helps with research tasks',
            tools: ['web_search', 'summarizer'],
            createdAt: '2023-01-01T00:00:00Z',
            updatedAt: '2023-01-01T00:00:00Z',
          },
          {
            id: '2',
            name: 'Math Tutor',
            description: 'Assists with mathematical problems',
            tools: ['calculator'],
            createdAt: '2023-01-02T00:00:00Z',
            updatedAt: '2023-01-02T00:00:00Z',
          },
        ];
        setError('Backend not reachable, showing sample agents');
        setAgents(fallback);
      } finally {
        setLoading(false);
      }
    };
    fetchAgents();
  }, []);

  const createAgent = async (agent: Omit<Agent, 'id'>) => {
    try {
      const response = await fetch('/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(agent),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const newAgent: Agent = await response.json();
      setAgents([...agents, newAgent]);
    } catch (err) {
      setError('Failed to create agent');
      throw err;
    }
  };

  const updateAgent = async (id: string, agentUpdates: Partial<Agent>) => {
    try {
      // In a real app, this would be an API call
      // const response = await fetch(`/api/agents/${id}`, {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(agentUpdates),
      // });
      // const updatedAgent = await response.json();
      
      // Simulate API call
      setAgents(agents.map(agent => 
        agent.id === id 
          ? { ...agent, ...agentUpdates, updatedAt: new Date().toISOString() } 
          : agent
      ));
    } catch (err) {
      setError('Failed to update agent');
      throw err;
    }
  };

  const deleteAgent = async (id: string) => {
    try {
      // In a real app, this would be an API call
      // await fetch(`/api/agents/${id}`, { method: 'DELETE' });
      
      // Simulate API call
      setAgents(agents.filter(agent => agent.id !== id));
    } catch (err) {
      setError('Failed to delete agent');
      throw err;
    }
  };

  return {
    agents,
    loading,
    error,
    createAgent,
    updateAgent,
    deleteAgent,
  };
};
