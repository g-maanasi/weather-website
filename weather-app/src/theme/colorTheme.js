import { createTheme } from "@mui/material/styles";

export const lightTheme = createTheme({
  palette: {
    primary: {
      main: "#ffffff",
    },
    secondary: {
      main: "#cee0ee",
    },
    mainText: {
      main: "#3d82f2",
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    primary: {
      main: "#00296b",
    },
    secondary: {
      main: "#cee0ee",
    },
    mainText: {
      main: "#3d82f2",
    },
  },
});
