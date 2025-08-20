'use client';

import React, { useState } from 'react';
import { useAgentForm } from './AgentFormContext';

const ToolsField = () => {
  const { state, addTool, removeTool } = useAgentForm();
  const [selectedTool, setSelectedTool] = useState('');

  const availableTools = [
    { id: 'web_search', name: 'Web Search' },
    { id: 'calculator', name: 'Calculator' },
    { id: 'summarizer', name: 'Text Summarizer' },
  ];

  const handleAddTool = () => {
    if (selectedTool && !state.tools.includes(selectedTool)) {
      addTool(selectedTool);
      setSelectedTool('');
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">
        Tools
      </label>
      <div className="mt-2 flex">
        <select
          value={selectedTool}
          onChange={(e) => setSelectedTool(e.target.value)}
          className="block flex-1 border border-gray-300 rounded-l-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
          <option value="">Select a tool</option>
          {availableTools.map((tool) => (
            <option key={tool.id} value={tool.id}>
              {tool.name}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={handleAddTool}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-r-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Add
        </button>
      </div>

      {state.tools.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {state.tools.map((toolId) => {
            const tool = availableTools.find(t => t.id === toolId);
            return (
              <span 
                key={toolId} 
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
              >
                {tool?.name || toolId}
                <button
                  type="button"
                  onClick={() => removeTool(toolId)}
                  className="flex-shrink-0 ml-1 h-4 w-4 rounded-full inline-flex items-center justify-center text-indigo-400 hover:bg-indigo-200 hover:text-indigo-500 focus:outline-none focus:bg-indigo-500 focus:text-white"
                >
                  <span className="sr-only">Remove</span>
                  <svg className="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                    <path strokeLinecap="round" strokeWidth="1.5" d="M1 1l6 6m0-6L1 7" />
                  </svg>
                </button>
              </span>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ToolsField;
