
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Radar, Zap, Shield, Search, Globe, Target } from 'lucide-react';
import { useDiscoveryPulse } from '@/hooks/useDiscoveryPulse';

export const LiveHunterWidget: React.FC = () => {
    const { missions } = useDiscoveryPulse();
    const activeMissions = missions.filter(m => m.status === 'active');
    
    return (
        <div className="bg-zinc-900/40 backdrop-blur-md rounded-2xl border border-white/5 overflow-hidden shadow-xl h-[500px] flex flex-col">
            <div className="px-4 py-3 border-b border-white/5 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                    <div className="relative">
                        <Radar className="w-4 h-4 text-primary" />
                        <motion.div 
                            className="absolute inset-0 bg-primary/20 rounded-full"
                            animate={{ scale: [1, 2], opacity: [1, 0] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                        />
                    </div>
                    <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Agentic Patrols</span>
                </div>
                <div className="flex items-center space-x-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-[9px] text-emerald-500 font-bold">LIVE</span>
                </div>
            </div>

            <div className="p-4 flex flex-col flex-grow overflow-hidden">
                <div className="flex-grow overflow-y-auto space-y-4 pr-2 custom-scrollbar">
                <AnimatePresence mode="popLayout">
                    {activeMissions.length > 0 ? (
                        activeMissions.map((mission) => (
                            <motion.div
                                key={mission.mission_id}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 10 }}
                                className="space-y-2"
                            >
                                <div className="flex items-center justify-between text-[10px]">
                                    <span className="text-zinc-500 font-medium">TARGET:</span>
                                    <span className="text-blue-400 font-bold truncate max-w-[120px]">
                                        {mission.target.replace('https://', '').split('/')[0]}
                                    </span>
                                </div>
                                <div className="h-1 w-full bg-zinc-800 rounded-full overflow-hidden">
                                    <motion.div 
                                        className="h-full bg-primary"
                                        animate={{ x: [-100, 100] }}
                                        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                                    />
                                </div>
                                <div className="text-[9px] text-zinc-500 italic">
                                    {mission.label}
                                </div>
                            </motion.div>
                        ))
                    ) : (
                        <div className="py-4 text-center space-y-2">
                            <Shield className="w-8 h-8 text-zinc-700 mx-auto opacity-30" />
                            <p className="text-[10px] text-zinc-600 font-medium">
                                Standing by for next deployment...
                            </p>
                        </div>
                    )}
                </AnimatePresence>
                </div>

                <div className="pt-4 border-t border-white/5 flex-shrink-0">
                    <div className="bg-zinc-950/50 rounded-xl p-3 border border-white/5 space-y-2">
                        <div className="flex items-center space-x-2 text-[10px] font-bold text-zinc-500">
                            <Globe className="w-3 h-3" />
                            <span>SOURCE RELEVANCE</span>
                        </div>
                        <div className="grid grid-cols-2 gap-2">
                            <div className="space-y-1">
                                <div className="text-[8px] text-zinc-600">Atomic (.edu)</div>
                                <div className="text-xs font-bold text-primary">PRIORITY</div>
                            </div>
                            <div className="space-y-1">
                                <div className="text-[8px] text-zinc-600">Dork Strategy</div>
                                <div className="text-xs font-bold text-zinc-400">DEEP_SCOUT</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
