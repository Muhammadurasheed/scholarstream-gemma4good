import { Scholarship } from '@/types/scholarship';
import { OpportunityCard } from './OpportunityCard';
import { useScholarships } from '@/hooks/useScholarships';
import { cn } from '@/lib/utils';

interface SimpleOpportunityGridProps {
  opportunities: Scholarship[];
  view?: 'grid' | 'list';
  className?: string;
  justFlushedIds?: Set<string>;
}

/**
 * Simple CSS Grid-based opportunity display (no virtualization)
 * Used with pagination for better UX and SEO
 */
export const SimpleOpportunityGrid = ({ 
  opportunities, 
  view = 'grid',
  className,
  justFlushedIds = new Set(),
}: SimpleOpportunityGridProps) => {
  const { savedScholarshipIds, toggleSaveScholarship, startApplication } = useScholarships();

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
    <div 
      className={cn(
        view === 'grid' 
          ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6'
          : 'flex flex-col gap-4',
        className
      )}
    >
      {opportunities.map((scholarship) => (
        <OpportunityCard
          key={scholarship.id}
          scholarship={scholarship}
          isSaved={savedScholarshipIds.has(scholarship.id)}
          onToggleSave={toggleSaveScholarship}
          onStartApplication={startApplication}
          isJustAdded={justFlushedIds.has(scholarship.id)}
        />
      ))}
    </div>
  );
};
