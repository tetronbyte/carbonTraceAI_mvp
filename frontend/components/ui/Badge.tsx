import clsx from 'clsx';

export function Badge({
  className,
  children,
}: { className?: string; children: React.ReactNode }) {
  return (
    <span className={clsx('pill', className)}>{children}</span>
  );
}
