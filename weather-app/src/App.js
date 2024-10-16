import "./App.css";
import { Box } from '@mui/material';

function App() {
  return (
    <div className="App">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
          href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap"
          rel="stylesheet"
        />
      </head>
      <Box className="website-nav">
        <h3>Welcome to Worldwide Weather Forecast!</h3>
        <p>Select a place you want to view.</p>
      </Box>
    </div>
  );
}

export default App;
