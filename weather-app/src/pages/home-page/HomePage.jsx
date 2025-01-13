import "./homepage.css";
import { Box, Typography } from "@mui/material";
import { NavigationBar } from "../../components/navigation/NavigationBar";
import { LocationSelection } from "../../components/weather-selection/LocationSelection";
import { Fade } from "react-awesome-reveal";

export const Home = () => {
  return (
    <Box className="home-container">
      <NavigationBar />

      <Box className="page-container">
        <Box className="banner-container">
          <Box className="banner">
            <Fade cascade damping={0.7} className="text-containter">
              <Typography variant="h4" fontWeight={"fontWeightLight"}>
                Making weather lookup
              </Typography>
              <Typography variant="h3" fontWeight={"fontWeightHeavy"} sx={{ color: '#02387f' }}>
                Simple and Seamless
              </Typography>
            </Fade>
          </Box>
        </Box>
        <LocationSelection />
      </Box>
    </Box>
  );
};
