import { useState } from 'react';
import { Send, Loader2, HelpCircle } from 'lucide-react';
import type { Interview } from '../lib/api';

interface InterviewFormProps {
  interview: Interview;
  onSubmit: (answers: Record<string, string>) => Promise<void>;
}

export function InterviewForm({ interview, onSubmit }: InterviewFormProps) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit(answers);
    } finally {
      setSubmitting(false);
    }
  };

  const handleSkip = async () => {
    if (confirm("Are you sure you want to skip? The analysis might be less accurate without these details.")) {
      setSubmitting(true);
      try {
        await onSubmit({});
      } finally {
        setSubmitting(false);
      }
    }
  };

  const handleChange = (id: string, value: string) => {
    setAnswers(prev => ({ ...prev, [id]: value }));
  };

  const allAnswered = interview.questions.every(q => (answers[q.id] || '').trim().length > 0);

  return (
    <div className="bg-white p-8 rounded-3xl shadow-xl border border-slate-100 max-w-3xl mx-auto">
      <div className="mb-8 text-center">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">We need a bit more info</h2>
        <p className="text-slate-500">
          To give you the best analysis, our agents have a few clarifying questions about your idea.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {interview.questions.map((q) => (
          <div key={q.id} className="space-y-3">
            <label htmlFor={q.id} className="block text-lg font-medium text-slate-800">
              {q.text}
            </label>
            
            {q.guidance && (
              <div className="flex gap-2 items-start p-3 bg-indigo-50 rounded-lg text-sm text-indigo-700">
                <HelpCircle className="w-4 h-4 shrink-0 mt-0.5" />
                <p>{q.guidance}</p>
              </div>
            )}

            <textarea
              id={q.id}
              required
              rows={3}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all resize-none"
              placeholder="Your answer..."
              value={answers[q.id] || ''}
              onChange={(e) => handleChange(q.id, e.target.value)}
            />
          </div>
        ))}

        <div className="pt-4 flex justify-between items-center">
          <button
            type="button"
            onClick={handleSkip}
            disabled={submitting}
            className="text-slate-500 hover:text-slate-700 font-medium px-4 py-2 rounded-lg hover:bg-slate-50 transition-colors text-sm"
          >
            Skip Questions
          </button>

          <button
            type="submit"
            disabled={submitting || !allAnswered}
            className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {submitting ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Submitting...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Submit Answers
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
