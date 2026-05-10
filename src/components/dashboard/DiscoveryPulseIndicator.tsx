
import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Radar, CheckCircle, Zap } from 'lucide-react';
import { useDiscoveryPulse } from '@/hooks/useDiscoveryPulse';

export const DiscoveryPulseIndicator: React.FC = () => {
    const { status, missions } = useDiscoveryPulse();
    const [visible, setVisible] = useState(true);

    // Only show the single most recent mission, not all of them
    const latestMission = missions[0] || null;

    // Auto-dismiss completed missions after 4 seconds
    useEffect(() => {
        if (latestMission?.status === 'completed') {
            const timer = setTimeout(() => setVisible(false), 4000);
            return () => clearTimeout(timer);
        } else {
            setVisible(true);
        }
    }, [latestMission?.mission_id, latestMission?.status]);

    if (!latestMission || !visible) return null;

    const isActive = latestMission.status === 'active';
    const labelText = latestMission.label || '';

    // Truncate label intelligently
    const truncated = labelText.length > 52 ? labelText.slice(0, 52) + '…' : labelText;

    return (
        <div className="fixed bottom-6 right-6 z-50 pointer-events-none">
            <AnimatePresence mode="wait">
                <motion.div
                    key={latestMission.mission_id + latestMission.status}
                    initial={{ opacity: 0, y: 16, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 8, scale: 0.95 }}
                    transition={{ duration: 0.25, ease: 'easeOut' }}
                    className={`flex items-center space-x-3 px-4 py-2.5 rounded-xl shadow-2xl backdrop-blur-xl border max-w-[280px] ${
                        isActive
                            ? 'bg-blue-950/80 border-blue-500/30 text-blue-300'
                            : 'bg-emerald-950/80 border-emerald-500/30 text-emerald-300'
                    }`}
                >
                    {/* Icon */}
                    <div className="shrink-0">
                        {isActive ? (
                            <motion.div
                                animate={{ rotate: 360 }}
                                transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                            >
                                <Radar className="w-4 h-4 text-blue-400" />
                            </motion.div>
                        ) : (
                            <CheckCircle className="w-4 h-4 text-emerald-400" />
                        )}
                    </div>

                    {/* Text */}
                    <div className="flex flex-col min-w-0">
                        <span className="text-[10px] font-bold uppercase tracking-widest opacity-60">
                            {isActive ? 'Live Discovery' : 'Capture Success'}
                        </span>
                        <span className="text-[11px] font-medium leading-tight mt-0.5 truncate">
                            {truncated}
                        </span>
                    </div>

                    {/* Active pulse bars */}
                    {isActive && (
                        <div className="flex space-x-0.5 shrink-0 pl-1">
                            {[0, 1, 2].map((i) => (
                                <motion.div
                                    key={i}
                                    className="w-0.5 rounded-full bg-blue-400/50"
                                    animate={{ height: [4, 10, 4] }}
                                    transition={{ duration: 0.7, repeat: Infinity, delay: i * 0.15 }}
                                />
                            ))}
                        </div>
                    )}
                </motion.div>
            </AnimatePresence>

            {/* Status strip */}
            {status === 'active' && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mt-1.5 flex items-center justify-end space-x-1.5"
                >
                    <Zap className="w-2.5 h-2.5 text-yellow-400 animate-pulse" />
                    <span className="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">
                        Sentinel Active
                    </span>
                </motion.div>
            )}
        </div>
    );
};
