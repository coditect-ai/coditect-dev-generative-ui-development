import React, { useState } from 'react';

const MarketPositioningDashboard = () => {
  const [activeTab, setActiveTab] = useState('positioning');
  
  const tabs = [
    { id: 'positioning', label: 'Market Position' },
    { id: 'timeline', label: '2026 Channels' },
    { id: 'moats', label: 'Competitive Moats' },
    { id: 'risks', label: 'Risk Matrix' }
  ];

  const PositioningMatrix = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-slate-800">AI Code Industry Positioning</h3>
      
      <div className="relative bg-slate-50 rounded-lg p-6 h-80">
        {/* Axes */}
        <div className="absolute left-12 top-4 bottom-12 w-px bg-slate-300" />
        <div className="absolute left-12 right-4 bottom-12 h-px bg-slate-300" />
        
        {/* Labels */}
        <div className="absolute left-0 top-1/2 -translate-y-1/2 -rotate-90 text-xs font-medium text-slate-500 whitespace-nowrap">
          MULTI-MODEL ← → SINGLE-MODEL
        </div>
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-xs font-medium text-slate-500">
          HORIZONTAL ← → VERTICAL
        </div>
        
        {/* Quadrant Labels */}
        <div className="absolute top-8 left-16 text-xs text-slate-400">Single + Horizontal</div>
        <div className="absolute top-8 right-8 text-xs text-slate-400">Single + Vertical</div>
        <div className="absolute bottom-16 left-16 text-xs text-slate-400">Multi + Horizontal</div>
        <div className="absolute bottom-16 right-8 text-xs text-slate-400">Multi + Vertical</div>
        
        {/* Competitors */}
        <div className="absolute top-16 left-24 bg-gray-200 px-3 py-1.5 rounded text-xs font-medium text-gray-700">
          GitHub Copilot
        </div>
        <div className="absolute top-28 left-32 bg-gray-200 px-3 py-1.5 rounded text-xs font-medium text-gray-700">
          Codeium
        </div>
        <div className="absolute bottom-24 left-28 bg-blue-100 px-3 py-1.5 rounded text-xs font-medium text-blue-700">
          Cursor
        </div>
        <div className="absolute bottom-32 left-40 bg-blue-100 px-3 py-1.5 rounded text-xs font-medium text-blue-700">
          Windsurf
        </div>
        <div className="absolute top-20 right-24 bg-orange-100 px-3 py-1.5 rounded text-xs font-medium text-orange-700">
          Gap: Vertical Only
        </div>
        
        {/* Coditect - highlighted */}
        <div className="absolute bottom-20 right-16 bg-emerald-500 px-4 py-2 rounded-lg shadow-lg text-sm font-bold text-white animate-pulse">
          CODITECT
        </div>
        
        {/* Opportunity zone */}
        <div className="absolute bottom-14 right-8 w-32 h-24 border-2 border-dashed border-emerald-400 rounded-lg opacity-50" />
        <div className="absolute bottom-8 right-12 text-xs text-emerald-600 font-medium">
          Opportunity Zone
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div className="bg-gray-100 p-3 rounded">
          <div className="font-medium text-gray-700">Single-Model Players</div>
          <div className="text-gray-500 text-xs mt-1">Locked to one provider, commodity features</div>
        </div>
        <div className="bg-blue-50 p-3 rounded">
          <div className="font-medium text-blue-700">Multi-Model Horizontal</div>
          <div className="text-blue-500 text-xs mt-1">Good flexibility, no vertical depth</div>
        </div>
        <div className="bg-emerald-50 p-3 rounded">
          <div className="font-medium text-emerald-700">Multi-Model Vertical</div>
          <div className="text-emerald-500 text-xs mt-1">Coditect's moat position</div>
        </div>
      </div>
    </div>
  );

  const TimelineChannels = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-slate-800">2026 Distribution Channels</h3>
      
      <div className="space-y-4">
        {[
          {
            channel: 'Apps SDK',
            provider: 'OpenAI',
            tam: '850M users',
            relevance: 'HIGH',
            coditect: 'Generate compliant code action in ChatGPT',
            color: 'emerald'
          },
          {
            channel: 'Mini Apps',
            provider: 'Apple',
            tam: 'iOS ecosystem',
            relevance: 'MEDIUM',
            coditect: 'Compliance checker for developers',
            color: 'blue'
          },
          {
            channel: 'Group Chats',
            provider: 'OpenAI → Meta',
            tam: 'Social discovery',
            relevance: 'LOW',
            coditect: 'Enterprise has own channels',
            color: 'slate'
          }
        ].map((item, i) => (
          <div key={i} className={`border-l-4 border-${item.color}-500 bg-${item.color}-50 p-4 rounded-r-lg`}>
            <div className="flex justify-between items-start">
              <div>
                <div className="font-semibold text-slate-800">{item.channel}</div>
                <div className="text-sm text-slate-600">{item.provider}</div>
              </div>
              <div className="text-right">
                <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                  item.relevance === 'HIGH' ? 'bg-emerald-200 text-emerald-800' :
                  item.relevance === 'MEDIUM' ? 'bg-blue-200 text-blue-800' :
                  'bg-slate-200 text-slate-800'
                }`}>
                  {item.relevance}
                </span>
                <div className="text-xs text-slate-500 mt-1">TAM: {item.tam}</div>
              </div>
            </div>
            <div className="mt-2 text-sm text-slate-700">
              <span className="font-medium">Coditect Play:</span> {item.coditect}
            </div>
          </div>
        ))}
      </div>
      
      <div className="bg-amber-50 border border-amber-200 p-4 rounded-lg">
        <div className="font-medium text-amber-800">Key Insight from A16Z</div>
        <div className="text-sm text-amber-700 mt-1">
          "In 2009, App Store TAM was 6M iPhones. Today, Apps SDK TAM is 850M users.
          The scale is enormous from day one."
        </div>
      </div>
    </div>
  );

  const CompetitiveMoats = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-slate-800">Why Labs Can't Replicate Coditect</h3>
      
      <div className="grid grid-cols-2 gap-4">
        {[
          {
            moat: 'Multi-Model Access',
            labs: 'Can only ship own models',
            coditect: 'Any model, any provider',
            icon: '🔗'
          },
          {
            moat: 'Compliance First',
            labs: 'Generic, horizontal focus',
            coditect: 'Purpose-built for regulated',
            icon: '🛡️'
          },
          {
            moat: 'Incentive Structure',
            labs: 'PMs promoted for safe features',
            coditect: 'Founders rewarded for risk',
            icon: '🎯'
          },
          {
            moat: 'Vertical Depth',
            labs: 'Breadth over depth',
            coditect: 'Healthcare, Fintech expertise',
            icon: '📊'
          }
        ].map((item, i) => (
          <div key={i} className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
            <div className="text-2xl mb-2">{item.icon}</div>
            <div className="font-semibold text-slate-800">{item.moat}</div>
            <div className="mt-3 space-y-2 text-sm">
              <div className="flex items-start gap-2">
                <span className="text-red-500">✗</span>
                <span className="text-slate-600"><span className="font-medium">Labs:</span> {item.labs}</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-emerald-500">✓</span>
                <span className="text-slate-600"><span className="font-medium">Coditect:</span> {item.coditect}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="bg-slate-800 text-white p-4 rounded-lg">
        <div className="font-medium">A16Z Quote</div>
        <div className="text-sm text-slate-300 mt-1 italic">
          "The direction of ambition you're incentivized to have at big tech is really different.
          When you're a founder, you're like, look, I need to distinguish myself, I want to do something crazy."
        </div>
      </div>
    </div>
  );

  const RiskMatrix = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-slate-800">Risk Assessment Matrix</h3>
      
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-100">
              <th className="text-left p-3 font-medium">Risk</th>
              <th className="text-left p-3 font-medium">A16Z View</th>
              <th className="text-left p-3 font-medium">Mitigation</th>
              <th className="text-center p-3 font-medium">Severity</th>
            </tr>
          </thead>
          <tbody>
            {[
              {
                risk: 'Labs copy features',
                view: '"Don\'t worry" - different incentives',
                mitigation: 'Multi-model + vertical depth',
                severity: 'LOW'
              },
              {
                risk: 'Market timing',
                view: '"Best time ever" but finite window',
                mitigation: 'Accelerate, don\'t perfect',
                severity: 'MEDIUM'
              },
              {
                risk: 'Over-competition',
                view: 'Room for 30-50 winners',
                mitigation: 'Own regulated vertical',
                severity: 'LOW'
              },
              {
                risk: 'Talent spread thin',
                view: 'Over-raising causes this',
                mitigation: 'Raise 24mo, focus ruthlessly',
                severity: 'MEDIUM'
              },
              {
                risk: 'Weak PMF',
                view: '"Only product problems"',
                mitigation: 'High CAC = product needs work',
                severity: 'HIGH'
              }
            ].map((item, i) => (
              <tr key={i} className="border-b border-slate-100">
                <td className="p-3 font-medium text-slate-800">{item.risk}</td>
                <td className="p-3 text-slate-600">{item.view}</td>
                <td className="p-3 text-slate-600">{item.mitigation}</td>
                <td className="p-3 text-center">
                  <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                    item.severity === 'LOW' ? 'bg-emerald-100 text-emerald-800' :
                    item.severity === 'MEDIUM' ? 'bg-amber-100 text-amber-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {item.severity}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-emerald-50 p-4 rounded-lg text-center">
          <div className="text-2xl font-bold text-emerald-600">2</div>
          <div className="text-xs text-emerald-700">Low Risk</div>
        </div>
        <div className="bg-amber-50 p-4 rounded-lg text-center">
          <div className="text-2xl font-bold text-amber-600">2</div>
          <div className="text-xs text-amber-700">Medium Risk</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg text-center">
          <div className="text-2xl font-bold text-red-600">1</div>
          <div className="text-xs text-red-700">High Risk</div>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'positioning': return <PositioningMatrix />;
      case 'timeline': return <TimelineChannels />;
      case 'moats': return <CompetitiveMoats />;
      case 'risks': return <RiskMatrix />;
      default: return <PositioningMatrix />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-slate-800">Coditect.AI Market Analysis</h1>
          <p className="text-slate-600 text-sm mt-1">Based on A16Z's "Harsh Truth About AI Startups" Framework</p>
        </div>
        
        {/* Key Stats */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          {[
            { label: 'Industry Winners', value: '30-50', sublabel: 'Not a single winner market' },
            { label: 'Apps SDK TAM', value: '850M', sublabel: 'vs 6M iPhones in 2009' },
            { label: 'Consumer Price', value: '$200+', sublabel: 'Willingness to pay/month' },
            { label: 'Distribution', value: '2026', sublabel: 'New channels emerging' }
          ].map((stat, i) => (
            <div key={i} className="bg-white rounded-lg p-4 shadow-sm">
              <div className="text-2xl font-bold text-slate-800">{stat.value}</div>
              <div className="text-sm font-medium text-slate-700">{stat.label}</div>
              <div className="text-xs text-slate-500">{stat.sublabel}</div>
            </div>
          ))}
        </div>
        
        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="flex border-b border-slate-200">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-slate-800 text-white'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
          
          <div className="p-6">
            {renderContent()}
          </div>
        </div>
        
        {/* Bottom CTA */}
        <div className="mt-6 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-lg p-6 text-white">
          <div className="font-bold text-lg">Strategic Imperative</div>
          <div className="mt-2 text-emerald-100">
            Multi-model orchestration + compliance-first + regulated vertical = 
            <span className="font-bold text-white"> Coditect's defensible position</span>
          </div>
          <div className="mt-3 text-sm text-emerald-200">
            Labs can't replicate (single-model lock) • Horizontal players won't specialize • Window is open but finite
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketPositioningDashboard;
