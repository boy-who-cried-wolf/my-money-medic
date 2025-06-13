import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '../components/ui/card';
import { Search, Filter, MoreVertical, UserPlus, Shield, Star, TrendingUp, AlertCircle } from 'lucide-react';
import brokerService, { Broker, BrokerCreate } from '../services/broker.service';
import ConfirmModal from '../components/ui/confirm-modal';
import Modal from '../components/ui/modal';
import BrokerForm from './BrokerForm';

const Brokers: React.FC = () => {
  const [brokers, setBrokers] = useState<Broker[]>([]);
  const [filteredBrokers, setFilteredBrokers] = useState<Broker[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [licenseFilter, setLicenseFilter] = useState<string>('all');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [deleteModalState, setDeleteModalState] = useState<{
    isOpen: boolean;
    brokerId: string | null;
    brokerName: string;
  }>({
    isOpen: false,
    brokerId: null,
    brokerName: '',
  });

  // Fetch brokers on component mount
  useEffect(() => {
    const fetchBrokers = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await brokerService.getBrokers();
        setBrokers(data);
        setFilteredBrokers(data);
      } catch (error) {
        console.error('Error fetching brokers:', error);
        setError('Failed to load brokers data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchBrokers();
  }, []);

  // Filter brokers when search term or license status changes
  useEffect(() => {
    const filtered = brokers.filter(broker => {
      const matchesSearch = 
        broker.license_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
        broker.company_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        broker.office_address?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesLicense = licenseFilter === 'all' || broker.license_status === licenseFilter;
      return matchesSearch && matchesLicense;
    });
    setFilteredBrokers(filtered);
  }, [searchTerm, licenseFilter, brokers]);

  const handleAddBroker = () => {
    setIsCreateModalOpen(true);
  };

  const handleCreateBroker = async (brokerData: BrokerCreate) => {
    try {
      const newBroker = await brokerService.createBroker(brokerData);
      setBrokers(prevBrokers => [newBroker, ...prevBrokers]);
      setError(null);
      setIsCreateModalOpen(false);
    } catch (error) {
      console.error('Error creating broker:', error);
      throw error;
    }
  };

  const handleDeleteBroker = async (id: string, name: string) => {
    setDeleteModalState({
      isOpen: true,
      brokerId: id,
      brokerName: name,
    });
  };

  const handleConfirmDelete = async () => {
    if (!deleteModalState.brokerId) return;
    
    try {
      await brokerService.deleteBroker(deleteModalState.brokerId);
      setBrokers(brokers.filter(broker => broker.id !== deleteModalState.brokerId));
      setError(null);
    } catch (error) {
      console.error('Error deleting broker:', error);
      throw error;
    }
  };

  const handleToggleVerification = async (brokerId: string) => {
    try {
      const updatedBroker = await brokerService.toggleVerification(brokerId);
      setBrokers(brokers.map(broker => 
        broker.id === brokerId ? updatedBroker : broker
      ));
      setError(null);
    } catch (error) {
      console.error('Error toggling broker verification:', error);
      throw error;
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

  return (
    <div className="p-4 space-y-4">
      {/* Header Section */}
      <div className="flex justify-between items-center mb-6">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent">
            Broker Management
          </h1>
          <p className="text-sm text-muted-foreground">
            Manage and monitor broker accounts and licenses
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-xs text-muted-foreground">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
          <button 
            className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary-600 text-white hover:bg-primary-700 h-10 px-4 py-2"
            onClick={handleAddBroker}
          >
            <UserPlus className="h-4 w-4 mr-2" />
            Add Broker
          </button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Total Brokers</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <Shield className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{brokers.length}</div>
            <div className="text-xs text-muted-foreground mt-0.5">Registered brokers</div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Verified Brokers</CardTitle>
            <div className="p-1.5 rounded-full bg-green-50">
              <Shield className="h-3.5 w-3.5 text-green-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{brokers.filter(b => b.is_verified).length}</div>
            <div className="text-xs text-muted-foreground mt-0.5">Fully verified accounts</div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Active Licenses</CardTitle>
            <div className="p-1.5 rounded-full bg-blue-50">
              <TrendingUp className="h-3.5 w-3.5 text-blue-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{brokers.filter(b => b.license_status === 'active').length}</div>
            <div className="text-xs text-muted-foreground mt-0.5">Currently active licenses</div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search brokers by license, company, or location..."
                  className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="flex gap-4">
              <select
                className="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                value={licenseFilter}
                onChange={(e) => setLicenseFilter(e.target.value)}
              >
                <option value="all">All Licenses</option>
                <option value="active">Active</option>
                <option value="pending">Pending</option>
                <option value="revoked">Revoked</option>
                <option value="expired">Expired</option>
              </select>
              <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-primary-200 bg-primary-50 hover:bg-primary-100 text-primary-700 h-10 px-4 py-2">
                <Filter className="h-4 w-4 mr-2" />
                More Filters
              </button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Brokers Table */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-4">
          <CardTitle className="text-base font-semibold">Broker List</CardTitle>
        </CardHeader>
        <CardContent className="p-4 pt-0">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Broker
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    License
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Company
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Experience
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rating
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredBrokers.map((broker) => (
                  <tr key={broker.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center mr-3">
                          <span className="text-sm font-medium text-primary-600">
                            {broker.company_name?.[0] || 'B'}
                          </span>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {broker.company_name || 'Unnamed Company'}
                          </div>
                          <div className="text-xs text-gray-500">ID: {broker.id}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{broker.license_number}</div>
                      <button
                        onClick={() => handleToggleVerification(broker.id)}
                        className={`inline-flex items-center justify-center rounded-md text-xs font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${
                          broker.is_verified ? 'text-primary-600 hover:text-primary-700' : 'text-yellow-600 hover:text-yellow-700'
                        }`}
                      >
                        <Shield className="h-3 w-3 mr-1" />
                        {broker.is_verified ? 'Verified' : 'Pending Verification'}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{broker.company_name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{broker.years_of_experience} years</div>
                      <div className="text-xs text-gray-500">{broker.experience_level}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Star className="h-4 w-4 text-yellow-400" />
                        <span className="ml-1 text-sm text-gray-900">{broker.average_rating.toFixed(1)}</span>
                        <span className="ml-1 text-xs text-gray-500">({broker.success_rate}% success)</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        broker.license_status === 'active' ? 'bg-primary-100 text-primary-700' :
                        broker.license_status === 'pending' ? 'bg-yellow-100 text-yellow-700' :
                        broker.license_status === 'revoked' ? 'bg-red-100 text-red-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        {broker.license_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => handleDeleteBroker(broker.id, broker.company_name || 'Unnamed Company')}
                          className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-red-50 hover:text-red-700 p-1 rounded-full"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                        <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-primary-50 hover:text-primary-700 p-1 rounded-full">
                          <MoreVertical className="h-5 w-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Broker"
        size="lg"
      >
        <BrokerForm
          onSubmit={handleCreateBroker}
          onCancel={() => setIsCreateModalOpen(false)}
        />
      </Modal>

      <ConfirmModal
        isOpen={deleteModalState.isOpen}
        onClose={() => setDeleteModalState({ isOpen: false, brokerId: null, brokerName: '' })}
        onConfirm={handleConfirmDelete}
        title="Delete Broker"
        description={`Are you sure you want to delete ${deleteModalState.brokerName}? This action cannot be undone.`}
        confirmText="Delete Broker"
        variant="danger"
      />
    </div>
  );
};

export default Brokers; 