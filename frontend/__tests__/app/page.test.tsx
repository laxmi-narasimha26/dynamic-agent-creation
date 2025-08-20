import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '@/app/page';

// Mock router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe('Home', () => {
  it('renders the dashboard title', () => {
    render(<Home />);
    
    expect(screen.getByText('Agent Dashboard')).toBeInTheDocument();
  });

  it('renders navigation cards', () => {
    render(<Home />);
    
    expect(screen.getByText('Create New Agent')).toBeInTheDocument();
    expect(screen.getByText('Manage Agents')).toBeInTheDocument();
    expect(screen.getByText('Tool Registry')).toBeInTheDocument();
  });

  it('renders sample agents section', () => {
    render(<Home />);
    
    expect(screen.getByText('Sample Agents')).toBeInTheDocument();
    expect(screen.getByText('Research Assistant')).toBeInTheDocument();
    expect(screen.getByText('Math Tutor')).toBeInTheDocument();
    expect(screen.getByText('Content Summarizer')).toBeInTheDocument();
  });

  it('renders execute links for sample agents', () => {
    render(<Home />);
    
    const executeLinks = screen.getAllByText('Execute');
    expect(executeLinks).toHaveLength(3);
  });
});
