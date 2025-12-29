import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Loader2, AlertCircle, ArrowLeft, Download, Sparkles, CheckCircle2 } from 'lucide-react';
import { getRun, exportMarkdownUrl, submitFeedback } from '../lib/api';
import type { RunState } from '../lib/api';
import { ReportView } from '../components/ReportView';
import { InterviewForm } from '../components/InterviewForm';

const STEPS = [
  { id: 'interview', label: 'Initial Assessment', desc: 'Formulating clarifying questions', agents: ['InterviewerAgent'] },
  { id: 'plan', label: 'Strategic Planning', desc: 'Structuring the analysis plan', agents: ['PlannerAgent'] },
  { id: 'market', label: 'Market Research', desc: 'Analyzing market trends and audience', agents: ['MarketAgent', 'AudienceInsightAgent', 'CompetitorScanAgent'] },
  { id: 'risk', label: 'Risk Assessment', desc: 'Identifying potential risks and pitfalls', agents: ['RiskAgent'] },
  { id: 'execution', label: 'Execution Planning', desc: 'Drafting execution roadmap', agents: ['ExecutionAgent'] },
  { id: 'evaluation', label: 'Review & Verdict', desc: 'Finalizing verdict and recommendations', agents: ['JudgeAgent', 'InterviewEvaluatorAgent'] },
];

export function RunView() {
  const { runId } = useParams<{ runId: string }>();
  const [run, setRun] = useState<RunState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [polling, setPolling] = useState(true);

  useEffect(() => {
    if (!runId) return;

    let intervalId: ReturnType<typeof setInterval>;

    const fetchRun = async () => {
      try {
        const data = await getRun(runId);
        setRun(data);

        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          setPolling(false);
        }
        // If waiting for input, we can stop polling until they submit
        if (data.status === 'WAITING_FOR_INPUT') {
             setPolling(false);
        }
      } catch (err) {
        console.error(err);
        setError('Failed to load analysis.');
        setPolling(false);
      }
    };

    fetchRun();

    if (polling) {
      intervalId = setInterval(fetchRun, 2000);
    }

    return () => clearInterval(intervalId);
  }, [runId, polling]);

  const handleInterviewSubmit = async (answers: Record<string, string>) => {
      if (!runId) return;
      await submitFeedback(runId, answers);
      // Resume polling
      setPolling(true);
      // Optimistically update status to show loading
      setRun(prev => prev ? { ...prev, status: 'RUNNING' } : null);
  };

  const getStepStatus = (stepAgents: string[]) => {
    if (!run?.events) return 'pending';
    
    const started = run.events.some(e => e.type === 'AGENT_STARTED' && e.agent && stepAgents.includes(e.agent));
    const finished = run.events.some(e => e.type === 'AGENT_FINISHED' && e.agent && stepAgents.includes(e.agent));
    
    // Special case for interview: if waiting for input, it's current (or completed phase 1)
    if (stepAgents.includes('InterviewerAgent') && run.status === 'WAITING_FOR_INPUT') {
        return 'completed';
    }

    if (finished) return 'completed';
    if (started) return 'current';
    return 'pending';
  };

  // Determine the active step index to show progress
  const activeStepIndex = STEPS.findIndex(step => getStepStatus(step.agents) === 'current');
  const lastCompletedIndex = STEPS.map(step => getStepStatus(step.agents)).lastIndexOf('completed');
  const currentDisplayIndex = activeStepIndex !== -1 ? activeStepIndex : (lastCompletedIndex !== -1 ? lastCompletedIndex + 1 : 0);


  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Analysis</h2>
        <p className="text-gray-600 mb-6">{error}</p>
        <Link to="/" className="text-indigo-600 hover:underline font-medium">
          Return Home
        </Link>
      </div>
    );
  }

  if (!run) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <Loader2 className="w-12 h-12 text-indigo-600 animate-spin mb-4" />
        <p className="text-gray-600 font-medium">Loading...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-gray-500 hover:text-gray-900 transition-colors">
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>
        
        {run.status === 'COMPLETED' && (
          <a 
            href={exportMarkdownUrl(run.run_id)} 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
          >
            <Download className="w-4 h-4" />
            Export Markdown
          </a>
        )}
      </div>

      {run.status === 'STARTED' || run.status === 'RUNNING' || run.status === 'QUEUED' ? (
        <div className="bg-white p-12 rounded-3xl shadow-xl border border-slate-100 text-center max-w-3xl mx-auto relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 animate-gradient-x"></div>
          
          <div className="relative w-32 h-32 mx-auto mb-10">
            <div className="absolute inset-0 border-4 border-indigo-50 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-indigo-600 rounded-full border-t-transparent animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <Sparkles className="w-12 h-12 text-indigo-600 animate-pulse" />
            </div>
          </div>
          
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Analyzing Your Idea</h2>
          <p className="text-slate-500 mb-8 text-lg max-w-lg mx-auto">
            Our AI agents are researching the market, identifying competitors, and assessing risks. This usually takes 1-2 minutes.
          </p>

          <div className="flex justify-center gap-2 mb-8">
            <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
            <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
          </div>

          <div className="max-w-md mx-auto space-y-3 text-left">
            {STEPS.map((step, index) => {
               const status = getStepStatus(step.agents);
               // If we are past this step, mark as completed
               const isPast = index < currentDisplayIndex;
               const displayStatus = isPast ? 'completed' : (index === currentDisplayIndex ? 'current' : 'pending');
               
               // Override logic: if status is explicitly completed, use it
               const finalStatus = status === 'completed' ? 'completed' : displayStatus;

               return (
                <div key={step.id} className={`flex items-center gap-3 p-3 rounded-xl transition-all duration-500 ${
                  finalStatus === 'current' 
                    ? 'bg-indigo-50 border border-indigo-100 shadow-sm scale-105' 
                    : finalStatus === 'completed'
                    ? 'opacity-50'
                    : 'opacity-30'
                }`}>
                  <div className="shrink-0">
                    {finalStatus === 'completed' ? (
                      <CheckCircle2 className="w-5 h-5 text-green-600" />
                    ) : finalStatus === 'current' ? (
                      <Loader2 className="w-5 h-5 text-indigo-600 animate-spin" />
                    ) : (
                      <div className="w-5 h-5 rounded-full border-2 border-slate-300" />
                    )}
                  </div>
                  <div>
                    <h3 className={`text-sm font-bold ${
                      finalStatus === 'current' ? 'text-indigo-900' : 'text-slate-700'
                    }`}>
                      {step.label}
                    </h3>
                    {finalStatus === 'current' && (
                      <p className="text-xs text-indigo-700">{step.desc}</p>
                    )}
                  </div>
                </div>
               );
            })}
          </div>
        </div>
      ) : run.status === 'WAITING_FOR_INPUT' && run.interview ? (
        <InterviewForm interview={run.interview} onSubmit={handleInterviewSubmit} />
      ) : run.status === 'FAILED' ? (
        <div className="bg-red-50 p-12 rounded-3xl border border-red-100 text-center max-w-2xl mx-auto">
          <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <AlertCircle className="w-10 h-10 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-red-900 mb-3">Analysis Failed</h2>
          <p className="text-red-700 mb-8 text-lg">{run.error || 'An unexpected error occurred during analysis.'}</p>
          <button 
            onClick={() => window.location.reload()}
            className="px-8 py-3 bg-white border border-red-200 text-red-700 rounded-xl font-bold hover:bg-red-50 transition-colors shadow-sm"
          >
            Retry Analysis
          </button>
        </div>
      ) : (
        run.report && <ReportView report={run.report} />
      )}
    </div>
  );
}


