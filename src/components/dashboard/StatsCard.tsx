import { LucideIcon } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface StatsCardProps {
  icon: LucideIcon;
  value: string | number;
  label: string;
  iconColor?: string;
  onClick?: () => void;
}

import { motion } from 'framer-motion';

export const StatsCard = ({ icon: Icon, value, label, iconColor = 'text-primary', onClick }: StatsCardProps) => {
  return (
    <motion.div
      whileHover={onClick ? { y: -4, scale: 1.02 } : { y: -4 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={cn(
        'group relative overflow-hidden rounded-2xl p-6 transition-colors duration-500',
        'bg-white/5 dark:bg-zinc-900/40 backdrop-blur-xl border border-white/10 dark:border-white/5',
        'hover:bg-white/10 dark:hover:bg-zinc-800/60 hover:border-white/20 dark:hover:border-white/10 hover:shadow-[0_8px_30px_rgb(0,0,0,0.12)]',
        onClick && 'cursor-pointer'
      )}
      onClick={onClick}
    >
      {/* Subtle background glow on hover */}
      <div className="absolute -inset-2 bg-gradient-to-br from-primary/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500" />
      
      <div className="relative z-10 flex flex-col gap-4">
        <div className="flex items-start justify-between">
          <div className={cn('rounded-xl bg-white/10 dark:bg-black/20 p-2.5 backdrop-blur-md shadow-sm', iconColor)}>
            <Icon className="h-5 w-5" />
          </div>
        </div>
        <div>
          <div className="text-3xl font-black text-foreground tracking-tight truncate drop-shadow-sm">{value}</div>
          <p className="text-sm font-medium text-muted-foreground mt-1 tracking-wide uppercase opacity-80">{label}</p>
        </div>
      </div>
    </motion.div>
  );
};
