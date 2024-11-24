import React from 'react';
import './App.css';
import UserList from './UserList';

const App: React.FC = () => {
    return (
        <div className="App">
            <div className="mainbox">
                <h1>Let’s level up your brand, together</h1>
                <UserList />
            </div>
        </div>
    );
};

export default App;
