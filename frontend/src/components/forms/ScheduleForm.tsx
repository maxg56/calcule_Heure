'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { z } from 'zod';
import { api } from '@/lib/api';
import type { Schedule, CreateScheduleInput } from '@/types';

// Zod schema for validation
const scheduleSchema = z.object({
  heure_debut: z.string().min(1, "L'heure de début est requise"),
  heure_debut_pause: z.string().min(1, "L'heure de début de pause est requise"),
  heure_fin_pause: z.string().min(1, "L'heure de fin de pause est requise"),
});

interface ScheduleFormProps {
  onSuccess?: (schedule: Schedule) => void;
  initialData?: Partial<CreateScheduleInput>;
}

export function ScheduleForm({ onSuccess, initialData }: ScheduleFormProps) {
  const [formData, setFormData] = useState<CreateScheduleInput>({
    heure_debut: initialData?.heure_debut || '',
    heure_debut_pause: initialData?.heure_debut_pause || '',
    heure_fin_pause: initialData?.heure_fin_pause || '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [calculatedEndTime, setCalculatedEndTime] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field
    setErrors((prev) => ({ ...prev, [name]: '' }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrors({});

    try {
      // Validate form data
      const validatedData = scheduleSchema.parse(formData);

      // Submit to API
      const schedule = await api.createSchedule(validatedData);
      setCalculatedEndTime(schedule.heure_depart_calculee);

      // Call success callback
      if (onSuccess) {
        onSuccess(schedule);
      }

      // Reset form
      setFormData({
        heure_debut: '',
        heure_debut_pause: '',
        heure_fin_pause: '',
      });
    } catch (error) {
      if (error instanceof Error) {
        if (error.name === 'ZodError') {
          const zodError = error as any;
          const fieldErrors: Record<string, string> = {};
          zodError.errors.forEach((err: any) => {
            if (err.path) {
              fieldErrors[err.path[0]] = err.message;
            }
          });
          setErrors(fieldErrors);
        } else {
          setErrors({ submit: error.message });
        }
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Ajouter un Horaire</CardTitle>
        <CardDescription>
          Saisissez vos heures de travail et de pause
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="heure_debut">Heure de début</Label>
            <Input
              id="heure_debut"
              name="heure_debut"
              type="time"
              value={formData.heure_debut}
              onChange={handleChange}
              required
            />
            {errors.heure_debut && (
              <p className="text-sm text-destructive">{errors.heure_debut}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="heure_debut_pause">Heure de début de pause</Label>
            <Input
              id="heure_debut_pause"
              name="heure_debut_pause"
              type="time"
              value={formData.heure_debut_pause}
              onChange={handleChange}
              required
            />
            {errors.heure_debut_pause && (
              <p className="text-sm text-destructive">{errors.heure_debut_pause}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="heure_fin_pause">Heure de fin de pause</Label>
            <Input
              id="heure_fin_pause"
              name="heure_fin_pause"
              type="time"
              value={formData.heure_fin_pause}
              onChange={handleChange}
              required
            />
            {errors.heure_fin_pause && (
              <p className="text-sm text-destructive">{errors.heure_fin_pause}</p>
            )}
          </div>

          {errors.submit && (
            <div className="p-3 bg-destructive/10 text-destructive rounded-md">
              {errors.submit}
            </div>
          )}

          {calculatedEndTime && (
            <div className="p-4 bg-primary/10 text-primary rounded-md">
              <p className="font-semibold">Heure de départ calculée:</p>
              <p className="text-2xl">{calculatedEndTime}</p>
            </div>
          )}

          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? 'Enregistrement...' : 'Enregistrer et Calculer'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
