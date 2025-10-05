import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import MarsMap from './MarsMap'
import Search from './Search'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Search />} />
        <Route path="/map" element={<MarsMap />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
