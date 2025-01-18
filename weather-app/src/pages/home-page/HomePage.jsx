import "./homepage.css";
import React, { useRef } from 'react';
import { Box, Button, Typography } from "@mui/material";
import { NavigationBar } from "../../components/navigation/NavigationBar";
import { LocationSelection } from "../../components/weather-selection/LocationSelection";

export const Home = () => {
  const ref = useRef(null);

  const handleClick = () => {
    ref.current?.scrollIntoView({behavior: 'smooth'});
  };

  return (
    <Box className="home-container">
      <NavigationBar />

      <Box className="page-container">
        <LocationSelection ref={ref} />
      </Box>
    </Box>
  );
};
