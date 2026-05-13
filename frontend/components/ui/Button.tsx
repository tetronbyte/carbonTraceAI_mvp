'use client';

import clsx from 'clsx';
import { ButtonHTMLAttributes, forwardRef } from 'react';

type Variant = 'primary' | 'secondary' | 'ghost';
type Size = 'sm' | 'md' | 'lg';

const styles: Record<Variant, string> = {
  primary:
    'bg-accent text-white shadow-glow-accent hover:bg-accent-glow active:scale-[0.98]',
  secondary:
    'bg-ink-700/60 text-ink-100 border border-white/10 hover:bg-ink-700 hover:border-white/20',
  ghost:
    'text-ink-300 hover:bg-white/5 hover:text-ink-100',
};
const sizes: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
};

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
}

export const Button = forwardRef<HTMLButtonElement, Props>(
  ({ variant = 'primary', size = 'md', className, ...rest }, ref) => (
    <button
      ref={ref}
      className={clsx(
        'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all',
        'focus:outline-none focus:ring-2 focus:ring-accent/40',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        styles[variant],
        sizes[size],
        className
      )}
      {...rest}
    />
  )
);
Button.displayName = 'Button';
