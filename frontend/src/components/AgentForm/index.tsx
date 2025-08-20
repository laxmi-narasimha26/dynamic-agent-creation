'use client';

import React, { useState } from 'react';
import { AgentFormProvider, useAgentForm } from './AgentFormContext';
import NameField from './NameField';
import DescriptionField from './DescriptionField';
import ToolsField from './ToolsField';
import SubmitButton from './SubmitButton';

interface AgentFormProps {
  onSubmit: (agent: { name: string; description: string; tools: string[] }) => void;
  initialData?: { name?: string; description?: string; tools?: string[] };
}

const AgentFormContent: React.FC<AgentFormProps> = ({ onSubmit, initialData }) => {
  const { state, setName, setDescription, setTools } = useAgentForm();
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      name: state.name,
      description: state.description,
      tools: state.tools
    });
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <NameField />
      <DescriptionField />
      <ToolsField />
      <SubmitButton />
    </form>
  );
};

const AgentForm: React.FC<AgentFormProps> = (props) => {
  return (
    <AgentFormProvider initialData={props.initialData}>
      <AgentFormContent {...props} />
    </AgentFormProvider>
  );
};

export default AgentForm;
