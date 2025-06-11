import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { useAuthContext } from '../context/AuthContext';

interface ProfileSettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const ProfileSettingsModal = ({ isOpen, onClose }: ProfileSettingsModalProps) => {
  const { user } = useAuthContext();
  const [activeTab, setActiveTab] = useState('profile');
  const [formData, setFormData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    phone: user?.phone || '',
    notifications: {
      email: true,
      push: true,
      marketing: false
    },
    theme: 'system',
    language: 'en'
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleNotificationChange = (type: string) => {
    setFormData(prev => ({
      ...prev,
      notifications: {
        ...prev.notifications,
        [type]: !prev.notifications[type as keyof typeof prev.notifications]
      }
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement profile update logic
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-2xl bg-white dark:bg-dark-800 rounded-2xl shadow-xl z-50 overflow-hidden"
          >
            <div className="flex flex-col h-[80vh] max-h-[800px]">
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-light-200 dark:border-dark-700">
                <h2 className="text-2xl font-semibold text-light-900 dark:text-dark-100">
                  Profile Settings
                </h2>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-light-100 dark:hover:bg-dark-700 rounded-lg transition-colors"
                >
                  <svg className="w-6 h-6 text-light-600 dark:text-dark-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Tabs */}
              <div className="flex border-b border-light-200 dark:border-dark-700">
                {['profile', 'notifications', 'preferences'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-6 py-4 text-sm font-medium capitalize transition-colors ${
                      activeTab === tab
                        ? 'text-primary-500 border-b-2 border-primary-500'
                        : 'text-light-600 dark:text-dark-300 hover:text-light-900 dark:hover:text-dark-100'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>

              {/* Content */}
              <div className="flex-1 overflow-y-auto p-6">
                <form onSubmit={handleSubmit}>
                  {activeTab === 'profile' && (
                    <div className="space-y-6">
                      <div className="flex items-center space-x-6">
                        <div className="relative">
                          <div className="w-24 h-24 rounded-full bg-light-100 dark:bg-dark-700 flex items-center justify-center">
                            <svg className="w-12 h-12 text-light-400 dark:text-dark-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                          </div>
                          <button
                            type="button"
                            className="absolute bottom-0 right-0 p-1.5 bg-primary-500 text-white rounded-full hover:bg-primary-600 transition-colors"
                          >
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                          </button>
                        </div>
                        <div>
                          <h3 className="text-lg font-medium text-light-900 dark:text-dark-100">
                            Profile Picture
                          </h3>
                          <p className="text-sm text-light-600 dark:text-dark-300">
                            Upload a new profile picture
                          </p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-6">
                        <div>
                          <label className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-2">
                            First Name
                          </label>
                          <input
                            type="text"
                            name="firstName"
                            value={formData.firstName}
                            onChange={handleInputChange}
                            className="w-full px-4 py-2 rounded-lg border border-light-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-2">
                            Last Name
                          </label>
                          <input
                            type="text"
                            name="lastName"
                            value={formData.lastName}
                            onChange={handleInputChange}
                            className="w-full px-4 py-2 rounded-lg border border-light-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-2">
                          Email
                        </label>
                        <input
                          type="email"
                          name="email"
                          value={formData.email}
                          onChange={handleInputChange}
                          className="w-full px-4 py-2 rounded-lg border border-light-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-2">
                          Phone Number
                        </label>
                        <input
                          type="tel"
                          name="phone"
                          value={formData.phone}
                          onChange={handleInputChange}
                          className="w-full px-4 py-2 rounded-lg border border-light-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        />
                      </div>
                    </div>
                  )}

                  {activeTab === 'notifications' && (
                    <div className="space-y-6">
                      <div className="flex items-center justify-between p-4 bg-light-50 dark:bg-dark-700 rounded-lg">
                        <div>
                          <h3 className="text-sm font-medium text-light-900 dark:text-dark-100">
                            Email Notifications
                          </h3>
                          <p className="text-sm text-light-600 dark:text-dark-300">
                            Receive email updates about your account
                          </p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={formData.notifications.email}
                            onChange={() => handleNotificationChange('email')}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-light-300 dark:bg-dark-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-500/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-light-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                        </label>
                      </div>

                      <div className="flex items-center justify-between p-4 bg-light-50 dark:bg-dark-700 rounded-lg">
                        <div>
                          <h3 className="text-sm font-medium text-light-900 dark:text-dark-100">
                            Push Notifications
                          </h3>
                          <p className="text-sm text-light-600 dark:text-dark-300">
                            Receive push notifications on your device
                          </p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={formData.notifications.push}
                            onChange={() => handleNotificationChange('push')}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-light-300 dark:bg-dark-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-500/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-light-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                        </label>
                      </div>

                      <div className="flex items-center justify-between p-4 bg-light-50 dark:bg-dark-700 rounded-lg">
                        <div>
                          <h3 className="text-sm font-medium text-light-900 dark:text-dark-100">
                            Marketing Emails
                          </h3>
                          <p className="text-sm text-light-600 dark:text-dark-300">
                            Receive emails about new features and promotions
                          </p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={formData.notifications.marketing}
                            onChange={() => handleNotificationChange('marketing')}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-light-300 dark:bg-dark-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-500/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-light-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
                        </label>
                      </div>
                    </div>
                  )}

                  {activeTab === 'preferences' && (
                    <div className="space-y-6">
                      <div>
                        <label className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-2">
                          Theme
                        </label>
                        <select
                          value={formData.theme}
                          onChange={(e) => setFormData(prev => ({ ...prev, theme: e.target.value }))}
                          className="w-full px-4 py-2 rounded-lg border border-light-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        >
                          <option value="light">Light</option>
                          <option value="dark">Dark</option>
                          <option value="system">System</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-2">
                          Language
                        </label>
                        <select
                          value={formData.language}
                          onChange={(e) => setFormData(prev => ({ ...prev, language: e.target.value }))}
                          className="w-full px-4 py-2 rounded-lg border border-light-300 dark:border-dark-600 bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        >
                          <option value="en">English</option>
                          <option value="es">Spanish</option>
                          <option value="fr">French</option>
                          <option value="de">German</option>
                        </select>
                      </div>
                    </div>
                  )}
                </form>
              </div>

              {/* Footer */}
              <div className="flex items-center justify-end space-x-4 p-6 border-t border-light-200 dark:border-dark-700">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 text-sm font-medium text-light-600 dark:text-dark-300 hover:text-light-900 dark:hover:text-dark-100 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  onClick={handleSubmit}
                  className="px-4 py-2 text-sm font-medium text-white bg-primary-500 rounded-lg hover:bg-primary-600 transition-colors"
                >
                  Save Changes
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default ProfileSettingsModal; 