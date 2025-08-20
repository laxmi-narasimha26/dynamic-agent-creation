import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ExecuteAgentPage from '@/app/agents/[id]/execute/page';

// Mock router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
  useSearchParams: () => ({
    get: jest.fn(),
  }),
}));

describe('ExecuteAgentPage', () => {
  it('renders the execute agent page title', () => {
    render(<ExecuteAgentPage />);
    
    expect(screen.getByText('Execute Agent')).toBeInTheDocument();
  });

  it('renders the query input field', () => {
    render(<ExecuteAgentPage />);
    
    expect(screen.getByLabelText('Query')).toBeInTheDocument();
  });

  it('renders the execute button', () => {
    render(<ExecuteAgentPage />);
    
    expect(screen.getByText('Execute')).toBeInTheDocument();
  });

  it('renders the back link', () => {
    render(<ExecuteAgentPage />);
    
    expect(screen.getByText('Back to Agents')).toBeInTheDocument();
  });
});
