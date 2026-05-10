import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Scholarship } from '@/types/scholarship';
import { OpportunityCard } from './OpportunityCard';
import { useScholarships } from '@/hooks/useScholarships';
import { ChevronRight, ChevronDown, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CortexSourceGroupProps {
  opportunities: Scholarship[];
}

export const CortexSourceGroup = ({ opportunities }: CortexSourceGroupProps) => {
  const { savedScholarshipIds, toggleSaveScholarship, startApplication } = useScholarships();
  
  // State for expanding categories
  const [expandedCats, setExpandedCats] = useState<Record<string, boolean>>({});

  const toggleExpand = (cat: string) => {
    setExpandedCats(prev => ({ ...prev, [cat]: !prev[cat] }));
  };

  // Grouping logic
  const redditOpps = opportunities.filter(o => o.source_url?.includes('reddit.com'));
  const linkedinOpps = opportunities.filter(o => o.source_url?.includes('linkedin.com'));
  const xOpps = opportunities.filter(o => o.source_url?.includes('x.com') || o.source_url?.includes('twitter.com'));
  const webOpps = opportunities.filter(o => 
    !o.source_url?.includes('reddit.com') && 
    !o.source_url?.includes('linkedin.com') && 
    !o.source_url?.includes('x.com') && 
    !o.source_url?.includes('twitter.com')
  );

  const categories = [
    { id: 'web', title: 'Atomic Sources (.edu & Foundations)', icon: '🏛️', opps: webOpps, color: 'from-emerald-500/20 to-teal-500/20', textColor: 'text-emerald-400' },
    { id: 'linkedin', title: 'LinkedIn Bounties', icon: '💼', opps: linkedinOpps, color: 'from-blue-500/20 to-cyan-500/20', textColor: 'text-blue-400' },
    { id: 'reddit', title: 'Reddit Signals', icon: '🔥', opps: redditOpps, color: 'from-orange-500/20 to-red-500/20', textColor: 'text-orange-400' },
    { id: 'x', title: 'X/Twitter Threads', icon: '🐦', opps: xOpps, color: 'from-slate-500/20 to-zinc-500/20', textColor: 'text-slate-300' },
  ];

  if (opportunities.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 px-4 text-center border border-white/5 rounded-2xl bg-white/[0.02] backdrop-blur-sm relative overflow-hidden">
        {/* Radar sweeping background */}
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20 animate-pulse" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 border border-primary/20 rounded-full animate-ping opacity-20" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 border border-primary/40 rounded-full animate-ping opacity-40" />
        
        <div className="relative z-10 w-16 h-16 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(var(--primary),0.3)]">
          <svg className="w-8 h-8 text-primary animate-spin-slow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v20M17 5l-10 14M22 12H2M19 17L5 7" />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-white mb-2 tracking-tight">Cortex V3 is Hunting</h3>
        <p className="text-sm text-zinc-400 max-w-sm leading-relaxed">
          The deep web is being scanned for high-fidelity opportunities that match your Digital DNA. High-value matches will appear here automatically.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      {categories.map((category) => {
        if (category.opps.length === 0) return null;
        
        const isExpanded = expandedCats[category.id] || false;
        const visibleOpps = isExpanded ? category.opps : category.opps.slice(0, 2);
        const hasMore = category.opps.length > 2;

        return (
          <div key={category.id} className="relative">
            {/* Category Header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={cn("p-2 rounded-xl bg-gradient-to-br border border-white/10", category.color)}>
                  <span className="text-xl leading-none block">{category.icon}</span>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                    {category.title}
                    <span className={cn("text-xs font-black px-2 py-0.5 rounded-full bg-white/10", category.textColor)}>
                      {category.opps.length}
                    </span>
                  </h3>
                </div>
              </div>
              
              {hasMore && (
                <button 
                  onClick={() => toggleExpand(category.id)}
                  className="text-sm font-semibold text-primary hover:text-primary/80 transition-colors flex items-center gap-1 bg-primary/10 hover:bg-primary/20 px-3 py-1.5 rounded-full"
                >
                  {isExpanded ? 'Collapse' : `View all ${category.opps.length} matches`}
                  {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                </button>
              )}
            </div>

            {/* Grid */}
            <motion.div 
              layout
              className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-6"
            >
              <AnimatePresence mode="popLayout">
                {visibleOpps.map((opp) => (
                  <motion.div
                    key={opp.id}
                    layout
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.3 }}
                  >
                    <OpportunityCard
                      scholarship={opp}
                      isSaved={savedScholarshipIds.has(opp.id)}
                      onToggleSave={toggleSaveScholarship}
                      onStartApplication={startApplication}
                    />
                  </motion.div>
                ))}
              </AnimatePresence>
            </motion.div>
          </div>
        );
      })}
    </div>
  );
};
