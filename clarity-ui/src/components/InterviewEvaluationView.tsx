import { AlertTriangle, Lightbulb } from 'lucide-react';
import type { InterviewEvaluation } from '../lib/api';

interface InterviewEvaluationViewProps {
  evaluation: InterviewEvaluation;
}

export function InterviewEvaluationView({ evaluation }: InterviewEvaluationViewProps) {
  return (
    <div className="space-y-8">
      <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
        <h2 className="text-2xl font-bold text-slate-900 mb-4">Interview Analysis</h2>
        <p className="text-slate-600 leading-relaxed">{evaluation.summary}</p>
      </div>

      <div className="grid gap-6">
        {evaluation.evaluations.map((item) => (
          <div key={item.question_id} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
            <div className="mb-4">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Question</h3>
              <p className="text-slate-900 font-medium">{item.question_text}</p>
            </div>
            
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Your Answer</h3>
              <p className="text-slate-700 italic bg-slate-50 p-3 rounded-lg border border-slate-100">
                "{item.answer_text}"
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-slate-900 mb-2">Analysis</h4>
                <p className="text-slate-600 text-sm">{item.analysis}</p>
              </div>

              {item.suggestions.length > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 font-semibold text-indigo-700 mb-2">
                    <Lightbulb className="w-4 h-4" />
                    Suggestions
                  </h4>
                  <ul className="space-y-1">
                    {item.suggestions.map((s, i) => (
                      <li key={i} className="text-sm text-slate-600 flex items-start gap-2">
                        <span className="block w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0" />
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {item.concerns.length > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 font-semibold text-amber-600 mb-2">
                    <AlertTriangle className="w-4 h-4" />
                    Risks & Concerns
                  </h4>
                  <ul className="space-y-1">
                    {item.concerns.map((c, i) => (
                      <li key={i} className="text-sm text-slate-600 flex items-start gap-2">
                        <span className="block w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                        {c}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
