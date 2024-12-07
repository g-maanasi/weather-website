import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [test, setTest] = useState('');

  useEffect(() => {
    fetch("http://127.0.0.1:5000")
      .then(res => res.json())
      .then(
        (result) => {
          setTest(result.message)
        }
      )
  }, [])
  
  return (
    <div className="App">
      {test}
    </div>
  );
}

export default App;
