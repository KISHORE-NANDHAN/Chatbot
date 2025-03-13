import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Chat from "./Chat";
import Popup from "./Popup";

export default function App() {
  return (
    <Router>
      <div>
        <nav style={{ padding: "10px", display: "flex", gap: "20px" }}>
          <Link to="/">Home</Link>
          <Link to="/chat">Go to Chat</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Popup />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </div>
    </Router>
  );
}
