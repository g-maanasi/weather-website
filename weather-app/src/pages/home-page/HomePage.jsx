import "./homepage.css";
import { Box } from "@mui/material";
import { NavigationBar } from "../../components/navigation/NavigationBar";
import { LocationSelection } from "../../components/weather-selection/LocationSelection";

export const Home = () => {
  return (
    <Box className="home-container">
      <NavigationBar />

      <Box className="page-container">
        <LocationSelection />
      </Box>
    </Box>
  );
};
