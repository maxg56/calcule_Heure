'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { api } from '@/lib/api';
import { configSchema, type ConfigFormData } from '@/lib/validations';
import type { Config } from '@/types';
import { Settings, RotateCcw } from 'lucide-react';

export default function ConfigPage() {
  const [config, setConfig] = useState<Config | null>(null);
  const [formData, setFormData] = useState<ConfigFormData>({
    duree_travail_heures: 7,
    duree_travail_minutes: 10,
    seuil_pause_minutes: 45,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const data = await api.getConfig();
      setConfig(data);
      setFormData({
        duree_travail_heures: data.duree_travail_heures,
        duree_travail_minutes: data.duree_travail_minutes,
        seuil_pause_minutes: data.seuil_pause_minutes,
      });
    } catch (error) {
      console.error('Error loading config:', error);
      setMessage({ type: 'error', text: 'Erreur lors du chargement de la configuration' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: Number(value) }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setMessage(null);

    try {
      // Validate form data
      configSchema.parse(formData);

      // Submit to API
      const updatedConfig = await api.updateConfig(formData);
      setConfig(updatedConfig);
      setMessage({ type: 'success', text: 'Configuration enregistrée avec succès!' });
    } catch (error) {
      if (error instanceof Error) {
        setMessage({ type: 'error', text: error.message });
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = async () => {
    if (!confirm('Êtes-vous sûr de vouloir réinitialiser la configuration aux valeurs par défaut ?')) {
      return;
    }

    setIsSaving(true);
    setMessage(null);

    try {
      const resetConfig = await api.resetConfig();
      setConfig(resetConfig);
      setFormData({
        duree_travail_heures: resetConfig.duree_travail_heures,
        duree_travail_minutes: resetConfig.duree_travail_minutes,
        seuil_pause_minutes: resetConfig.seuil_pause_minutes,
      });
      setMessage({ type: 'success', text: 'Configuration réinitialisée aux valeurs par défaut' });
    } catch (error) {
      if (error instanceof Error) {
        setMessage({ type: 'error', text: error.message });
      }
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Configuration</h1>
        <p className="text-muted-foreground">
          Personnalisez les paramètres de l'application
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Chargement...</div>
      ) : (
        <div className="grid gap-6 max-w-2xl">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Paramètres de Travail
              </CardTitle>
              <CardDescription>
                Définissez vos préférences de durée de travail et de pause
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold mb-3">Durée de travail quotidienne</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="duree_travail_heures">Heures</Label>
                        <Input
                          id="duree_travail_heures"
                          name="duree_travail_heures"
                          type="number"
                          min="0"
                          max="24"
                          value={formData.duree_travail_heures}
                          onChange={handleChange}
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="duree_travail_minutes">Minutes</Label>
                        <Input
                          id="duree_travail_minutes"
                          name="duree_travail_minutes"
                          type="number"
                          min="0"
                          max="59"
                          value={formData.duree_travail_minutes}
                          onChange={handleChange}
                          required
                        />
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground mt-2">
                      Actuellement: {formData.duree_travail_heures}h{formData.duree_travail_minutes}min
                    </p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="seuil_pause_minutes">
                      Durée minimale de pause recommandée (minutes)
                    </Label>
                    <Input
                      id="seuil_pause_minutes"
                      name="seuil_pause_minutes"
                      type="number"
                      min="0"
                      max="180"
                      value={formData.seuil_pause_minutes}
                      onChange={handleChange}
                      required
                    />
                    <p className="text-sm text-muted-foreground">
                      Les pauses inférieures à cette durée seront signalées en rouge dans les graphiques
                    </p>
                  </div>
                </div>

                {message && (
                  <div
                    className={`p-3 rounded-md ${
                      message.type === 'success'
                        ? 'bg-primary/10 text-primary'
                        : 'bg-destructive/10 text-destructive'
                    }`}
                  >
                    {message.text}
                  </div>
                )}

                <div className="flex gap-3">
                  <Button type="submit" disabled={isSaving}>
                    {isSaving ? 'Enregistrement...' : 'Enregistrer'}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleReset}
                    disabled={isSaving}
                  >
                    <RotateCcw className="h-4 w-4 mr-2" />
                    Réinitialiser
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>

          {config && (
            <Card>
              <CardHeader>
                <CardTitle>Configuration Actuelle</CardTitle>
                <CardDescription>Valeurs enregistrées dans le système</CardDescription>
              </CardHeader>
              <CardContent>
                <dl className="space-y-2">
                  <div className="flex justify-between">
                    <dt className="text-muted-foreground">Durée de travail:</dt>
                    <dd className="font-medium">
                      {config.duree_travail_heures}h {config.duree_travail_minutes}min
                    </dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-muted-foreground">Seuil de pause:</dt>
                    <dd className="font-medium">{config.seuil_pause_minutes} minutes</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-muted-foreground">Format d'heure:</dt>
                    <dd className="font-mono text-sm">{config.format_heure}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-muted-foreground">Format de date:</dt>
                    <dd className="font-mono text-sm">{config.format_date}</dd>
                  </div>
                </dl>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
