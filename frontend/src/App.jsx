import './App.css'
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import { Home } from './pages/home'
import Options from './pages/options'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/options" element={<Options />} />
      </Routes>
    </Router>
  )
}

export default App
