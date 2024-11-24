import { useState, useEffect } from 'react';
import axios from 'axios';

interface User {
    id: number;
    firstName: string;
    lastName: string;
    role: string;
}

const UserList: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [newUser, setNewUser] = useState<Omit<User, 'id'>>({
        firstName: '',
        lastName: '',
        role: '',
    });

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const response = await axios.get<User[]>('http://localhost:8000/api/users/');
            console.log(response.data);
            setUsers(response.data);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    const handleAddUser = async () => {
        try {
            const response = await axios.post<User>('http://localhost:8000/api/users/', newUser);
            setUsers((prevUsers) => [...prevUsers, response.data]);
            setNewUser({ firstName: '', lastName: '', role: '' });
        } catch (error) {
            console.error('Error adding user:', error);
        }
    };

    const handleDeleteUser = async (id: number) => {
        try {
            await axios.delete(`http://localhost:8000/api/users/${id}`);
            setUsers(users.filter(user => user.id !== id));
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    };

    return (
        <div>
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleAddUser();
                }}
            >
                <label htmlFor="firstName">First name</label>
                <input
                    id="firstName"
                    type="text"
                    placeholder="First name"
                    value={newUser.firstName}
                    onChange={(e) => setNewUser({ ...newUser, firstName: e.target.value })}
                />
                <label htmlFor="lastName">Last name</label>
                <input
                    id="lastName"
                    type="text"
                    placeholder="Last name"
                    value={newUser.lastName}
                    onChange={(e) => setNewUser({ ...newUser, lastName: e.target.value })}
                />
                <label htmlFor="role">Role</label>
                <select
                    id="role"
                    value={newUser.role}
                    onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                >
                    <option value="">Select role</option>
                    <option value="student">Student</option>
                    <option value="director">Director</option>
                    <option value="manager">Manager</option>
                    <option value="developer">Developer</option>
                </select>
                <button type="submit">SUBMIT</button>
            </form>

            <ul>
                {users.map(user => (
                    <li key={user.id}>
                        <div>
                            <strong>{user.firstName} {user.lastName}</strong>
                            <span>({user.role})</span>
                        </div>
                        <button
                            className="deleteBtn"
                            onClick={() => handleDeleteUser(user.id)}
                        >
                            🗑️
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default UserList;
