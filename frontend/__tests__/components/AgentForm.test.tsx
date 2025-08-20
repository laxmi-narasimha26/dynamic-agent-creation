import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import AgentForm from '@/components/AgentForm';

// Mock router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe('AgentForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders correctly', () => {
    render(<AgentForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText('Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
    expect(screen.getByText('Tools')).toBeInTheDocument();
    expect(screen.getByText('Create Agent')).toBeInTheDocument();
  });

  it('allows filling in the form fields', () => {
    render(<AgentForm onSubmit={mockOnSubmit} />);
    
    const nameInput = screen.getByLabelText('Name');
    const descriptionInput = screen.getByLabelText('Description');
    
    fireEvent.change(nameInput, { target: { value: 'Test Agent' } });
    fireEvent.change(descriptionInput, { target: { value: 'A test agent for testing' } });
    
    expect(nameInput).toHaveValue('Test Agent');
    expect(descriptionInput).toHaveValue('A test agent for testing');
  });

  it('allows adding and removing tools', () => {
    render(<AgentForm onSubmit={mockOnSubmit} />);
    
    // Add a tool
    const toolSelect = screen.getByRole('combobox');
    const addButton = screen.getByText('Add');
    
    fireEvent.change(toolSelect, { target: { value: 'web_search' } });
    fireEvent.click(addButton);
    
    expect(screen.getByText('Web Search')).toBeInTheDocument();
    
    // Remove the tool
    const removeButton = screen.getByRole('button', { name: 'Remove' });
    fireEvent.click(removeButton);
    
    expect(screen.queryByText('Web Search')).not.toBeInTheDocument();
  });

  it('calls onSubmit when form is submitted', () => {
    render(<AgentForm onSubmit={mockOnSubmit} />);
    
    const nameInput = screen.getByLabelText('Name');
    const descriptionInput = screen.getByLabelText('Description');
    const form = screen.getByRole('form');
    
    fireEvent.change(nameInput, { target: { value: 'Test Agent' } });
    fireEvent.change(descriptionInput, { target: { value: 'A test agent for testing' } });
    
    fireEvent.submit(form);
    
    expect(mockOnSubmit).toHaveBeenCalledWith({
      name: 'Test Agent',
      description: 'A test agent for testing',
      tools: [],
    });
  });

  it('disables submit button when form is invalid', () => {
    render(<AgentForm onSubmit={mockOnSubmit} />);
    
    const submitButton = screen.getByText('Create Agent');
    
    expect(submitButton).toBeDisabled();
    
    const nameInput = screen.getByLabelText('Name');
    const descriptionInput = screen.getByLabelText('Description');
    
    fireEvent.change(nameInput, { target: { value: 'Test Agent' } });
    fireEvent.change(descriptionInput, { target: { value: 'A test agent for testing' } });
    
    expect(submitButton).not.toBeDisabled();
  });
});
