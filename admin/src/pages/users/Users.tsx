import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '../../components/ui/card';
import { Search, Filter, MoreVertical, UserPlus, AlertCircle, Users as UsersIcon } from 'lucide-react';
import userService, { User, UserCreate } from '../../services/user.service';
import ConfirmModal from '../../components/ui/confirm-modal';
import Modal from '../../components/ui/modal';
import UserForm from './UserForm';

const Users: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [userTypeFilter, setUserTypeFilter] = useState<string>('all');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [deleteModalState, setDeleteModalState] = useState<{
    isOpen: boolean;
    userId: string | null;
    userName: string;
  }>({
    isOpen: false,
    userId: null,
    userName: '',
  });

  // Fetch users on component mount
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await userService.getUsers();
        setUsers(data);
        setFilteredUsers(data);
      } catch (error) {
        console.error('Error fetching users:', error);
        setError('Failed to load users data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  // Filter users when search term or user type changes
  useEffect(() => {
    const filtered = users.filter(user => {
      const matchesSearch = 
        user.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = userTypeFilter === 'all' || user.user_type === userTypeFilter;
      return matchesSearch && matchesType;
    });
    setFilteredUsers(filtered);
  }, [searchTerm, userTypeFilter, users]);

  const handleAddUser = () => {
    setIsCreateModalOpen(true);
  };

  const handleCreateUser = async (userData: UserCreate) => {
    try {
      const newUser = await userService.createUser(userData);
      setUsers(prevUsers => [newUser, ...prevUsers]);
      setError(null);
      setIsCreateModalOpen(false);
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  };

  const handleDeleteUser = async (id: string, name: string) => {
    setDeleteModalState({
      isOpen: true,
      userId: id,
      userName: name,
    });
  };

  const handleConfirmDelete = async () => {
    if (!deleteModalState.userId) return;
    
    try {
      await userService.deleteUser(deleteModalState.userId);
      setUsers(users.filter(user => user.id !== deleteModalState.userId));
      setError(null);
    } catch (error) {
      console.error('Error deleting user:', error);
      throw error;
    }
  };

  const handleToggleStatus = async (userId: string) => {
    try {
      const updatedUser = await userService.toggleUserStatus(userId);
      setUsers(users.map(user => 
        user.id === userId ? updatedUser : user
      ));
      setError(null);
    } catch (error) {
      console.error('Error toggling user status:', error);
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
            User Management
          </h1>
          <p className="text-sm text-muted-foreground">
            Manage and monitor user accounts across the platform
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-xs text-muted-foreground">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
          <button 
            className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary-600 text-white hover:bg-primary-700 h-10 px-4 py-2"
            onClick={handleAddUser}
          >
            <UserPlus className="h-4 w-4 mr-2" />
            Add User
          </button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Total Users</CardTitle>
            <div className="p-1.5 rounded-full bg-primary-50">
              <UsersIcon className="h-3.5 w-3.5 text-primary-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{users.length}</div>
            <div className="text-xs text-muted-foreground mt-0.5">Active accounts in the system</div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Active Users</CardTitle>
            <div className="p-1.5 rounded-full bg-green-50">
              <UsersIcon className="h-3.5 w-3.5 text-green-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{users.filter(u => u.is_active).length}</div>
            <div className="text-xs text-muted-foreground mt-0.5">Currently active accounts</div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 p-3">
            <CardTitle className="text-xs font-medium text-muted-foreground">Brokers</CardTitle>
            <div className="p-1.5 rounded-full bg-blue-50">
              <UsersIcon className="h-3.5 w-3.5 text-blue-600" />
            </div>
          </CardHeader>
          <CardContent className="p-3 pt-0">
            <div className="text-xl font-bold">{users.filter(u => u.user_type === 'broker').length}</div>
            <div className="text-xs text-muted-foreground mt-0.5">Registered brokers</div>
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
                  placeholder="Search users by name or email..."
                  className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="flex gap-4">
              <select
                className="px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                value={userTypeFilter}
                onChange={(e) => setUserTypeFilter(e.target.value)}
              >
                <option value="all">All Types</option>
                <option value="client">Clients</option>
                <option value="broker">Brokers</option>
                <option value="admin">Admins</option>
              </select>
              <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-primary-200 bg-primary-50 hover:bg-primary-100 text-primary-700 h-10 px-4 py-2">
                <Filter className="h-4 w-4 mr-2" />
                More Filters
              </button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Users Table */}
      <Card className="hover:shadow-lg transition-shadow duration-200">
        <CardHeader className="p-4">
          <CardTitle className="text-base font-semibold">User List</CardTitle>
        </CardHeader>
        <CardContent className="p-4 pt-0">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Login
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredUsers.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center mr-3">
                          <span className="text-sm font-medium text-primary-600">
                            {user.first_name[0]}{user.last_name[0]}
                          </span>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {user.first_name} {user.last_name}
                          </div>
                          <div className="text-xs text-gray-500">
                            ID: {user.id}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{user.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        (user.user_type || 'client') === 'admin' ? 'bg-purple-100 text-purple-800' :
                        (user.user_type || 'client') === 'broker' ? 'bg-blue-100 text-blue-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {(user.user_type || 'client').charAt(0).toUpperCase() + (user.user_type || 'client').slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => handleToggleStatus(user.id)}
                        className={`inline-flex items-center justify-center rounded-md text-xs font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${
                          user.is_active ? 'bg-primary-100 text-primary-700 hover:bg-primary-200' : 'bg-red-100 text-red-700 hover:bg-red-200'
                        } px-2 py-1`}
                      >
                        {user.is_active ? 'Active' : 'Inactive'}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {new Date(user.updated_at).toLocaleDateString()}
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(user.updated_at).toLocaleTimeString()}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => handleDeleteUser(user.id, `${user.first_name} ${user.last_name}`)}
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
        title="Create New User"
        size="lg"
      >
        <UserForm
          onSubmit={handleCreateUser}
          onCancel={() => setIsCreateModalOpen(false)}
        />
      </Modal>

      <ConfirmModal
        isOpen={deleteModalState.isOpen}
        onClose={() => setDeleteModalState({ isOpen: false, userId: null, userName: '' })}
        onConfirm={handleConfirmDelete}
        title="Delete User"
        description={`Are you sure you want to delete ${deleteModalState.userName}? This action cannot be undone.`}
        confirmText="Delete User"
        variant="danger"
      />
    </div>
  );
};

export default Users; 