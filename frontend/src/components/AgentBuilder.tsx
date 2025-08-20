import React, { createContext, useState, useCallback, useMemo, useContext } from 'react';
import { useQuery } from '@tanstack/react-query';

const AgentBuilderContext = createContext(null);

export function AgentBuilder({ children, onSave }) {
  const [agent, setAgent] = useState({ name: '', description: '', tools: [] });

  const { data: availableTools = [] } = useQuery({ queryKey: ['tools'], queryFn: fetchAvailableTools });

  const updateAgent = useCallback((updates) => {
    setAgent((prev) => ({ ...prev, ...updates }));
  }, []);

  const isValid = useMemo(() => agent.name.length > 0 && agent.description.length > 0, [agent]);

  const contextValue = useMemo(() => ({ agent, updateAgent, availableTools, isValid }), [agent, updateAgent, availableTools, isValid]);

  return (
    <AgentBuilderContext.Provider value={contextValue}>
      <form onSubmit={(e) => {
        e.preventDefault();
        if (isValid) onSave(agent);
      }}>
        {children}
      </form>
    </AgentBuilderContext.Provider>
  );
}

export function BasicInfo() {
  const { agent, updateAgent } = useContext(AgentBuilderContext);
  return (
    <div className='space-y-4'>
      <input
        type='text'
        value={agent.name}
        onChange={(e) => updateAgent({ name: e.target.value })}
        placeholder='Agent name'
        className='border p-2 rounded w-full'
      />
      <textarea
        value={agent.description}
        onChange={(e) => updateAgent({ description: e.target.value })}
        placeholder='Agent description'
        className='border p-2 rounded w-full'
      />
    </div>
  );
}

export function ToolSelector() {
  const { agent, updateAgent, availableTools } = useContext(AgentBuilderContext);
  return (
    <div>
      <h3 className='font-semibold mb-2'>Available Tools</h3>
      <div className='grid grid-cols-2 gap-2'>
        {availableTools.map((tool) => (
          <label key={tool} className='inline-flex items-center space-x-2'>
            <input
              type='checkbox'
              checked={agent.tools.includes(tool)}
              onChange={() => {
                const newTools = agent.tools.includes(tool)
                  ? agent.tools.filter((t) => t !== tool)
                  : [...agent.tools, tool];
                updateAgent({ tools: newTools });
              }}
            />
            <span>{tool}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
