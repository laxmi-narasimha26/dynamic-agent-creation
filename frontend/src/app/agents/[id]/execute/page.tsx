'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { useAgentExecution } from '@/hooks/useAgentExecution';

export default function ExecuteAgentPage() {
  const params = useParams();
  const agentId = params.id as string;
  const [query, setQuery] = useState('');
  const { isExecuting, executionResult, executionSteps, executeAgent, stopExecution } = useAgentExecution();

  const handleExecute = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    executeAgent(agentId, query);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Execute Agent</h1>
          <p className="mt-1 text-sm text-gray-500">Agent ID: {agentId}</p>
        </div>

        <div className="bg-white shadow sm:rounded-lg mb-6">
          <div className="px-6 py-5 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Query</h2>
          </div>
          <div className="px-6 py-5">
            <form onSubmit={handleExecute} className="space-y-4">
              <div>
                <label htmlFor="query" className="block text-sm font-medium text-gray-700">
                  Enter your query
                </label>
                <textarea
                  id="query"
                  rows={3}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="What would you like the agent to help you with?"
                  required
                  disabled={isExecuting}
                />
              </div>
              <div className="flex justify-end space-x-3">
                {isExecuting && (
                  <button
                    type="button"
                    onClick={stopExecution}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    Stop
                  </button>
                )}
                <button
                  type="submit"
                  disabled={isExecuting || !query.trim()}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isExecuting ? 'Executing...' : 'Execute Agent'}
                </button>
              </div>
            </form>
          </div>
        </div>

        {(executionSteps.length > 0 || executionResult) && (
          <div className="bg-white shadow sm:rounded-lg">
            <div className="px-6 py-5 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Execution Trace</h2>
            </div>
            <div className="px-6 py-5">
              <div className="space-y-4">
                {executionSteps.map((step) => (
                  <div key={step.id} className="flex items-start">
                    <div className="flex-shrink-0 h-5 w-5 rounded-full bg-indigo-100 flex items-center justify-center">
                      <div className="h-2 w-2 rounded-full bg-indigo-600"></div>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm text-gray-700">{step.content}</p>
                    </div>
                  </div>
                ))}
                
                {executionResult && (
                  <div className="pt-4 border-t border-gray-200">
                    <h3 className="text-md font-medium text-gray-900 mb-2">Result</h3>
                    <div className="text-sm text-gray-700 bg-gray-50 p-4 rounded-md whitespace-pre-wrap">
                      {executionResult}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
