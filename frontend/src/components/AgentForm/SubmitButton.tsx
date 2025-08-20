'use client';

import React from 'react';
import { useAgentForm } from './AgentFormContext';

const SubmitButton = () => {
  const { state } = useAgentForm();
  
  const isFormValid = state.name.trim() !== '' && state.description.trim() !== '';
  
  return (
    <div className="flex justify-end space-x-3">
      <button
        type="submit"
        disabled={!isFormValid}
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Create Agent
      </button>
    </div>
  );
};

export default SubmitButton;
