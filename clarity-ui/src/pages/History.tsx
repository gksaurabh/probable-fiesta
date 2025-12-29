import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Clock, ArrowRight, Search, AlertCircle, Loader2 } from 'lucide-react';
import { listRuns } from '../lib/api';
import type { RunStatus } from '../lib/api';

interface RunSummary {
  run_id: string;
  status: RunStatus;
  created_at: string;
  idea_text?: string;
}

export function History() {
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRuns = async () => {
      try {
        const data = await listRuns();
        // Sort by created_at desc
        const sorted = data.sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setRuns(sorted);
      } catch (err) {
        console.error(err);
        setError('Failed to load history.');
      } finally {
        setLoading(false);
      }
    };

    fetchRuns();
  }, []);

  const getStatusColor = (status: RunStatus) => {
    switch (status) {
      case 'COMPLETED': return 'bg-green-100 text-green-700';
      case 'FAILED': return 'bg-red-100 text-red-700';
      case 'RUNNING': return 'bg-indigo-100 text-indigo-700';
      case 'QUEUED': return 'bg-gray-100 text-gray-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-20">
        <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
        <p className="text-gray-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analysis History</h1>
        <Link 
          to="/" 
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
        >
          New Analysis
        </Link>
      </div>

      {runs.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-xl border border-gray-200 border-dashed">
          <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-1">No analyses yet</h3>
          <p className="text-gray-500 mb-6">Start your first idea validation analysis today.</p>
          <Link 
            to="/" 
            className="text-indigo-600 font-medium hover:underline"
          >
            Start New Analysis
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {runs.map((run) => (
            <Link 
              key={run.run_id} 
              to={`/runs/${run.run_id}`}
              className="block bg-white p-6 rounded-xl border border-gray-200 hover:border-indigo-300 hover:shadow-md transition-all group"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold tracking-wide ${getStatusColor(run.status)}`}>
                      {run.status}
                    </span>
                    <span className="flex items-center gap-1 text-xs text-gray-500">
                      <Clock className="w-3 h-3" />
                      {new Date(run.created_at).toLocaleDateString()} at {new Date(run.created_at).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-gray-900 font-medium truncate">
                    {run.idea_text || 'Untitled Idea'}
                  </p>
                </div>
                <ArrowRight className="w-5 h-5 text-gray-300 group-hover:text-indigo-600 transition-colors" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
