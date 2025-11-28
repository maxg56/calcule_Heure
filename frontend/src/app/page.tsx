'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ScheduleForm } from '@/components/forms/ScheduleForm';
import { api } from '@/lib/api';
import type { Statistics, Schedule } from '@/types';
import { Clock, Calendar, TrendingUp, Coffee } from 'lucide-react';

export default function HomePage() {
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [recentSchedules, setRecentSchedules] = useState<Schedule[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [stats, schedules] = await Promise.all([
        api.getStatistics(),
        api.getSchedules(),
      ]);
      setStatistics(stats);
      setRecentSchedules(schedules.slice(-5).reverse());
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleScheduleAdded = () => {
    loadData();
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
        <p className="text-muted-foreground">
          Vue d'ensemble de vos horaires de travail
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Chargement...</div>
      ) : (
        <>
          {/* Statistics Cards */}
          {statistics && (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Moyenne d'arrivée
                  </CardTitle>
                  <Clock className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{statistics.moyenne_arrivee}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Moyenne de départ
                  </CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{statistics.moyenne_depart}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Moyenne de pause
                  </CardTitle>
                  <Coffee className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {statistics.moyenne_pause_minutes} min
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Total d'entrées
                  </CardTitle>
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{statistics.total_entrees}</div>
                </CardContent>
              </Card>
            </div>
          )}

          <div className="grid gap-8 md:grid-cols-2">
            {/* Add Schedule Form */}
            <ScheduleForm onSuccess={handleScheduleAdded} />

            {/* Recent Schedules */}
            <Card>
              <CardHeader>
                <CardTitle>Horaires Récents</CardTitle>
                <CardDescription>
                  Les 5 dernières entrées
                </CardDescription>
              </CardHeader>
              <CardContent>
                {recentSchedules.length === 0 ? (
                  <p className="text-muted-foreground text-center py-8">
                    Aucun horaire enregistré
                  </p>
                ) : (
                  <div className="space-y-4">
                    {recentSchedules.map((schedule) => (
                      <div
                        key={schedule.id}
                        className="flex items-center justify-between border-b pb-2 last:border-0"
                      >
                        <div>
                          <p className="font-medium">
                            {new Date(schedule.date_saisie).toLocaleDateString('fr-FR')}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {schedule.heure_debut} → {schedule.heure_depart_calculee}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-muted-foreground">Pause</p>
                          <p className="font-medium">
                            {schedule.duree_pause_minutes || 0} min
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
