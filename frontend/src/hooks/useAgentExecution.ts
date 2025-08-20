import { useState, useRef, useEffect } from 'react';

interface ExecutionStep {
  id: string;
  content: string;
  timestamp: number;
}

interface UseAgentExecutionReturn {
  isExecuting: boolean;
  executionResult: string | null;
  executionSteps: ExecutionStep[];
  executeAgent: (agentId: string, query: string) => void;
  stopExecution: () => void;
}

export const useAgentExecution = (): UseAgentExecutionReturn => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<string | null>(null);
  const [executionSteps, setExecutionSteps] = useState<ExecutionStep[]>([]);
  const eventSourceRef = useRef<EventSource | null>(null);

  const executeAgent = (agentId: string, query: string) => {
    if (isExecuting) return;
    
    setIsExecuting(true);
    setExecutionResult(null);
    setExecutionSteps([]);
    
    // Connect to real SSE endpoint exposed by backend
    // Next.js rewrite proxies /api -> http://localhost:8000
    const url = `/api/agents/${encodeURIComponent(agentId)}/stream?query=${encodeURIComponent(query)}`;
    const es = new EventSource(url);
    eventSourceRef.current = es;

    es.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        switch (data.type) {
          case 'message':
            setExecutionSteps(prev => [...prev, {
              id: `${Date.now()}-${prev.length}`,
              content: data.content,
              timestamp: data.timestamp ?? Date.now(),
            }]);
            break;
          case 'result':
            setExecutionResult(data.content);
            break;
          case 'complete':
            setIsExecuting(false);
            es.close();
            eventSourceRef.current = null;
            break;
          case 'error':
            console.error('Execution error:', data.message);
            setIsExecuting(false);
            es.close();
            eventSourceRef.current = null;
            break;
          default:
            break;
        }
      } catch (e) {
        // Some proxies may send comments/heartbeats; ignore JSON parse errors
      }
    };

    es.onerror = (error) => {
      console.error('SSE error:', error);
      setIsExecuting(false);
      try { es.close(); } catch {}
      eventSourceRef.current = null;
    };
  };

  const stopExecution = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setIsExecuting(false);
  };

  // Clean up event source on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return {
    isExecuting,
    executionResult,
    executionSteps,
    executeAgent,
    stopExecution
  };
};
