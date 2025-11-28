import Link from 'next/link';
import { Clock, BarChart3, Settings, Calendar } from 'lucide-react';

interface MainLayoutProps {
  children: React.ReactNode;
}

const navItems = [
  { href: '/', label: 'Dashboard', icon: Clock },
  { href: '/schedules', label: 'Horaires', icon: Calendar },
  { href: '/statistics', label: 'Statistiques', icon: BarChart3 },
  { href: '/config', label: 'Configuration', icon: Settings },
];

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <Clock className="h-6 w-6" />
              <h1 className="text-2xl font-bold">Gestion des Horaires</h1>
            </Link>
            <nav className="flex space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className="flex items-center space-x-2 px-4 py-2 rounded-md hover:bg-accent transition-colors"
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}
