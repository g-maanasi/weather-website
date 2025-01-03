import './navigationBar.css'
import {
  Box,
  FormControl,
  InputAdornment,
  OutlinedInput,
  Typography,
} from "@mui/material";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import SearchIcon from "@mui/icons-material/Search";
import { Link } from "react-router-dom";

export const NavigationBar = () => {
  return (
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
            Climafy
          </Typography>
        </Box>

        <Box className="right-container">
          <Box className="search-bar">
            <FormControl sx={{ m: 1, width: "24ch" }} variant="outlined">
              <OutlinedInput
                id="outlined-adornment-weight"
                startAdornment={
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                }
                aria-describedby="outlined-weight-helper-text"
                inputProps={{
                  "aria-label": "weight",
                }}
                size="small"
              />
            </FormControl>
          </Box>
          <Box className="log-in-container">
            <Link href="login">Log In or Sign Up</Link>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};
