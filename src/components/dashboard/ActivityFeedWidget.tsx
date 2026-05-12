import { Sparkles, FileText, Clock, CheckCircle, Upload, TrendingUp, Radar, Target } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { getTimeAgo, formatCurrency } from '@/utils/scholarshipUtils';
import { useRealtimeOpportunities } from '@/hooks/useRealtimeOpportunities';
import { useDiscoveryPulse } from '@/hooks/useDiscoveryPulse';
import { useMemo } from 'react';

interface Activity {
  id: string;
  type: 'new' | 'mission' | 'match' | 'system';
  icon: React.ElementType;
  iconColor: string;
  title: string;
  description: string;
  timestamp: string;
}

export const ActivityFeedWidget = () => {
  const { opportunities: realtimeOpps } = useRealtimeOpportunities();
  const { missions } = useDiscoveryPulse();

  const activities = useMemo(() => {
    const items: Activity[] = [];

    // 1. Convert real-time opportunities into activity items
    realtimeOpps.slice(0, 5).forEach(opp => {
      items.push({
        id: `opp-${opp.id}`,
        type: 'new',
        icon: Sparkles,
        iconColor: 'text-primary',
        title: 'Opportunity Discovered',
        description: `"${opp.name || opp.title}" found on ${new URL(opp.source_url || '').hostname}`,
        timestamp: opp.last_verified || new Date().toISOString(),
      });
    });

    // 2. Convert missions into activity items if they represent a discovery
    missions.slice(0, 5).forEach(mission => {
      if (mission.label?.includes('Match') || mission.label?.includes('discovered')) {
        items.push({
          id: `mission-${mission.id}`,
          type: 'match',
          icon: Target,
          iconColor: 'text-emerald-500',
          title: 'High-Potential Match',
          description: mission.label,
          timestamp: mission.timestamp || new Date().toISOString(),
        });
      } else if (mission.label?.includes('Hunt') || mission.label?.includes('Drone')) {
        items.push({
          id: `mission-${mission.id}`,
          type: 'mission',
          icon: Radar,
          iconColor: 'text-blue-500',
          title: 'Drone Fleet Deployed',
          description: mission.label,
          timestamp: mission.timestamp || new Date().toISOString(),
        });
      }
    });

    // Sort by timestamp descending
    return items.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()).slice(0, 6);
  }, [realtimeOpps, missions]);

  const getIconBadge = (activity: Activity) => {
    const Icon = activity.icon;
    return (
      <div className={`rounded-full bg-muted p-2 ${activity.iconColor}`}>
        <Icon className="h-3.5 w-3.5" />
      </div>
    );
  };

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Cortex Activity</h3>
        {activities.length > 0 && <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />}
      </div>
      
      <div className="space-y-4">
        {activities.length > 0 ? (
          activities.map((activity, index) => (
            <div key={activity.id} className="relative">
              <div className="flex gap-3">
                {getIconBadge(activity)}
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-foreground mb-0.5">{activity.title}</div>
                  <div className="text-xs text-muted-foreground mb-1 leading-relaxed">{activity.description}</div>
                  <div className="text-[10px] text-zinc-500">{getTimeAgo(activity.timestamp)}</div>
                </div>
              </div>
              {index < activities.length - 1 && (
                <div className="absolute left-[18px] top-10 bottom-0 w-px bg-border/50" />
              )}
            </div>
          ))
        ) : (
          <div className="py-8 text-center">
            <div className="bg-muted/30 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
              <Clock className="w-6 h-6 text-zinc-500" />
            </div>
            <p className="text-xs text-muted-foreground">Awaiting drone telemetry...</p>
          </div>
        )}
      </div>
      <Button variant="ghost" className="w-full mt-4 text-xs font-bold uppercase tracking-widest text-zinc-500" size="sm">
        Full Event Log
      </Button>
    </Card>
  );
};
