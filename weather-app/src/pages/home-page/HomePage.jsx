import "./homepage.css";
import React, { useRef } from 'react';
import { Box, Button, Typography } from "@mui/material";
import { NavigationBar } from "../../components/navigation/NavigationBar";
import { LocationSelection } from "../../components/weather-selection/LocationSelection";
import { Fade } from "react-awesome-reveal";

export const Home = () => {
  const ref = useRef(null);

  const handleClick = () => {
    ref.current?.scrollIntoView({behavior: 'smooth'});
  };

  return (
    <Box className="home-container">
      <NavigationBar />

      <Box className="page-container">
        <Box className="banner-container">
          <Box className="banner">
            <Fade cascade damping={0.6} className="text-containter">
              <Typography variant="h4" fontWeight={"fontWeightLight"}>
                Making weather lookup
              </Typography>
              <Typography
                variant="h3"
                fontWeight={"fontWeightHeavy"}
                sx={{ color: "#02387f" }}
              >
                Simple and Seamless
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={handleClick}
                sx={{ mt: "2rem", backgroundColor: "black" }}
              >
                Get Started
              </Button>
            </Fade>
          </Box>
        </Box>
        <LocationSelection ref={ref} />
      </Box>
    </Box>
  );
};
