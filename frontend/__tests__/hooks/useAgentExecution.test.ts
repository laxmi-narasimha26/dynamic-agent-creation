import { renderHook, act } from '@testing-library/react';
import { useAgentExecution } from '@/hooks/useAgentExecution';

describe('useAgentExecution', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should initialize with correct default values', () => {
    const { result } = renderHook(() => useAgentExecution());
    
    expect(result.current.isExecuting).toBe(false);
    expect(result.current.executionResult).toBeNull();
    expect(result.current.executionSteps).toEqual([]);
  });

  it('should execute agent and update state', async () => {
    const { result } = renderHook(() => useAgentExecution());
    
    // Start execution
    act(() => {
      result.current.executeAgent('agent-1', 'Test query');
    });
    
    expect(result.current.isExecuting).toBe(true);
    expect(result.current.executionResult).toBeNull();
    expect(result.current.executionSteps).toEqual([]);
    
    // Advance timers to simulate execution
    await act(async () => {
      jest.advanceTimersByTime(3000);
    });
    
    expect(result.current.isExecuting).toBe(false);
    expect(result.current.executionResult).not.toBeNull();
    expect(result.current.executionSteps).toHaveLength(6);
  });

  it('should not start execution if already executing', async () => {
    const { result } = renderHook(() => useAgentExecution());
    
    // Start execution
    act(() => {
      result.current.executeAgent('agent-1', 'Test query');
    });
    
    // Try to start another execution
    act(() => {
      result.current.executeAgent('agent-1', 'Another query');
    });
    
    // Only the first execution should be running
    expect(result.current.isExecuting).toBe(true);
    
    // Advance timers
    await act(async () => {
      jest.advanceTimersByTime(3000);
    });
    
    // Execution should complete
    expect(result.current.isExecuting).toBe(false);
  });

  it('should stop execution when stopExecution is called', async () => {
    const { result } = renderHook(() => useAgentExecution());
    
    // Start execution
    act(() => {
      result.current.executeAgent('agent-1', 'Test query');
    });
    
    expect(result.current.isExecuting).toBe(true);
    
    // Stop execution
    act(() => {
      result.current.stopExecution();
    });
    
    expect(result.current.isExecuting).toBe(false);
  });

  it('should clean up event source on unmount', () => {
    const { result, unmount } = renderHook(() => useAgentExecution());
    
    // Mock event source
    const mockClose = jest.fn();
    result.current['eventSourceRef'].current = { close: mockClose } as any;
    
    // Unmount the hook
    unmount();
    
    // Event source should be closed
    expect(mockClose).toHaveBeenCalled();
  });
});
