import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '../components/ui/card';
import { AlertCircle, Database, Key, RefreshCw, Shield, Bell, CheckCircle2 } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import settingsService, { SystemSettings } from '../services/settings.service';

const Switch: React.FC<{
  checked: boolean;
  onChange: (checked: boolean) => void;
  label: string;
}> = ({ checked, onChange, label }) => (
  <div className="flex items-center justify-between">
    <label className="text-sm font-medium text-gray-700">{label}</label>
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={`
        relative inline-flex h-6 w-11 items-center rounded-full transition-colors
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2
        ${checked ? 'bg-primary-600' : 'bg-gray-200'}
      `}
    >
      <span
        className={`
          inline-block h-5 w-5 transform rounded-full bg-white shadow-lg ring-0 transition-transform
          ${checked ? 'translate-x-6' : 'translate-x-1'}
        `}
      />
    </button>
  </div>
);

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<SystemSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await settingsService.getSettings();
        setSettings(data);
      } catch (error) {
        console.error('Error fetching settings:', error);
        setError('Failed to load settings. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleSave = async () => {
    if (!settings) return;
    
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      await settingsService.updateSettings(settings);
      setSuccess('Settings updated successfully');
    } catch (error) {
      console.error('Error saving settings:', error);
      setError('Failed to save settings. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-red-500 text-center p-6 rounded-lg bg-red-50">
          <AlertCircle className="h-8 w-8 mx-auto mb-2" />
          <p className="text-base font-medium">{error}</p>
        </div>
      </div>
    );
  }

  if (!settings) {
    return null;
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
          Settings
        </h1>
        <button
          className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
            disabled:pointer-events-none disabled:opacity-50
            bg-primary-600 text-white hover:bg-primary-700 h-10 px-6 py-2 shadow-sm"
          onClick={handleSave}
          disabled={saving}
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${saving ? 'animate-spin' : ''}`} />
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {success && (
        <div className="bg-green-50 text-green-600 p-4 rounded-lg flex items-center shadow-sm">
          <CheckCircle2 className="h-5 w-5 mr-2" />
          <span>{success}</span>
        </div>
      )}

      {/* Cache Settings */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-4 border-b">
          <div className="flex items-center gap-2">
            <Database className="h-5 w-5 text-primary-600" />
            <CardTitle className="text-lg font-semibold">Cache Settings</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="p-4">
          <div className="space-y-6">
            <Switch
              checked={settings.cache.enabled}
              onChange={(checked) => setSettings({
                ...settings,
                cache: { ...settings.cache, enabled: checked }
              })}
              label="Enable Cache"
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Max Cache Size (MB)</label>
                <input
                  type="number"
                  value={settings.cache.maxSize}
                  onChange={(e) => setSettings({
                    ...settings,
                    cache: { ...settings.cache, maxSize: parseInt(e.target.value) }
                  })}
                  className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                    shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Cache TTL (minutes)</label>
                <input
                  type="number"
                  value={settings.cache.ttl}
                  onChange={(e) => setSettings({
                    ...settings,
                    cache: { ...settings.cache, ttl: parseInt(e.target.value) }
                  })}
                  className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                    shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
            </div>
            <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded-md">
              Current cache size: {settings.cache.currentSize}MB
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Security Settings */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-4 border-b">
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-primary-600" />
            <CardTitle className="text-lg font-semibold">Security Settings</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="p-4">
          <div className="space-y-6">
            <Switch
              checked={settings.security.twoFactorEnabled}
              onChange={(checked) => setSettings({
                ...settings,
                security: { ...settings.security, twoFactorEnabled: checked }
              })}
              label="Two-Factor Authentication"
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Session Timeout (minutes)</label>
                <input
                  type="number"
                  value={settings.security.sessionTimeout}
                  onChange={(e) => setSettings({
                    ...settings,
                    security: { ...settings.security, sessionTimeout: parseInt(e.target.value) }
                  })}
                  className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                    shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Max Login Attempts</label>
                <input
                  type="number"
                  value={settings.security.maxLoginAttempts}
                  onChange={(e) => setSettings({
                    ...settings,
                    security: { ...settings.security, maxLoginAttempts: parseInt(e.target.value) }
                  })}
                  className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                    shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* API Settings */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-4 border-b">
          <div className="flex items-center gap-2">
            <Key className="h-5 w-5 text-primary-600" />
            <CardTitle className="text-lg font-semibold">API Settings</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="p-4">
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Rate Limit (requests/minute)</label>
                <input
                  type="number"
                  value={settings.api.rateLimit}
                  onChange={(e) => setSettings({
                    ...settings,
                    api: { ...settings.api, rateLimit: parseInt(e.target.value) }
                  })}
                  className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                    shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Timeout (seconds)</label>
                <input
                  type="number"
                  value={settings.api.timeout}
                  onChange={(e) => setSettings({
                    ...settings,
                    api: { ...settings.api, timeout: parseInt(e.target.value) }
                  })}
                  className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                    shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Base URL</label>
              <input
                type="text"
                value={settings.api.baseUrl}
                onChange={(e) => setSettings({
                  ...settings,
                  api: { ...settings.api, baseUrl: e.target.value }
                })}
                className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                  shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notification Settings */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-4 border-b">
          <div className="flex items-center gap-2">
            <Bell className="h-5 w-5 text-primary-600" />
            <CardTitle className="text-lg font-semibold">Notification Settings</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="p-4">
          <div className="space-y-6">
            <Switch
              checked={settings.notifications.email}
              onChange={(checked) => setSettings({
                ...settings,
                notifications: { ...settings.notifications, email: checked }
              })}
              label="Email Notifications"
            />
            <Switch
              checked={settings.notifications.sms}
              onChange={(checked) => setSettings({
                ...settings,
                notifications: { ...settings.notifications, sms: checked }
              })}
              label="SMS Notifications"
            />
            <Switch
              checked={settings.notifications.push}
              onChange={(checked) => setSettings({
                ...settings,
                notifications: { ...settings.notifications, push: checked }
              })}
              label="Push Notifications"
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Alert Threshold</label>
              <input
                type="number"
                value={settings.notifications.alertThreshold}
                onChange={(e) => setSettings({
                  ...settings,
                  notifications: { ...settings.notifications, alertThreshold: parseInt(e.target.value) }
                })}
                className="block w-full rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm
                  shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Settings; 