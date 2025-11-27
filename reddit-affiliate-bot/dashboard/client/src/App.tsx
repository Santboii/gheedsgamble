import { useState, useEffect } from 'react';
import axios from 'axios';
import { formatDistanceToNow } from 'date-fns';
import { ExternalLink, Copy, Check, X, MessageSquare, BarChart2 } from 'lucide-react';

// API Configuration
const API_URL = 'http://localhost:3001/api';

interface Opportunity {
  post_id: string;
  title: string;
  url: string;
  subreddit: string;
  author: string;
  analysis: {
    confidence: number;
    experience_level: string;
    budget_range: string;
  };
  suggested_response: string;
  created_at: string;
  status: 'new' | 'replied' | 'skipped';
}

interface Stats {
  total_processed: number;
  total_responses: number;
  responses_today: number;
}

function App() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [filter, setFilter] = useState<'new' | 'replied' | 'skipped'>('new');
  const [loading, setLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, [filter]);

  const fetchData = async () => {
    try {
      const [oppsRes, statsRes] = await Promise.all([
        axios.get(`${API_URL}/opportunities?status=${filter}`),
        axios.get(`${API_URL}/stats`)
      ]);
      setOpportunities(oppsRes.data);
      setStats(statsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const updateStatus = async (id: string, status: 'replied' | 'skipped') => {
    try {
      await axios.post(`${API_URL}/opportunities/${id}/status`, { status });
      // Optimistic update
      setOpportunities(prev => prev.filter(opp => opp.post_id !== id));
      // Refresh stats
      const statsRes = await axios.get(`${API_URL}/stats`);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-8 border-b border-slate-700 pb-6">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Reddit Opportunity Finder
            </h1>
            <p className="text-slate-400 mt-1">Monitor and respond to relevant posts</p>
          </div>
          <div className="flex gap-4">
            <div className="bg-slate-800 p-3 rounded-lg border border-slate-700">
              <div className="text-sm text-slate-400">Analyzed</div>
              <div className="text-xl font-bold">{stats?.total_processed || 0}</div>
            </div>
            <div className="bg-slate-800 p-3 rounded-lg border border-slate-700">
              <div className="text-sm text-slate-400">Responses</div>
              <div className="text-xl font-bold">{stats?.total_responses || 0}</div>
            </div>
            <div className="bg-slate-800 p-3 rounded-lg border border-slate-700">
              <div className="text-sm text-slate-400">Today</div>
              <div className="text-xl font-bold text-green-400">{stats?.responses_today || 0}</div>
            </div>
          </div>
        </header>

        {/* Filters */}
        <div className="flex gap-2 mb-6">
          {(['new', 'replied', 'skipped'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === f
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {/* Content */}
        {loading ? (
          <div className="text-center py-12 text-slate-500">Loading opportunities...</div>
        ) : opportunities.length === 0 ? (
          <div className="text-center py-12 bg-slate-800 rounded-xl border border-slate-700">
            <BarChart2 className="mx-auto h-12 w-12 text-slate-600 mb-4" />
            <h3 className="text-xl font-medium text-slate-300">No opportunities found</h3>
            <p className="text-slate-500 mt-2">Check back later or adjust your filters.</p>
          </div>
        ) : (
          <div className="grid gap-6">
            {opportunities.map((opp) => (
              <div key={opp.post_id} className="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg transition-all hover:border-slate-600">
                {/* Post Header */}
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-3">
                    <span className="bg-blue-500/10 text-blue-400 px-3 py-1 rounded-full text-sm font-medium">
                      r/{opp.subreddit}
                    </span>
                    <span className="text-slate-400 text-sm">
                      Posted by u/{opp.author} • {formatDistanceToNow(new Date(opp.created_at))} ago
                    </span>
                  </div>
                  <a
                    href={opp.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    <ExternalLink size={20} />
                  </a>
                </div>

                {/* Post Title */}
                <h2 className="text-xl font-semibold mb-4 text-slate-100">
                  <a href={opp.url} target="_blank" rel="noopener noreferrer" className="hover:text-blue-400 transition-colors">
                    {opp.title}
                  </a>
                </h2>

                {/* Analysis Badges */}
                <div className="flex gap-2 mb-6 flex-wrap">
                  <span className="bg-slate-700/50 px-2 py-1 rounded text-xs text-slate-300 border border-slate-600">
                    Confidence: {Math.round(opp.analysis.confidence * 100)}%
                  </span>
                  <span className="bg-slate-700/50 px-2 py-1 rounded text-xs text-slate-300 border border-slate-600">
                    Level: {opp.analysis.experience_level}
                  </span>
                  <span className="bg-slate-700/50 px-2 py-1 rounded text-xs text-slate-300 border border-slate-600">
                    Budget: {opp.analysis.budget_range}
                  </span>
                </div>

                {/* Suggested Response */}
                <div className="bg-slate-900/50 rounded-lg p-4 mb-6 border border-slate-700/50 relative group">
                  <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => copyToClipboard(opp.suggested_response, opp.post_id)}
                      className="p-2 bg-slate-700 rounded hover:bg-slate-600 text-slate-300 transition-colors"
                      title="Copy response"
                    >
                      {copiedId === opp.post_id ? <Check size={16} className="text-green-400" /> : <Copy size={16} />}
                    </button>
                  </div>
                  <pre className="whitespace-pre-wrap font-sans text-slate-300 text-sm leading-relaxed">
                    {opp.suggested_response}
                  </pre>
                </div>

                {/* Actions */}
                {filter === 'new' && (
                  <div className="flex gap-3 pt-4 border-t border-slate-700">
                    <button
                      onClick={() => updateStatus(opp.post_id, 'replied')}
                      className="flex-1 bg-green-600 hover:bg-green-500 text-white py-2 px-4 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <MessageSquare size={18} />
                      Mark Replied
                    </button>
                    <button
                      onClick={() => updateStatus(opp.post_id, 'skipped')}
                      className="flex-1 bg-slate-700 hover:bg-slate-600 text-slate-200 py-2 px-4 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <X size={18} />
                      Skip
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
