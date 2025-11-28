'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import type { Schedule } from '@/types';
import { Trash2, Calendar } from 'lucide-react';

export default function SchedulesPage() {
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadSchedules();
  }, []);

  const loadSchedules = async () => {
    try {
      const data = await api.getSchedules();
      setSchedules(data.reverse());
    } catch (error) {
      console.error('Error loading schedules:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet horaire ?')) {
      return;
    }

    try {
      await api.deleteSchedule(id);
      setSchedules(schedules.filter(s => s.id !== id));
    } catch (error) {
      console.error('Error deleting schedule:', error);
      alert('Erreur lors de la suppression');
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Horaires</h1>
        <p className="text-muted-foreground">
          Liste complète de tous vos horaires enregistrés
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Chargement...</div>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Tous les Horaires
            </CardTitle>
            <CardDescription>
              {schedules.length} horaire(s) enregistré(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            {schedules.length === 0 ? (
              <p className="text-muted-foreground text-center py-8">
                Aucun horaire enregistré
              </p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left py-3 px-4">Date</th>
                      <th className="text-left py-3 px-4">Heure début</th>
                      <th className="text-left py-3 px-4">Début pause</th>
                      <th className="text-left py-3 px-4">Fin pause</th>
                      <th className="text-left py-3 px-4">Durée pause</th>
                      <th className="text-left py-3 px-4">Heure départ</th>
                      <th className="text-right py-3 px-4">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {schedules.map((schedule) => (
                      <tr key={schedule.id} className="border-b hover:bg-muted/50">
                        <td className="py-3 px-4">
                          {new Date(schedule.date_saisie).toLocaleDateString('fr-FR', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                          })}
                        </td>
                        <td className="py-3 px-4 font-medium">{schedule.heure_debut}</td>
                        <td className="py-3 px-4">{schedule.heure_debut_pause}</td>
                        <td className="py-3 px-4">{schedule.heure_fin_pause}</td>
                        <td className="py-3 px-4">
                          <span className="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-primary/10 text-primary">
                            {schedule.duree_pause_minutes || 0} min
                          </span>
                        </td>
                        <td className="py-3 px-4 font-semibold text-primary">
                          {schedule.heure_depart_calculee}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDelete(schedule.id)}
                            className="text-destructive hover:text-destructive"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
