import ReactMarkdown from 'react-markdown';
import { 
  CheckCircle, 
  AlertTriangle, 
  XCircle, 
  Target, 
  Users, 
  TrendingUp, 
  ShieldAlert, 
  Rocket, 
  BookOpen 
} from 'lucide-react';
import type { ClarityReport } from '../lib/api';

import { InterviewEvaluationView } from './InterviewEvaluationView';

interface ReportViewProps {
  report: ClarityReport;
}

export function ReportView({ report }: ReportViewProps) {
  const { idea, audience, market, risks, execution, recommendation, interview_evaluation } = report;

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'PURSUE': return 'from-emerald-500 to-teal-600 shadow-emerald-200';
      case 'KILL': return 'from-red-500 to-rose-600 shadow-red-200';
      case 'PIVOT': return 'from-amber-500 to-orange-600 shadow-amber-200';
      default: return 'from-slate-500 to-slate-600 shadow-slate-200';
    }
  };

  const getVerdictIcon = (verdict: string) => {
    switch (verdict) {
      case 'PURSUE': return <CheckCircle className="w-12 h-12 text-white" />;
      case 'KILL': return <XCircle className="w-12 h-12 text-white" />;
      case 'PIVOT': return <AlertTriangle className="w-12 h-12 text-white" />;
      default: return null;
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      {/* Header / Verdict */}
      <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${getVerdictColor(recommendation.verdict)} shadow-xl p-8 md:p-12 text-white`}>
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-64 h-64 bg-black opacity-10 rounded-full blur-3xl"></div>
        
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
          <div className="flex items-center gap-6">
            <div className="p-4 bg-white/20 backdrop-blur-sm rounded-2xl border border-white/30 shadow-inner">
              {getVerdictIcon(recommendation.verdict)}
            </div>
            <div>
              <div className="text-sm font-bold uppercase tracking-widest opacity-80 mb-1">Final Verdict</div>
              <h2 className="text-5xl font-black tracking-tight">{recommendation.verdict}</h2>
              <div className="flex items-center gap-2 mt-2">
                <div className="h-2 w-24 bg-black/20 rounded-full overflow-hidden">
                  <div className="h-full bg-white rounded-full" style={{ width: `${recommendation.confidence * 100}%` }}></div>
                </div>
                <span className="font-bold opacity-90">{(recommendation.confidence * 100).toFixed(0)}% Confidence</span>
              </div>
            </div>
          </div>
          <div className="md:max-w-lg bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20 text-sm md:text-base leading-relaxed shadow-lg">
            <ReactMarkdown>{recommendation.rationale}</ReactMarkdown>
          </div>
        </div>
      </div>

      {/* Scores */}
      {recommendation.scores && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col h-full">
            <div className="text-center mb-4">
              <div className="text-3xl font-black text-slate-900 mb-1">{recommendation.scores.market_demand.score}/10</div>
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Market Demand</div>
            </div>
            <p className="text-sm text-slate-600 leading-relaxed text-center border-t border-slate-100 pt-4 mt-auto">
              {recommendation.scores.market_demand.reasoning}
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col h-full">
            <div className="text-center mb-4">
              <div className="text-3xl font-black text-slate-900 mb-1">{recommendation.scores.competitive_advantage.score}/10</div>
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Competitive Advantage</div>
            </div>
            <p className="text-sm text-slate-600 leading-relaxed text-center border-t border-slate-100 pt-4 mt-auto">
              {recommendation.scores.competitive_advantage.reasoning}
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col h-full">
            <div className="text-center mb-4">
              <div className="text-3xl font-black text-slate-900 mb-1">{recommendation.scores.technical_feasibility.score}/10</div>
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Technical Feasibility</div>
            </div>
            <p className="text-sm text-slate-600 leading-relaxed text-center border-t border-slate-100 pt-4 mt-auto">
              {recommendation.scores.technical_feasibility.reasoning}
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col h-full">
            <div className="text-center mb-4">
              <div className="text-3xl font-black text-slate-900 mb-1">{recommendation.scores.business_viability.score}/10</div>
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Business Viability</div>
            </div>
            <p className="text-sm text-slate-600 leading-relaxed text-center border-t border-slate-100 pt-4 mt-auto">
              {recommendation.scores.business_viability.reasoning}
            </p>
          </div>
        </div>
      )}

      {/* Idea Overview */}
      <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 card-hover">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-indigo-100 rounded-lg text-indigo-600">
            <Target className="w-6 h-6" />
          </div>
          <h3 className="text-2xl font-bold text-slate-900">Idea Overview</h3>
        </div>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Concept</h4>
              <p className="text-slate-900 font-bold text-xl leading-tight">{idea.title}</p>
            </div>
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">One Liner</h4>
              <p className="text-slate-600 leading-relaxed">{idea.one_liner}</p>
            </div>
          </div>
          <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Summary</h4>
            <p className="text-slate-700 font-medium leading-relaxed">{idea.expanded_summary}</p>
          </div>
        </div>
      </section>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Audience */}
        <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 card-hover">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
              <Users className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-bold text-slate-900">Audience</h3>
          </div>
          <div className="space-y-6">
            <div className="bg-gradient-to-br from-blue-50 to-white p-6 rounded-2xl border border-blue-100 shadow-sm">
              <h4 className="font-bold text-lg text-blue-900 mb-3">Primary Users</h4>
              <ul className="space-y-2">
                {audience.primary_users.map((user, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-600">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-blue-400 shrink-0"></span>
                    {user}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
              <h4 className="font-bold text-lg text-slate-900 mb-3">Jobs to be Done</h4>
              <ul className="space-y-2">
                {audience.jobs_to_be_done.map((job, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-600">
                    <CheckCircle className="w-4 h-4 text-green-500 shrink-0 mt-0.5" />
                    {job}
                  </li>
                ))}
              </ul>
            </div>

            {audience.personas.length > 0 && (
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Personas</h4>
                <div className="space-y-4">
                  {audience.personas.map((persona, idx) => (
                    <div key={idx} className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                      <div className="flex justify-between items-start mb-2">
                        <h5 className="font-bold text-slate-900">{persona.name}</h5>
                        <span className="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded-full border border-slate-200">{persona.role}</span>
                      </div>
                      <p className="text-sm text-slate-600 italic">"{persona.pain_points}"</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Market */}
        <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 card-hover">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-purple-100 rounded-lg text-purple-600">
              <TrendingUp className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-bold text-slate-900">Market & Competition</h3>
          </div>
          <div className="space-y-6">
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Key Competitors</h4>
              <div className="space-y-2">
                {market.competitors.map((comp, idx) => (
                  <div key={idx} className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg border border-purple-100 text-purple-900 font-medium">
                    <div className="w-2 h-2 rounded-full bg-purple-400"></div>
                    {comp}
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Demand Signals</h4>
              <ul className="space-y-2">
                {market.demand_signals.map((signal, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-slate-600">
                    <TrendingUp className="w-4 h-4 text-green-500 shrink-0 mt-0.5" />
                    {signal}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
              <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2">Positioning</h4>
              <p className="text-slate-700 font-medium leading-relaxed">
                {market.positioning}
              </p>
            </div>
          </div>
        </section>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Risks */}
        <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 card-hover">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-amber-100 rounded-lg text-amber-600">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-bold text-slate-900">Risks & Mitigation</h3>
          </div>
          <div className="space-y-6">
            <div className="space-y-4">
              {risks.top_risks.map((risk, idx) => (
                <div key={idx} className="bg-amber-50 p-4 rounded-xl border border-amber-100">
                  <div className="flex items-start gap-3 mb-2">
                    <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                    <p className="font-bold text-amber-900 text-sm">{risk}</p>
                  </div>
                  {risks.mitigations[idx] && (
                    <div className="pl-8 text-sm text-amber-800/80">
                      <span className="font-bold text-amber-800">Mitigation: </span>
                      {risks.mitigations[idx]}
                    </div>
                  )}
                </div>
              ))}
            </div>
            
          </div>
        </section>

        {/* Execution */}
        <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 card-hover">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-emerald-100 rounded-lg text-emerald-600">
              <Rocket className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-bold text-slate-900">Execution Plan</h3>
          </div>
          <div className="space-y-8">
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">MVP Scope</h4>
              <div className="flex flex-wrap gap-2">
                {execution.mvp_scope.map((feat, i) => (
                  <span key={i} className="px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-lg text-sm font-bold border border-emerald-100 shadow-sm">
                    {feat}
                  </span>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">2-Week Plan</h4>
              <div className="space-y-3">
                {execution.two_week_plan.map((step, i) => (
                  <div key={i} className="flex gap-4 items-start">
                    <span className="flex items-center justify-center w-6 h-6 rounded-full bg-slate-100 text-slate-500 text-xs font-bold shrink-0">
                      {i + 1}
                    </span>
                    <p className="text-sm text-slate-700 font-medium pt-0.5">{step}</p>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">2-Month Plan</h4>
              <div className="space-y-3">
                {execution.two_month_plan.map((step, i) => (
                  <div key={i} className="flex gap-4 items-start">
                    <span className="flex items-center justify-center w-6 h-6 rounded-full bg-slate-100 text-slate-500 text-xs font-bold shrink-0">
                      {i + 1}
                    </span>
                    <p className="text-sm text-slate-700 font-medium pt-0.5">{step}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </div>

      {/* Interview Evaluation */}
      {interview_evaluation && (
        <section className="animate-in fade-in slide-in-from-bottom-4 duration-700 delay-300">
          <InterviewEvaluationView evaluation={interview_evaluation} />
        </section>
      )}

      {/* Sources */}
      {report.sources && report.sources.length > 0 && (
        <section className="bg-gray-50 p-6 rounded-xl border border-gray-200">
          <div className="flex items-center gap-2 mb-4 text-gray-500">
            <BookOpen className="w-5 h-5" />
            <h3 className="text-lg font-semibold">Sources & References</h3>
          </div>
          <ul className="grid md:grid-cols-2 gap-2 text-xs text-gray-500">
            {report.sources.map((source, i) => (
              <li key={i} className="truncate hover:text-gray-900">
                <a href={source.url} target="_blank" rel="noopener noreferrer" className="hover:underline" title={source.title}>
                  {source.title}
                </a>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
