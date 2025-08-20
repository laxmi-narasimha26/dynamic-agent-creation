'use client';

import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface AgentFormState {
  name: string;
  description: string;
  tools: string[];
}

type AgentFormAction =
  | { type: 'SET_NAME'; payload: string }
  | { type: 'SET_DESCRIPTION'; payload: string }
  | { type: 'SET_TOOLS'; payload: string[] }
  | { type: 'ADD_TOOL'; payload: string }
  | { type: 'REMOVE_TOOL'; payload: string };

interface AgentFormContextType {
  state: AgentFormState;
  setName: (name: string) => void;
  setDescription: (description: string) => void;
  setTools: (tools: string[]) => void;
  addTool: (tool: string) => void;
  removeTool: (tool: string) => void;
}

const AgentFormContext = createContext<AgentFormContextType | undefined>(undefined);

const initialState: AgentFormState = {
  name: '',
  description: '',
  tools: [],
};

function agentFormReducer(state: AgentFormState, action: AgentFormAction): AgentFormState {
  switch (action.type) {
    case 'SET_NAME':
      return { ...state, name: action.payload };
    case 'SET_DESCRIPTION':
      return { ...state, description: action.payload };
    case 'SET_TOOLS':
      return { ...state, tools: action.payload };
    case 'ADD_TOOL':
      if (!state.tools.includes(action.payload)) {
        return { ...state, tools: [...state.tools, action.payload] };
      }
      return state;
    case 'REMOVE_TOOL':
      return { ...state, tools: state.tools.filter(tool => tool !== action.payload) };
    default:
      return state;
  }
}

export const AgentFormProvider: React.FC<{ 
  children: ReactNode; 
  initialData?: Partial<AgentFormState> 
}> = ({ children, initialData }) => {
  const [state, dispatch] = useReducer(agentFormReducer, {
    ...initialState,
    ...initialData
  });

  const setName = (name: string) => dispatch({ type: 'SET_NAME', payload: name });
  const setDescription = (description: string) => dispatch({ type: 'SET_DESCRIPTION', payload: description });
  const setTools = (tools: string[]) => dispatch({ type: 'SET_TOOLS', payload: tools });
  const addTool = (tool: string) => dispatch({ type: 'ADD_TOOL', payload: tool });
  const removeTool = (tool: string) => dispatch({ type: 'REMOVE_TOOL', payload: tool });

  return (
    <AgentFormContext.Provider value={{
      state,
      setName,
      setDescription,
      setTools,
      addTool,
      removeTool
    }}>
      {children}
    </AgentFormContext.Provider>
  );
};

export const useAgentForm = () => {
  const context = useContext(AgentFormContext);
  if (!context) {
    throw new Error('useAgentForm must be used within an AgentFormProvider');
  }
  return context;
};
