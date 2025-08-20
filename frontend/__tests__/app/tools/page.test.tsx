import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ToolsPage from '@/app/tools/page';

// Mock router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe('ToolsPage', () => {
  it('renders the tools page title', () => {
    render(<ToolsPage />);
    
    expect(screen.getByText('Tool Registry')).toBeInTheDocument();
  });

  it('renders prebuilt tools', () => {
    render(<ToolsPage />);
    
    expect(screen.getByText('Web Search')).toBeInTheDocument();
    expect(screen.getByText('Calculator')).toBeInTheDocument();
    expect(screen.getByText('Text Summarizer')).toBeInTheDocument();
  });

  it('renders the register new tool form', () => {
    render(<ToolsPage />);
    
    expect(screen.getByText('Register New Tool')).toBeInTheDocument();
    expect(screen.getByLabelText('Tool Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Tool Code')).toBeInTheDocument();
    expect(screen.getByText('Register Tool')).toBeInTheDocument();
  });

  it('renders the test tools section', () => {
    render(<ToolsPage />);
    
    expect(screen.getByText('Test Tools')).toBeInTheDocument();
  });
});
