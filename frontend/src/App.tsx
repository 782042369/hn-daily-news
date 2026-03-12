import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Archive from './pages/Archive'
import Article from './pages/Article'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="archive" element={<Archive />} />
        <Route path=":date" element={<Article />} />
      </Route>
    </Routes>
  )
}

export default App
