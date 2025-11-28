'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrivalChart } from '@/components/charts/ArrivalChart';
import { DepartureChart } from '@/components/charts/DepartureChart';
import { PauseChart } from '@/components/charts/PauseChart';
import { api } from '@/lib/api';
import type { Statistics, ChartsData, Config } from '@/types';
import { BarChart3 } from 'lucide-react';

export default function StatisticsPage() {
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [chartsData, setChartsData] = useState<ChartsData | null>(null);
  const [config, setConfig] = useState<Config | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [stats, charts, configData] = await Promise.all([
        api.getStatistics(),
        api.getChartsData(),
        api.getConfig(),
      ]);
      setStatistics(stats);
      setChartsData(charts);
      setConfig(configData);
    } catch (error) {
      console.error('Error loading statistics:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Statistiques</h1>
        <p className="text-muted-foreground">
          Visualisation et analyse de vos horaires
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Chargement...</div>
      ) : (
        <>
          {/* Summary Statistics */}
          {statistics && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Résumé des Statistiques
                </CardTitle>
                <CardDescription>
                  Moyennes calculées sur {statistics.total_entrees} entrées
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-3">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Moyenne d'arrivée</p>
                    <p className="text-3xl font-bold">{statistics.moyenne_arrivee}</p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Moyenne de départ</p>
                    <p className="text-3xl font-bold">{statistics.moyenne_depart}</p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Moyenne de pause</p>
                    <p className="text-3xl font-bold">
                      {statistics.moyenne_pause_minutes} minutes
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Charts */}
          {chartsData && (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Évolution des Heures d'Arrivée</CardTitle>
                  <CardDescription>
                    Avec ligne de moyenne à {statistics?.moyenne_arrivee}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ArrivalChart
                    data={chartsData.arrivee}
                    moyenne={statistics?.moyenne_arrivee}
                  />
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Évolution des Heures de Départ</CardTitle>
                  <CardDescription>
                    Avec ligne de moyenne à {statistics?.moyenne_depart}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <DepartureChart
                    data={chartsData.depart}
                    moyenne={statistics?.moyenne_depart}
                  />
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Durée des Pauses</CardTitle>
                  <CardDescription>
                    Code couleur: vert si ≥ {config?.seuil_pause_minutes}min, rouge sinon
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <PauseChart
                    data={chartsData.pause}
                    seuil={config?.seuil_pause_minutes}
                  />
                </CardContent>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  );
}
