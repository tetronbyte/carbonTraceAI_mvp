import clsx from 'clsx';

export function Card({
  className,
  children,
}: { className?: string; children: React.ReactNode }) {
  return (
    <div className={clsx('glass rounded-xl p-6', className)}>{children}</div>
  );
}

export function CardHeader({
  title,
  subtitle,
  right,
}: { title: string; subtitle?: string; right?: React.ReactNode }) {
  return (
    <div className="flex items-start justify-between mb-4">
      <div>
        <h3 className="text-sm font-medium text-ink-300 uppercase tracking-wider">{title}</h3>
        {subtitle && <p className="text-xs text-ink-400 mt-1">{subtitle}</p>}
      </div>
      {right}
    </div>
  );
}
