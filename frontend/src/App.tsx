import { useState } from 'react';

export default function App() {
  const [cluster, setCluster] = useState<string>('');
  
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/20 via-slate-950 to-slate-950 -z-10" />
      
      <header className="border-b border-white/5 bg-white/5 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h1 className="font-semibold text-lg tracking-tight">Zero-Trust SRE Agent</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-sm text-slate-400">Connected as <span className="text-indigo-400 font-medium">sre-admin@enterprise.local</span></div>
            <div className="h-8 w-8 rounded-full bg-slate-800 border border-slate-700 overflow-hidden">
               <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="avatar" />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Sidebar / Cluster Selector */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-slate-900/50 border border-white/5 rounded-2xl p-6 backdrop-blur-sm shadow-xl">
              <h2 className="text-lg font-medium mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Target Environment
              </h2>
              <div className="space-y-3">
                {['eks-prod-us-east', 'onprem-tunnel-01', 'shadow-cluster-eu'].map((c) => (
                  <button 
                    key={c}
                    onClick={() => setCluster(c)}
                    className={`w-full text-left px-4 py-3 rounded-xl transition-all duration-200 border ${cluster === c ? 'bg-indigo-500/10 border-indigo-500/50 text-indigo-300 shadow-[0_0_15px_rgba(99,102,241,0.1)]' : 'bg-slate-950/50 border-white/5 text-slate-400 hover:bg-slate-800/50 hover:border-white/10'}`}
                  >
                    <div className="font-medium">{c}</div>
                    <div className="text-xs opacity-60 mt-1">{c.includes('prod') ? 'AWS Agentless' : 'MCP Sidecar'}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Action Area */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-slate-900/50 border border-white/5 rounded-2xl p-6 backdrop-blur-sm shadow-xl min-h-[400px] flex flex-col items-center justify-center text-center">
              {cluster ? (
                <div className="max-w-md w-full space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                  <div className="w-16 h-16 bg-indigo-500/10 rounded-2xl flex items-center justify-center mx-auto border border-indigo-500/20">
                     <svg className="w-8 h-8 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-medium text-white mb-2">Connected to {cluster}</h3>
                    <p className="text-slate-400 text-sm">Identity propagated via AWS STS. Awaiting SRE intent.</p>
                  </div>
                  
                  <div className="relative">
                    <input 
                      type="text" 
                      placeholder="e.g. Scale down deployment frontend to 2 replicas" 
                      className="w-full bg-slate-950/50 border border-white/10 rounded-xl py-3 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all placeholder:text-slate-600"
                    />
                    <button className="absolute right-2 top-2 bottom-2 bg-indigo-500 hover:bg-indigo-600 text-white px-4 rounded-lg text-sm font-medium transition-colors">
                      Execute
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4 text-slate-500">
                  <svg className="w-12 h-12 mx-auto opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                  </svg>
                  <p>Select a target environment to begin.</p>
                </div>
              )}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
