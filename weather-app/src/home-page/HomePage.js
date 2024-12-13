import "./homepage.css";
import { Box } from "@mui/material";
import { NavigationBar } from "../components/navigation/NavigationBar";

export const Home = () => {
  return (
    <Box className="home-container">
      <NavigationBar />

      <Box className="middle-container"></Box>
    </Box>
  );
};
