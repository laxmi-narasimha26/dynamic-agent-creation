import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import CreateAgentPage from '@/app/agents/create/page';

// Mock router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe('CreateAgentPage', () => {
  it('renders the create agent page title', () => {
    render(<CreateAgentPage />);
    
    expect(screen.getByText('Create New Agent')).toBeInTheDocument();
  });

  it('renders the agent form', () => {
    render(<CreateAgentPage />);
    
    expect(screen.getByLabelText('Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
    expect(screen.getByText('Tools')).toBeInTheDocument();
    expect(screen.getByText('Create Agent')).toBeInTheDocument();
  });

  it('renders the cancel link', () => {
    render(<CreateAgentPage />);
    
    expect(screen.getByText('Cancel')).toBeInTheDocument();
  });
});
