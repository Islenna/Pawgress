import './App.css'
import { User } from './types'
import UserCard from './components/user/UserCard'


const sampleUser: User = {
  id: 1,
  username: "vet_tech42",
  email: "tech@example.com",
  role: "admin"
};

function App() {

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">User Dashboard</h1>
      <UserCard user={sampleUser} />
    </div>
  );
}

export default App
