"use client";

import { ThemeProvider } from '@/contexts/ThemeContext';
import Sidebar from '@/components/Sidebar';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <div className="flex h-screen overflow-hidden bg-white dark:bg-gray-900">
        {/* Sidebar */}
        <div className="hidden md:flex md:w-64 md:flex-col">
          <Sidebar />
        </div>
        
        {/* Main content */}
        <div className="flex flex-1 flex-col overflow-hidden">
          <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900 p-6">
            {children}
          </main>
        </div>
      </div>
    </ThemeProvider>
  );
}
