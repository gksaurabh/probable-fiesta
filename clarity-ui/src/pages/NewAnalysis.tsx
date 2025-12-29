import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, Loader2 } from 'lucide-react';
import { runAnalysis } from '../lib/api';

export function NewAnalysis() {
  const [idea, setIdea] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idea.trim()) return;

    setIsSubmitting(true);
    setError(null);

    try {
      const { run_id } = await runAnalysis(idea);
      navigate(`/runs/${run_id}`);
    } catch (err) {
      console.error(err);
      setError('Failed to start analysis. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-12">
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-50 to-white shadow-lg shadow-indigo-100 border border-indigo-50 mb-6 transform rotate-3 hover:rotate-0 transition-transform duration-300">
          <Sparkles className="w-10 h-10 text-indigo-600" />
        </div>
        <h1 className="text-5xl font-bold text-slate-900 mb-4 tracking-tight">Validate Your Next Big Idea</h1>
        <p className="text-xl text-slate-500 max-w-2xl mx-auto leading-relaxed">
          Get comprehensive market analysis, risk assessment, and execution plans in minutes using our multi-agent AI system.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl blur opacity-20 group-hover:opacity-30 transition duration-1000 group-hover:duration-200"></div>
        <div className="relative bg-white p-8 sm:p-10 rounded-2xl shadow-xl border border-slate-100">
          <div className="mb-8">
            <label htmlFor="idea" className="block text-sm font-semibold text-slate-700 mb-3 uppercase tracking-wider">
              Describe your startup idea
            </label>
            <textarea
              id="idea"
              rows={6}
              className="w-full px-6 py-5 rounded-xl bg-slate-50 border-2 border-slate-100 focus:border-indigo-500 focus:ring-0 focus:bg-white transition-all resize-none text-slate-900 placeholder-slate-400 text-lg leading-relaxed"
              placeholder="e.g. A marketplace for renting high-end camping gear with delivery to campsites..."
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              disabled={isSubmitting}
            />
            <p className="mt-3 text-sm text-slate-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
              Be as specific as possible for better results
            </p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-xl text-sm border border-red-100 flex items-center gap-2">
              <span className="font-bold">Error:</span> {error}
            </div>
          )}

          <button
            type="submit"
            disabled={!idea.trim() || isSubmitting}
            className="w-full flex items-center justify-center gap-3 bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white font-bold py-5 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-200 hover:shadow-indigo-300 hover:-translate-y-0.5 active:translate-y-0 text-lg"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                Starting Analysis Engine...
              </>
            ) : (
              <>
                Start Analysis
                <ArrowRight className="w-6 h-6" />
              </>
            )}
          </button>
        </div>
      </form>
      
      <div className="mt-12 grid grid-cols-3 gap-6 text-center">
        {[
          { label: 'Market Research', desc: 'Deep dive into trends' },
          { label: 'Risk Analysis', desc: 'Identify potential pitfalls' },
          { label: 'Execution Plan', desc: 'Step-by-step roadmap' }
        ].map((item, i) => (
          <div key={i} className="p-4 rounded-xl bg-white border border-slate-100 shadow-sm">
            <h3 className="font-bold text-slate-900">{item.label}</h3>
            <p className="text-sm text-slate-500 mt-1">{item.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
