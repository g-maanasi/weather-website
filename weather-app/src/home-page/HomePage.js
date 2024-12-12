import "./homepage.css";
import { Box, Typography } from "@mui/material";
import ThermostatIcon from "@mui/icons-material/Thermostat";

export const Home = () => {
  return (
    <Box className="home-container">
      <Box className="header-bar">
        <Box className="header-navigation">
          <Box className="logo">
            <ThermostatIcon
              className="logo-icon"
              sx={{ height: 35, width: 35 }}
            />
            <Typography
              sx={{
                display: "flex",
                alignItems: "center",
                ml: 1,
                fontSize: 20,
                fontFamily: "'DM Sans', sans-serif",
              }}
            >
              National Weather
            </Typography>
          </Box>

          <Box className="log-in-container">
              
          </Box>
        </Box>
      </Box>

      <Box className="middle-container"></Box>
    </Box>
  );
};
