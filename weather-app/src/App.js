import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Home } from "./home-page/HomePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
