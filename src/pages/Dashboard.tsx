import { useState, useMemo, useEffect } from 'react';
import { Target, DollarSign, Clock, FileText, Sparkles, Search, Wifi, WifiOff } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { StatsCard } from '@/components/dashboard/StatsCard';
import { FinancialImpactWidget } from '@/components/dashboard/FinancialImpactWidget';
import { QuickActionsWidget } from '@/components/dashboard/QuickActionsWidget';
import { ActivityFeedWidget } from '@/components/dashboard/ActivityFeedWidget';
import { PriorityAlertsSection } from '@/components/dashboard/PriorityAlertsSection';
import { PaginatedGrid } from '@/components/dashboard/PaginatedGrid';
import { SimpleOpportunityGrid } from '@/components/dashboard/SimpleOpportunityGrid';
import { CortexSourceGroup } from '@/components/dashboard/CortexSourceGroup';
import { MobileBottomNav } from '@/components/dashboard/MobileBottomNav';
import { FloatingChatAssistant } from '@/components/dashboard/FloatingChatAssistant';
import { DiscoveryPulseIndicator } from '@/components/dashboard/DiscoveryPulseIndicator';
import { MissionControlConsole } from '@/components/dashboard/MissionControlConsole';
import { LiveHunterWidget } from '@/components/dashboard/LiveHunterWidget';
import { ViewToggle } from '@/components/dashboard/ViewToggle';
import { LocationFilter, LocationScope, filterByLocation, sortByLocationRelevance } from '@/components/dashboard/LocationFilter';
import { SourceFilter, SourceScope } from '@/components/dashboard/SourceFilter';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { useScholarships } from '@/hooks/useScholarships';
import { useAuth } from '@/contexts/AuthContext';
import { Skeleton } from '@/components/ui/skeleton';
import { formatCurrency, calculateDaysUntilDeadline, isNewScholarship } from '@/utils/scholarshipUtils';
import { UserProfile } from '@/types/scholarship';
import { matchingEngine } from '@/services/matchingEngine';
import { useRealtimeOpportunities } from '@/hooks/useRealtimeOpportunities';
import { Badge } from '@/components/ui/badge';
import { db } from '@/lib/firebase';
import { doc, getDoc } from 'firebase/firestore';
import { NotificationPill } from '@/components/dashboard/NotificationPill';
import { SkeletonCard } from '@/components/ui/SkeletonCard';
import { normalizeApplyUrl } from '@/utils/scholarshipUtils';

// Derive profile type from onboarding data for tab defaults
const deriveProfileType = (profile: UserProfile | null): 'coder' | 'medical' | 'arts' | 'engineering' | 'entrepreneur' | 'general' => {
  if (!profile) return 'general';
  const major = (profile.major || '').toLowerCase();
  const interests = (profile.interests || []).map(i => i.toLowerCase()).join(' ');
  const combined = `${major} ${interests}`;
  if (combined.match(/medicine|medical|pharma|nursing|health|clinical|biology|biochem/)) return 'medical';
  if (combined.match(/art|design|music|film|creative|fashion|architecture/)) return 'arts';
  if (combined.match(/startup|entrepreneur|business|venture|product/)) return 'entrepreneur';
  if (combined.match(/computer|software|coding|ai|ml|cyber|data|blockchain|hack/)) return 'coder';
  if (combined.match(/engineer|mechanical|electrical|civil|chemical|material/)) return 'engineering';
  return 'general';
};

// Pick default dashboard tab based on profile
const getDefaultTab = (profileType: ReturnType<typeof deriveProfileType>): string => {
  // Non-coders should not default to 'picks' which skews tech
  // Everyone lands on 'all' first, but Cortex Picks are still accessible
  if (profileType === 'medical') return 'scholarships'; // Fellowships/grants
  if (profileType === 'arts') return 'scholarships';     // Residencies/grants
  return 'picks'; // Coders, engineers, general → Cortex Picks
};

