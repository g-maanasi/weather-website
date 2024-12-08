import "./App.css";
import { useEffect, useState } from "react";
import { Box, Button, Typography } from "@mui/material";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";
import { lightTheme, darkTheme } from "./theme/colorTheme";
import { WeatherSelection } from "./weather-selection/weatherSelection";

function App() {
  const [test, setTest] = useState("");
  const [colorMode, setColorMode] = useState(lightTheme);

  useEffect(() => {
    fetch("http://127.0.0.1:5000")
      .then((res) => res.json())
      .then((result) => {
        setTest(result.message);
      });
  }, [setTest]);

  const toggleColorMode = () => {
    setColorMode(colorMode === lightTheme ? darkTheme : lightTheme);
  };

  return (
    <div className="App">
      <link rel="preconnect" href="https://fonts.googleapis.com"></link>
      <link rel="preconnect" href="https://fonts.gstatic.com" />
      <link
        href="https://fonts.googleapis.com/css2?family=Parkinsans:wght@300..800&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap"
        rel="stylesheet"
      ></link>
      <Box className="weather-location-container">
        <WeatherSelection />
      </Box>

      <Box className="title-container">
        <Box className="color-mode-container">
          <Button
            className="color-mode-button"
            variant="outlined"
            sx={{ borderRadius: 50, borderColor: "white" }}
            onClick={toggleColorMode}
          >
            {colorMode === lightTheme ? (
              <DarkModeIcon sx={{ color: "white" }} />
            ) : (
              <LightModeIcon />
            )}
          </Button>
        </Box>

        <Typography variant="h3" component="h2" className="title">
          Welcome to EasyWeather!
        </Typography>
      </Box>
    </div>
  );
}

export default App;
