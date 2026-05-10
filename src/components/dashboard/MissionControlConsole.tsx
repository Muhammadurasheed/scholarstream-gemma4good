
import React, { useEffect, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, Shield, Radar, Zap, Activity, Cpu, Search, Sparkles, Database, Network } from 'lucide-react';
import { useDiscoveryPulse } from '@/hooks/useDiscoveryPulse';
import { Scholarship } from '@/types/scholarship';

interface MissionControlConsoleProps {
  opportunities?: Scholarship[];
}

export const MissionControlConsole: React.FC<MissionControlConsoleProps> = ({ opportunities = [] }) => {
  const { status, missions } = useDiscoveryPulse();
  const [logs, setLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll terminal
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  // Initializing logs & Dynamic telemetry
  useEffect(() => {
    const dynamicLogs = [
      "Initializing Cortex V3 'Deep Scout' Mission...",
      "Auth Verified: Gemma 4 Good Native Engine",
      "Analyzing User Profile (Musa Ibrahim)...",
      "Digital DNA identified: CS Undergraduate / AI Specialist",
      "Geolocation strategy: 40/30/30 (Global/Continental/Local)",
      "Sentinel Patrolling Hidden Corners (Reddit, LinkedIn, X)...",
      "[THINKING] User has strong interests in Blockchain/AI.",
      "[THINKING] Targeting Ethereum Foundation & NVIDIA Research portals...",
      "[REASONING] Prioritizing .edu domains for Atomic Source authenticity.",
      "[SYSTEM] Deep web scan initialization complete.",
      "[SYSTEM] Real-time hunting stream connected."
    ];
    
    let i = 0;
    const interval = setInterval(() => {
      if (i < dynamicLogs.length) {
        const logLine = dynamicLogs[i];
        if (logLine) {
          const prefix = logLine.includes('[THINKING]') || logLine.includes('[REASONING]') ? '🧠' : logLine.includes('[SCOUT]') ? '📡' : '[SYSTEM]';
          const content = logLine.replace(/\[.*?\] /, '');
          setLogs(prev => [...prev, `${prefix} ${content}`]);
        }
        i++;
      } else {
        clearInterval(interval);
      }
    }, 400); // Faster typing for better UX

    return () => clearInterval(interval);
  }, []); // Run exactly once on mount!

  // Transform live missions into terminal logs
  useEffect(() => {
    if (missions.length > 0) {
      const latest = missions[0];
      const timestamp = new Date().toLocaleTimeString([], { hour12: false });
      const newLog = `[${timestamp}] ${latest.label}`;
      
      setLogs(prev => {
        if (prev[prev.length - 1] === newLog) return prev;
        return [...prev.slice(-15), newLog]; // Keep last 15 logs
      });
    }
  }, [missions]);

  return (
    <div className="w-full max-w-5xl mx-auto mt-8 relative">
      {/* Premium Glow Effect (Apple + DeepMind Vibe) */}
      <div className="absolute -inset-1.5 bg-gradient-to-r from-cyan-500/20 via-blue-600/20 to-purple-500/20 rounded-2xl blur-2xl opacity-60 pointer-events-none" />
      
      <div className="relative bg-black/90 backdrop-blur-xl rounded-2xl border border-white/10 shadow-[0_0_40px_rgba(0,0,0,0.8)] overflow-hidden font-mono text-xs md:text-sm">
        
        {/* Subtle top glare */}
        <div className="absolute top-0 inset-x-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />

        {/* Console Header */}
        <div className="flex items-center justify-between px-5 py-3 bg-white/[0.02] border-b border-white/5 backdrop-blur-md">
          <div className="flex items-center space-x-3">
            <div className="flex space-x-1.5">
              <div className="w-3 h-3 rounded-full bg-[#FF5F56] shadow-[0_0_10px_rgba(255,95,86,0.5)]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E] shadow-[0_0_10px_rgba(255,189,46,0.5)]" />
              <div className="w-3 h-3 rounded-full bg-[#27C93F] shadow-[0_0_10px_rgba(39,201,63,0.5)]" />
            </div>
            <span className="text-zinc-400 text-[10px] uppercase tracking-widest font-bold ml-2">
              ScholarStream Mission Control
            </span>
          </div>
          <div className="flex items-center space-x-3">
             <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400">
               <Cpu className="w-3 h-3 animate-pulse" />
               <span className="text-[10px] font-bold tracking-wider">GEMMA 4 NATIVE</span>
             </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="p-6 lg:p-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Log (Left 2 Columns) */}
          <div className="lg:col-span-2 flex flex-col space-y-4 relative">
            <div className="flex items-center space-x-2 text-zinc-400 mb-2">
              <Terminal className="w-4 h-4 text-cyan-400" />
              <span className="text-[10px] uppercase font-bold text-zinc-500 tracking-widest">Live Telemetry Feed</span>
            </div>
            
            <div 
              ref={scrollRef}
              className="h-64 overflow-y-auto space-y-2.5 scrollbar-hide scroll-smooth pr-4 relative z-10"
            >
              <AnimatePresence mode="popLayout">
                {logs.map((log, idx) => {
                  const isScout = log.includes('📡');
                  const isReasoning = log.includes('🧠');
                  const isSystem = log.includes('[SYSTEM]');
                  
                  return (
                    <motion.div
                      key={log + idx}
                      initial={{ opacity: 0, x: -10, filter: 'blur(4px)' }}
                      animate={{ opacity: 1, x: 0, filter: 'blur(0px)' }}
                      transition={{ duration: 0.3 }}
                      className={`font-mono text-[13px] leading-relaxed ${
                        isScout ? 'text-cyan-300 font-medium' : 
                        isReasoning ? 'text-purple-300' : 
                        isSystem ? 'text-zinc-500' : 'text-blue-400'
                      }`}
                    >
                      <span className="mr-3 opacity-30 select-none text-white">❯</span>
                      {log}
                    </motion.div>
                  )
                })}
              </AnimatePresence>
              {status === 'active' && (
                <motion.div 
                  animate={{ opacity: [0, 1, 0] }}
                  transition={{ repeat: Infinity, duration: 0.8 }}
                  className="inline-block w-2.5 h-4 bg-cyan-400 ml-1 translate-y-1 shadow-[0_0_8px_rgba(34,211,238,0.8)]"
                />
              )}
            </div>
            
            {/* Fade out for text overflow */}
            <div className="absolute bottom-0 inset-x-0 h-12 bg-gradient-to-t from-black via-black/80 to-transparent pointer-events-none z-20" />
          </div>

          {/* Status Panel (Right Column) */}
          <div className="lg:col-span-1 space-y-6 flex flex-col justify-center relative z-10">
            {/* Visualizer 1: Complex Radar */}
            <div className="bg-white/[0.02] rounded-2xl p-6 border border-white/5 flex flex-col items-center justify-center space-y-4 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                
                <div className="relative h-32 w-32 flex items-center justify-center">
                    {/* Outer slow ring */}
                    <motion.div 
                        className="absolute inset-0 border border-cyan-500/20 rounded-full border-dashed"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    />
                    {/* Middle pulse ring */}
                    <motion.div 
                        className="absolute inset-2 border-2 border-cyan-500/30 rounded-full"
                        animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
                        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                    />
                    {/* Inner fast ring */}
                    <motion.div 
                        className="absolute inset-6 border border-purple-500/40 rounded-full"
                        animate={{ rotate: -360 }}
                        transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                    />
                    <Radar className="w-8 h-8 text-cyan-400 absolute" />
                    
                    {/* Scanning beam */}
                    <motion.div 
                      className="absolute inset-0 rounded-full bg-gradient-to-tr from-transparent via-cyan-500/10 to-transparent"
                      animate={{ rotate: 360 }}
                      transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                      style={{ originX: '50%', originY: '50%' }}
                    />
                </div>
                <div className="text-center z-10">
                    <div className="text-[10px] text-zinc-400 font-bold uppercase mb-1 tracking-widest">Global Patrol</div>
                    <div className="text-xs text-cyan-400 font-black tracking-widest">SENTINEL-ACTIVE</div>
                </div>
            </div>

            {/* Visualizer 2: Metrics */}
            <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/[0.02] rounded-xl p-4 border border-white/5 relative overflow-hidden group hover:border-emerald-500/30 transition-colors">
                    <div className="absolute inset-0 bg-emerald-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                    <div className="flex items-center space-x-2 mb-2">
                        <Activity className="w-3.5 h-3.5 text-emerald-500" />
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">Signal</span>
                    </div>
                    <div className="text-lg font-black text-emerald-400">STABLE</div>
                </div>
                <div className="bg-white/[0.02] rounded-xl p-4 border border-white/5 relative overflow-hidden group hover:border-yellow-500/30 transition-colors">
                    <div className="absolute inset-0 bg-yellow-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                    <div className="flex items-center space-x-2 mb-2">
                        <Network className="w-3.5 h-3.5 text-yellow-500" />
                        <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">Threads</span>
                    </div>
                    <div className="text-lg font-black text-yellow-400">128<span className="text-xs text-yellow-500/50">/s</span></div>
                </div>
            </div>
          </div>
        </div>

        {/* Console Footer */}
        <div className="px-6 py-3 bg-black/60 border-t border-white/5 flex items-center justify-between text-[10px] backdrop-blur-xl">
           <div className="flex items-center space-x-6">
              <span className="text-zinc-500 font-medium tracking-wider">ENGINE: <span className="text-zinc-200 font-bold">CORTEX_V3</span></span>
              <span className="text-zinc-500 font-medium tracking-wider">MODE: <span className="text-cyan-400 font-bold">DEEP_SCOUT</span></span>
              <span className="text-zinc-500 font-medium tracking-wider">TOTAL EXTRACTED: <span className="text-purple-400 font-bold">{opportunities.length}</span></span>
           </div>
           <div className="flex items-center space-x-2.5">
              <motion.div 
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.8)]" 
              />
              <span className="text-emerald-500 font-bold uppercase tracking-widest">Secure Link Active</span>
           </div>
        </div>
      </div>
    </div>
  );
};

