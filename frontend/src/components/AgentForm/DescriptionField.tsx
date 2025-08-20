'use client';

import React from 'react';
import { useAgentForm } from './AgentFormContext';

const DescriptionField = () => {
  const { state, setDescription } = useAgentForm();
  
  return (
    <div>
      <label htmlFor="description" className="block text-sm font-medium text-gray-700">
        Description
      </label>
      <textarea
        id="description"
        rows={3}
        value={state.description}
        onChange={(e) => setDescription(e.target.value)}
        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        required
      />
    </div>
  );
};

export default DescriptionField;
