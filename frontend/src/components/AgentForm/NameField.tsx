'use client';

import React from 'react';
import { useAgentForm } from './AgentFormContext';

const NameField = () => {
  const { state, setName } = useAgentForm();
  
  return (
    <div>
      <label htmlFor="name" className="block text-sm font-medium text-gray-700">
        Name
      </label>
      <input
        type="text"
        id="name"
        value={state.name}
        onChange={(e) => setName(e.target.value)}
        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        required
      />
    </div>
  );
};

export default NameField;
