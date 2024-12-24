import "./weatherSelection.css";
import { useEffect, useState } from "react";
import { Autocomplete, Box, Button, TextField } from "@mui/material";

export const LocationSelection = () => {
  const [countryList, setCountryList] = useState([{ label: "United States" }]);
  const [regionList, setRegionList] = useState([{ label: "New York" }]);
  const [cityList, setCityList] = useState([{ label: "New York City" }]);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [selectedRegion, setSelectedRegion] = useState("");
  const [selectedCity, setSelectedCity] = useState("");
  const [submitAvailable, setSubmitAvailable] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/all_countries")
      .then((res) => res.json())
      .then((result) => {
        setCountryList(result["countries"]);
        console.log(result);
      });
  }, [setCountryList]);

  const onCountrySelect = (event, value, reason) => {
    if (reason === "selectOption") {
      setSelectedCountry(value);
      console.log("Option selected:", value);

      fetch(`http://127.0.0.1:5000/all_country_regions/${value["label"]}`)
        .then((res) => res.json())
        .then((result) => {
          if (!result || result["regions"].length === 0) {
            setSelectedRegion(null);
            getCitiesFromCountry(value["label"]);
          } else {
            setSelectedRegion("");
            setRegionList(result["regions"]);
          }
        });
    }
  };

  const getCitiesFromCountry = (country) => {
    fetch(`http://127.0.0.1:5000/all_country_cities/${country}`)
      .then((res) => res.json())
      .then((result) => {
        setSelectedCity("");
        setCityList(result["cities"]);
      });
  };

  const onRegionSelect = (event, value, reason) => {
    if (reason === "selectOption") {
      setSelectedRegion(value);
      console.log("Option selected:", value);
      const selection = selectedCountry["label"] + "," + value["label"];

      fetch(`http://127.0.0.1:5000/all_region_cities/${selection}`)
        .then((res) => res.json())
        .then((result) => {
          setSelectedCity("");
          setCityList(result["cities"]);
        });
    }
  };

  const onCitySelect = (event, value, reason) => {
    if (reason === "selectOption") {
      setSelectedCity(value);
      console.log("Option selected:", value);
      setSubmitAvailable(true);
    }
  };

  const getWeather = async () => {
    const weatherInfo = {
      city: selectedCity.label,
      region: selectedRegion.label,
      country: selectedCountry.label,
    };
    const url = "http://127.0.0.1:5000/get_weather";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(weatherInfo),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Box className="selection-container">
      <Autocomplete
        disablePortal
        options={countryList}
        sx={{ width: 300 }}
        onChange={onCountrySelect}
        value={selectedCountry}
        renderInput={(params) => <TextField {...params} label="Country" />}
      />

      {selectedCountry !== "" && selectedRegion !== null && (
        <Autocomplete
          disablePortal
          options={regionList}
          sx={{ width: 300, mt: 5 }}
          onChange={onRegionSelect}
          value={selectedRegion}
          renderInput={(params) => <TextField {...params} label="Region" />}
        />
      )}

      {(selectedRegion !== "" ||
        (selectedRegion === null && selectedCountry !== "")) && (
        <Autocomplete
          disablePortal
          options={cityList}
          sx={{ width: 300, mt: 5 }}
          onChange={onCitySelect}
          value={selectedCity}
          renderInput={(params) => <TextField {...params} label="City" />}
        />
      )}

      {submitAvailable && (
        <Button className="search-button" onClick={getWeather}>
          Search
        </Button>
      )}
    </Box>
  );
};
