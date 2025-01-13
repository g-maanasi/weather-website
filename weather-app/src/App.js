import "./App.css";
import React, { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Home } from "./pages/home-page/HomePage";

const Login = lazy(() => import("./pages/login/LoginPage"));
const Forecast = lazy(() => import("./pages/forecast-page/ForecastPage"));

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Suspense fallback={<div>Loading...</div>}>
              <Home />
            </Suspense>
          }
        />
        <Route
          path="/login"
          element={
            <Suspense fallback={<div>Loading...</div>}>
              <Login />
            </Suspense>
          }
        />
        <Route
          path="/forecast"
          element={
            <Suspense fallback={<div>Loading...</div>}>
              <Forecast />
            </Suspense>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
