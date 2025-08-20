import { renderHook, act } from '@testing-library/react';
import { useAgents } from '@/hooks/useAgents';

describe('useAgents', () => {
  beforeEach(() => {
    // Reset the agents data
    const { result } = renderHook(() => useAgents());
    act(() => {
      result.current.setAgents([]);
    });
  });

  it('should initialize with empty agents array', () => {
    const { result } = renderHook(() => useAgents());
    
    expect(result.current.agents).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('should add a new agent', async () => {
    const { result } = renderHook(() => useAgents());
    
    const newAgent = {
      id: '1',
      name: 'Test Agent',
      description: 'A test agent',
      tools: ['web_search'],
      createdAt: new Date().toISOString(),
    };
    
    await act(async () => {
      await result.current.createAgent(newAgent);
    });
    
    expect(result.current.agents).toHaveLength(1);
    expect(result.current.agents[0]).toEqual(newAgent);
  });

  it('should fetch agents', async () => {
    const { result } = renderHook(() => useAgents());
    
    const agents = [
      {
        id: '1',
        name: 'Test Agent 1',
        description: 'First test agent',
        tools: ['web_search'],
        createdAt: new Date().toISOString(),
      },
      {
        id: '2',
        name: 'Test Agent 2',
        description: 'Second test agent',
        tools: ['calculator'],
        createdAt: new Date().toISOString(),
      },
    ];
    
    // Simulate adding agents first
    await act(async () => {
      await result.current.createAgent(agents[0]);
      await result.current.createAgent(agents[1]);
    });
    
    // Fetch agents
    let fetchedAgents;
    await act(async () => {
      fetchedAgents = await result.current.fetchAgents();
    });
    
    expect(fetchedAgents).toEqual(agents);
  });

  it('should get an agent by id', async () => {
    const { result } = renderHook(() => useAgents());
    
    const agent = {
      id: '1',
      name: 'Test Agent',
      description: 'A test agent',
      tools: ['web_search'],
      createdAt: new Date().toISOString(),
    };
    
    // Add the agent first
    await act(async () => {
      await result.current.createAgent(agent);
    });
    
    // Get the agent by id
    let fetchedAgent;
    await act(async () => {
      fetchedAgent = await result.current.getAgent('1');
    });
    
    expect(fetchedAgent).toEqual(agent);
  });

  it('should update an agent', async () => {
    const { result } = renderHook(() => useAgents());
    
    const agent = {
      id: '1',
      name: 'Test Agent',
      description: 'A test agent',
      tools: ['web_search'],
      createdAt: new Date().toISOString(),
    };
    
    // Add the agent first
    await act(async () => {
      await result.current.createAgent(agent);
    });
    
    // Update the agent
    const updatedAgent = { ...agent, name: 'Updated Agent' };
    await act(async () => {
      await result.current.updateAgent('1', updatedAgent);
    });
    
    expect(result.current.agents[0].name).toBe('Updated Agent');
  });

  it('should delete an agent', async () => {
    const { result } = renderHook(() => useAgents());
    
    const agent = {
      id: '1',
      name: 'Test Agent',
      description: 'A test agent',
      tools: ['web_search'],
      createdAt: new Date().toISOString(),
    };
    
    // Add the agent first
    await act(async () => {
      await result.current.createAgent(agent);
    });
    
    // Delete the agent
    await act(async () => {
      await result.current.deleteAgent('1');
    });
    
    expect(result.current.agents).toHaveLength(0);
  });
});