const Dashboard = () => {
  const { user } = useAuth();
  const location = useLocation();
  const {
    scholarships,
    stats,
    loading,
    discoveryStatus,
    discoveryProgress,
    triggerDiscovery,
  } = useScholarships();

  const [searchQuery, setSearchQuery] = useState('');
  const [view, setView] = useState<'grid' | 'list'>('grid');

  // isFirstVisit: true when coming straight from onboarding (Genesis State)
  const isFirstVisit = !!(location.state as any)?.triggerDiscovery;
  const [genesisPhase, setGenesisPhase] = useState<'hunting' | 'done'>(
    isFirstVisit ? 'hunting' : 'done'
  );
  const [genesisMessage, setGenesisMessage] = useState('Deploying your AI agents...');

  const profileType = useMemo(() => deriveProfileType(userProfile), [userProfile]);
  const defaultTab = useMemo(() => getDefaultTab(profileType), [profileType]);
  const [activeTab, setActiveTab] = useState('picks');

  const [locationScope, setLocationScope] = useState<LocationScope>('all');
  const [sourceScope, setSourceScope] = useState<SourceScope>('all');

  // Real-time WebSocket connection
  const {
    connected: wsConnected,
    opportunities: realtimeOpportunities,
    newOpportunitiesCount,
    clearNewOpportunitiesCount,
    flushBuffer,
    justFlushedIds,
  } = useRealtimeOpportunities();

  // User profile state - fetched from Firestore with localStorage fallback
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);

  // Fetch user profile from Firestore on mount
  useEffect(() => {
    const fetchProfile = async () => {
      if (!user?.uid) return;

      // --- HACKATHON GUEST OVERRIDE ---
      if (user.uid === 'demo_guest_user') {
        const syntheticProfile: UserProfile = {
          name: 'Musa Ibrahim',
          academic_status: 'Undergraduate',
          school: 'University of Lagos',
          major: 'Computer Science',
          gpa: '3.92',
          graduation_year: '2026',
          interests: ['Artificial Intelligence', 'Web3', 'Blockchain', 'Cybersecurity', 'Cloud Native', 'Quantum Computing'],
          financial_need: 25000,
          patrol_enabled: true
        };
        setUserProfile(syntheticProfile);
        return;
      }

      try {
        // Try Firestore (source of truth)
        if (db) {
          const userDoc = await getDoc(doc(db, 'users', user.uid));
          if (userDoc.exists()) {
            const userData = userDoc.data();
            const profile = userData?.profile;

            if (profile) {
              const formattedProfile: UserProfile = {
                name: `${profile.firstName || profile.name || ''} ${profile.lastName || ''}`.trim(),
                academic_status: profile.academicStatus || profile.academic_status,
                school: profile.school,
                gpa: profile.gpa,
                major: profile.major,
                interests: profile.interests || [],
                financial_need: profile.financialNeed || profile.financial_need || 0,
                country: profile.country,
                state: profile.state,
                city: profile.city,
              };
              setUserProfile(formattedProfile);
              // Sync to localStorage
              localStorage.setItem('scholarstream_profile', JSON.stringify(formattedProfile));
              console.log('✅ Profile loaded from Firestore');
              return;
            }
          }
        }
      } catch (error) {
        console.warn('Could not fetch profile from Firestore, using localStorage fallback');
      }

      // Fallback to localStorage if Firestore fails or doc doesn't exist
      const localProfile = localStorage.getItem('scholarstream_profile');
      if (localProfile) {
        try {
          setUserProfile(JSON.parse(localProfile));
          console.log('📱 Profile loaded from localStorage');
        } catch (e) {
          console.error('Error parsing profile from localStorage:', e);
        }
      }
    };

    fetchProfile();
  }, [user?.uid]);

  // Deep Scout Trigger: Explicitly hunt using the user's profile upon login
  useEffect(() => {
    if (!user?.uid || !userProfile) return;
    
    const hasScouted = sessionStorage.getItem(`scouted_${user.uid}`);
    if (!hasScouted) {
      sessionStorage.setItem(`scouted_${user.uid}`, 'true');
      fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8081'}/api/scholarships/scout-profile/${user.uid}`, {
        method: 'POST',
      }).catch(err => console.error("Failed to trigger scout:", err));
    }
  }, [user?.uid, userProfile]);

  // Genesis State: animate status messages while agents hunt on first visit
  useEffect(() => {
    if (!isFirstVisit || genesisPhase === 'done') return;
    const messages = [
      '🌐 Scanning DevPost, MLH, DoraHacks...',
      '🧬 Analyzing your Academic DNA...',
      '🤖 Deploying profile-specific drones...',
      '📡 Deep scanning Reddit & LinkedIn signals...',
      '⚡ Matching opportunities to your profile...',
      '✅ Your first matches are arriving!',
    ];
    let i = 0;
    const interval = setInterval(() => {
      i++;
      if (i < messages.length) {
        setGenesisMessage(messages[i]);
      } else {
        clearInterval(interval);
        setGenesisPhase('done');
      }
    }, 2500);
    return () => clearInterval(interval);
  }, [isFirstVisit, genesisPhase]);

  // Auto-upgrade tab to defaultTab once profile is known
  useEffect(() => {
    if (activeTab === 'picks') {
      setActiveTab(defaultTab);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [defaultTab]);

  // Combine, deduplicate, and rank all opportunities (real-time + cached)
  const allOpportunities = useMemo(() => {
    // 1. Merge sources
    const combined = [...realtimeOpportunities, ...scholarships];

    // 2. Deduplicate by ID
    const uniqueMap = new Map();
    combined.forEach(opp => {
      if (!uniqueMap.has(opp.id)) {
        uniqueMap.set(opp.id, opp);
      }
    });
    const uniqueList = Array.from(uniqueMap.values());

    if (uniqueList.length === 0) return [];

    // 3. Apply Matching Engine for consistent scoring across both sources
    if (userProfile) {
      return matchingEngine.rankOpportunities(uniqueList, userProfile as any);
    }

    // Fallback for users without profile
    return uniqueList.map(s => ({
      ...s,
      match_score: s.match_score || 50,
      match_tier: s.match_tier || 'potential'
    }));
  }, [realtimeOpportunities, scholarships, userProfile]);

  // Trigger discovery if coming from onboarding
  useEffect(() => {
    const state = location.state as { triggerDiscovery?: boolean; profileData?: any };
    if (state?.triggerDiscovery && state?.profileData && user?.uid) {
      const userProfileData: UserProfile = {
        name: `${state.profileData.firstName} ${state.profileData.lastName}`,
        academic_status: state.profileData.academicStatus,
        school: state.profileData.school,
        year: state.profileData.year,
        gpa: state.profileData.gpa,
        major: state.profileData.major,
        graduation_year: state.profileData.graduationYear,
        background: state.profileData.background,
        financial_need: state.profileData.financialNeed,
        interests: state.profileData.interests,
        country: state.profileData.country,
        state: state.profileData.state,
        city: state.profileData.city,
      };

      triggerDiscovery(userProfileData);

      // Clear the state to prevent re-triggering on refresh
      window.history.replaceState({}, document.title);
    }
  }, [location.state, user, triggerDiscovery]);

  const getUserName = () => {
    if (userProfile?.name) return userProfile.name.split(' ')[0];
    return user?.name?.split(' ')[0] || 'there';
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  // Helper function to infer opportunity type from tags/description
  const inferOpportunityType = (opp: any): 'scholarship' | 'hackathon' | 'bounty' | 'competition' => {
    const tags = (opp.tags || []).map((t: string) => t.toLowerCase());
    const desc = (opp.description || '').toLowerCase();
    const name = (opp.name || '').toLowerCase();
    const combined = `${tags.join(' ')} ${desc} ${name}`;

    // Check source_type first (if explicitly set)
    const sourceType = (opp.source_type || '').toLowerCase();
    if (sourceType === 'devpost' || sourceType === 'mlh') return 'hackathon';
    if (sourceType === 'gitcoin') return 'bounty';
    if (sourceType === 'kaggle') return 'competition';

    // Infer from content
    if (combined.includes('hackathon') || combined.includes('hack ') || combined.includes('devpost')) {
      return 'hackathon';
    }
    if (combined.includes('bounty') || combined.includes('bug bounty') || combined.includes('security') || combined.includes('gitcoin')) {
      return 'bounty';
    }
    if (combined.includes('competition') || combined.includes('contest') || combined.includes('kaggle') || combined.includes('challenge')) {
      return 'competition';
    }

    return 'scholarship';
  };

  // Smart grouping with Search & Location logic
  const groupedOpportunities = useMemo(() => {
    let filtered = allOpportunities;

    // 1. Search Filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        opp =>
          opp.title?.toLowerCase().includes(query) ||
          opp.name?.toLowerCase().includes(query) ||
          opp.organization?.toLowerCase().includes(query) ||
          opp.description?.toLowerCase().includes(query) ||
          (opp.tags || []).some((t: string) => t.toLowerCase().includes(query))
      );
    }

    // 2. Location Scope Filter
    filtered = filterByLocation(filtered, locationScope, userProfile);

    // 3. Source Scope Filter
    if (sourceScope !== 'all') {
      filtered = filtered.filter(opp => {
        const tier = opp.source_tier || 'Standard';
        if (sourceScope === 'atomic') return tier === 'Atomic Source';
        if (sourceScope === 'aggregator') return tier === 'Aggregator';
        return true;
      });
    }

    // 4. Sort by Location Relevance (High Depth first)
    filtered = sortByLocationRelevance(filtered, locationScope, userProfile);

    // 5. Diversity Guard: Cap aggregators if they dominate
    const aggregatorCount: Record<string, number> = {};
    const diversified = [];
    
    for (const opp of filtered) {
      const isAggregator = (opp.source_tier === 'Aggregator');
      if (isAggregator) {
        const domain = new URL(opp.source_url || '').hostname;
        aggregatorCount[domain] = (aggregatorCount[domain] || 0) + 1;
        if (aggregatorCount[domain] <= 2) {
          diversified.push(opp);
        }
      } else {
        diversified.push(opp);
      }
    }

    const finalFiltered = diversified;

    // 6. Cortex Picks (Atomic Sources + High Match)
    const picks = finalFiltered.filter(opp => 
      opp.source_tier === 'Atomic Source' || 
      (opp.match_score && opp.match_score >= 80) ||
      (opp.organization && opp.organization.includes('Foundation')) ||
      (opp.source_url && opp.source_url.includes('.edu'))
    );

    return {
      all: finalFiltered,
      picks: picks,
      scholarships: finalFiltered.filter(opp => inferOpportunityType(opp) === 'scholarship'),
      hackathons: finalFiltered.filter(opp => inferOpportunityType(opp) === 'hackathon'),
      bounties: finalFiltered.filter(opp => inferOpportunityType(opp) === 'bounty'),
      competitions: finalFiltered.filter(opp => inferOpportunityType(opp) === 'competition')
    };
  }, [allOpportunities, searchQuery, locationScope, sourceScope, userProfile, realtimeOpportunities]);

  const urgentScholarships = useMemo(() => {
    return allOpportunities.filter(s => calculateDaysUntilDeadline(s.deadline) <= 7);
  }, [allOpportunities]);

  // Get current tab opportunities
  const getCurrentTabOpportunities = () => {
    switch (activeTab) {
      case 'picks': return groupedOpportunities.picks;
      case 'scholarships': return groupedOpportunities.scholarships;
      case 'hackathons': return groupedOpportunities.hackathons;
      case 'bounties': return groupedOpportunities.bounties;
      case 'competitions': return groupedOpportunities.competitions;
      default: return groupedOpportunities.all;
    }
  };

  const currentOpportunities = getCurrentTabOpportunities();

  if (loading || (discoveryStatus === 'processing' && allOpportunities.length === 0)) {
    return (
      <div className="min-h-screen bg-background">
        <DashboardHeader />
        <main className="container mx-auto px-4 py-8">
          <div className="space-y-8">
             <MissionControlConsole />
             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-32 rounded-xl" />)}
             </div>
             <div className="space-y-4">
                <Skeleton className="h-10 w-48" />
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                   {[1, 2, 3, 4, 5, 6].map(i => <SkeletonCard key={i} />)}
                </div>
             </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto px-4 py-8 pb-24 md:pb-8">
        <div className="flex flex-col space-y-8">
          
          {/* Hero Section */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">
                {getGreeting()}, {getUserName()}!
              </h1>
              <p className="text-muted-foreground flex items-center mt-1">
                <Sparkles className="w-4 h-4 mr-2 text-primary" />
                Cortex V3 has identified {allOpportunities.length} opportunities for you today.
              </p>
            </div>
            <div className="flex items-center space-x-2">
               <DiscoveryPulseIndicator status={discoveryStatus} progress={discoveryProgress} />
               <ViewToggle view={view} onViewChange={setView} />
            </div>
          </div>

          {/* Genesis State Banner — shown while agents are hunting for brand-new users */}
          {isFirstVisit && genesisPhase === 'hunting' && (
            <div className="relative overflow-hidden rounded-2xl border border-emerald-500/30 bg-gradient-to-br from-emerald-950/60 via-black/40 to-teal-950/40 p-6 backdrop-blur-xl">
              {/* Animated background pulse */}
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 via-transparent to-teal-500/5 animate-pulse" />
              <div className="relative flex items-center gap-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-emerald-400 animate-spin" style={{ animationDuration: '3s' }} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-bold text-emerald-300 mb-1">Your AI Agents Are Hunting Live</h3>
                  <p className="text-sm text-emerald-400/80 animate-pulse">{genesisMessage}</p>
                </div>
                <div className="hidden md:flex items-center gap-1.5 text-xs text-emerald-500/60">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span>LIVE</span>
                </div>
              </div>
              <div className="mt-4 flex gap-2">
                {['DevPost', 'MLH', 'Reddit', 'LinkedIn', 'Kaggle'].map((src, i) => (
                  <span key={src} className="text-[10px] px-2 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                    style={{ animationDelay: `${i * 300}ms` }}>
                    {src}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Mission Control Console (Telemetry) */}
          <MissionControlConsole opportunities={allOpportunities} />

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatsCard
              label="Total Matches"
              value={stats.total_count}
              icon={Target}
              iconColor="text-primary"
            />
            <StatsCard
              label="Funding Potential"
              value={formatCurrency(stats.total_value)}
              icon={DollarSign}
              iconColor="text-emerald-500"
            />
            <StatsCard
              label="Active Hunts"
              value={wsConnected ? "15" : "0"}
              icon={Wifi}
              iconColor={wsConnected ? "text-blue-500" : "text-zinc-500"}
            />
            <StatsCard
              label="Expiring Soon"
              value={allOpportunities.filter(s => calculateDaysUntilDeadline(s.deadline) <= 7).length}
              icon={Clock}
              iconColor="text-amber-500"
            />
          </div>

          {/* Priority Alerts */}
          <PriorityAlertsSection urgentScholarships={urgentScholarships} />

          {/* Main Content Area */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Left Column: Opportunities */}
            <div className="lg:col-span-8 space-y-6">
              {/* Filters & Search */}
              <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-card/50 p-4 rounded-xl border border-border/50">
                <div className="relative w-full md:w-96">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search titles, skills, or organizations..."
                    className="pl-10"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
                <div className="flex items-center space-x-2 w-full md:w-auto">
                   <LocationFilter scope={locationScope} onScopeChange={setLocationScope} />
                   <SourceFilter scope={sourceScope} onScopeChange={setSourceScope} />
                </div>
              </div>

              {/* Tabs & Content */}
              <Tabs defaultValue="picks" value={activeTab} onValueChange={setActiveTab} className="w-full">
                <div className="flex items-center justify-between mb-4 overflow-x-auto pb-2 scrollbar-hide">
                  <TabsList className="bg-muted/50 border border-border/50">
                    <TabsTrigger value="picks" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground font-bold">
                      <Sparkles className="w-3.5 h-3.5 mr-1.5" /> Cortex Picks <Badge variant="secondary" className="ml-2 bg-white/10">{groupedOpportunities.picks.length}</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="all">
                      All <Badge variant="secondary" className="ml-2 bg-white/10">{groupedOpportunities.all.length}</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="scholarships">
                      Scholarships <Badge variant="secondary" className="ml-2 bg-white/10">{groupedOpportunities.scholarships.length}</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="hackathons">
                      Hackathons <Badge variant="secondary" className="ml-2 bg-white/10">{groupedOpportunities.hackathons.length}</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="bounties">
                      Bounties <Badge variant="secondary" className="ml-2 bg-white/10">{groupedOpportunities.bounties.length}</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="competitions">
                      Kaggle/Earn <Badge variant="secondary" className="ml-2 bg-white/10">{groupedOpportunities.competitions.length}</Badge>
                    </TabsTrigger>
                  </TabsList>
                </div>

                {newOpportunitiesCount > 0 && (
                   <NotificationPill 
                    count={newOpportunitiesCount} 
                    onClick={() => {
                        flushBuffer();
                        clearNewOpportunitiesCount();
                    }} 
                   />
                )}

                <TabsContent value={activeTab} className="mt-0">
                  {activeTab === 'picks' ? (
                    <CortexSourceGroup opportunities={groupedOpportunities.picks} />
                  ) : currentOpportunities && currentOpportunities.length > 0 ? (
                    view === 'grid' ? (
                      <PaginatedGrid 
                        opportunities={currentOpportunities} 
                        justFlushedIds={justFlushedIds}
                      />
                    ) : (
                      <SimpleOpportunityGrid opportunities={currentOpportunities} />
                    )
                  ) : (
                    <div className="flex flex-col items-center justify-center py-20 text-center bg-card/30 rounded-3xl border-2 border-dashed border-border/50">
                      <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
                        <FileText className="w-8 h-8 text-muted-foreground" />
                      </div>
                      <h3 className="text-xl font-bold">No opportunities found</h3>
                      <p className="text-muted-foreground max-w-md mx-auto mt-2">
                        {searchQuery 
                          ? `We couldn't find any results matching "${searchQuery}". Try broadening your search.`
                          : "Cortex V3 is still scanning deep web signals. New matches will appear here in real-time."}
                      </p>
                      {searchQuery && (
                        <Button variant="outline" className="mt-6" onClick={() => setSearchQuery('')}>
                          Clear Search
                        </Button>
                      )}
                    </div>
                  )}
                </TabsContent>
              </Tabs>
            </div>

            {/* Right Column: Intelligence Widgets */}
            <div className="lg:col-span-4 space-y-8">
              <LiveHunterWidget />
              <FinancialImpactWidget stats={stats} />
              <QuickActionsWidget />
              <ActivityFeedWidget />
            </div>
          </div>
        </div>
      </main>

      <MobileBottomNav />
      <FloatingChatAssistant />
    </div>
  );
};

export default Dashboard;