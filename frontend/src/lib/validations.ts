/**
 * Validation schemas using Zod
 */

import { z } from 'zod';

/**
 * Config validation schema
 */
export const configSchema = z.object({
  duree_travail_heures: z.number().int().min(0).max(12),
  duree_travail_minutes: z.number().int().min(0).max(59),
  seuil_pause_minutes: z.number().int().min(0).max(180),
});

export type ConfigFormData = z.infer<typeof configSchema>;

/**
 * Schedule validation schema
 */
export const scheduleSchema = z.object({
  heure_debut: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/, 'Format HH:MM requis'),
  heure_debut_pause: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/, 'Format HH:MM requis'),
  heure_fin_pause: z.string().regex(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/, 'Format HH:MM requis'),
});

export type ScheduleFormData = z.infer<typeof scheduleSchema>;
