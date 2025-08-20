import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import AgentsPage from '@/app/agents/page';

// Mock router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe('AgentsPage', () => {
  it('renders the agents page title', () => {
    render(<AgentsPage />);
    
    expect(screen.getByText('Agent Management')).toBeInTheDocument();
  });

  it('renders the create agent button', () => {
    render(<AgentsPage />);
    
    expect(screen.getByText('Create New Agent')).toBeInTheDocument();
  });

  it('renders sample agents', () => {
    render(<AgentsPage />);
    
    expect(screen.getByText('Research Assistant')).toBeInTheDocument();
    expect(screen.getByText('Math Tutor')).toBeInTheDocument();
    expect(screen.getByText('Content Summarizer')).toBeInTheDocument();
  });

  it('renders execute and edit links for each agent', () => {
    render(<AgentsPage />);
    
    const executeLinks = screen.getAllByText('Execute');
    const editLinks = screen.getAllByText('Edit');
    
    expect(executeLinks).toHaveLength(3);
    expect(editLinks).toHaveLength(3);
  });
});
