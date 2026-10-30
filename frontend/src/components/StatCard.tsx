import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  colorScheme?: 'green' | 'red' | 'amber' | 'blue';
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  colorScheme = 'green'
}) => {
  const styles = {
    green: {
      bg: 'bg-emerald-50/70',
      border: 'border-emerald-200/80',
      text: 'text-emerald-800',
      iconBg: 'bg-emerald-600',
      iconColor: 'text-white'
    },
    red: {
      bg: 'bg-rose-50/70',
      border: 'border-rose-200/80',
      text: 'text-rose-800',
      iconBg: 'bg-rose-600',
      iconColor: 'text-white'
    },
    amber: {
      bg: 'bg-amber-50/70',
      border: 'border-amber-200/80',
      text: 'text-amber-800',
      iconBg: 'bg-amber-600',
      iconColor: 'text-white'
    },
    blue: {
      bg: 'bg-sky-50/70',
      border: 'border-sky-200/80',
      text: 'text-sky-800',
      iconBg: 'bg-sky-600',
      iconColor: 'text-white'
    }
  }[colorScheme];

  return (
    <div className={`rounded-2xl p-5 border ${styles.border} ${styles.bg} shadow-xs transition-all hover:shadow-md`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            {title}
          </p>
          <p className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {value}
          </p>
          {subtitle && (
            <p className="text-xs text-slate-500 mt-1 font-medium">
              {subtitle}
            </p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl ${styles.iconBg} ${styles.iconColor} flex items-center justify-center shadow-xs shrink-0`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
};
