'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import ThemeToggle from './ThemeToggle';

const navigation = [
  { name: 'Dashboard', href: '/', icon: '📊' },
  { name: 'Signals', href: '/signals', icon: '📈' },
  { name: 'Portfolio', href: '/portfolio', icon: '💼' },
  { name: 'Data Management', href: '/data-management', icon: '🗄️' },
  { name: 'Settings', href: '/settings', icon: '⚙️' },
  { name: 'About', href: '/about', icon: '📖' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full flex-col bg-gray-900 dark:bg-gray-950 text-white border-r border-gray-800 dark:border-gray-700">
      <div className="flex h-16 items-center justify-between px-4 border-b border-gray-800 dark:border-gray-700">
        <h1 className="text-xl font-bold">SentimentAlpha</h1>
        <ThemeToggle />
      </div>
      <nav className="flex-1 space-y-1 px-2 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`
                flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium
                transition-colors duration-150
                ${isActive 
                  ? 'bg-gray-800 dark:bg-gray-800 text-white' 
                  : 'text-gray-300 dark:text-gray-400 hover:bg-gray-800 dark:hover:bg-gray-800 hover:text-white'
                }
              `}
            >
              <span className="text-lg">{item.icon}</span>
              {item.name}
            </Link>
          );
        })}
      </nav>
      <div className="border-t border-gray-800 dark:border-gray-700 p-4">
        <p className="text-xs text-gray-400 dark:text-gray-500">Vietnam Stock Market Analytics</p>
      </div>
    </div>
  );
}
