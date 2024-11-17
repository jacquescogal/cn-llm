import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Base from './components/Base';
import ExplorePage from './components/explore-page/ExplorePage';

function App() {
  return (
    <>
    <Router>
      <Routes>
        <Route path="/" element={<Base />}>
        <Route path="/" element={<ExplorePage />}/>
        <Route path="/explore" element={<ExplorePage />}/>
        </Route>
      </Routes>
    </Router>
    </>
  )
}

export default App