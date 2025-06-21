/**
 * Utility function to combine class names
 * Filters out falsy values and joins class names with spaces
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
} 