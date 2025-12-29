import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { NewAnalysis } from './pages/NewAnalysis';
import { RunView } from './pages/RunView';
import { History } from './pages/History';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<NewAnalysis />} />
          <Route path="/runs/:runId" element={<RunView />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
