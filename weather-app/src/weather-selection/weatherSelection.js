import { useEffect, useState } from "react";
import { Autocomplete, Box, TextField } from "@mui/material";

export const WeatherSelection = () => {
  const [countryList, setCountryList] = useState([{ Name: "United States of America" }]);
  const [regionList, setRegionList] = useState([{ name: "New York" }]);
  const [cityList, setCityList] = useState([{ name: "New York City" }]);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [selectedRegion, setSelectedRegion] = useState("");
  const [selectedCity, setSelectedCity] = useState("");

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
          if (result["regions"].length === 0) {
            setSelectedRegion(null);
          } else {
            setSelectedRegion("");
            setRegionList(result["regions"]);
          }
        });
    }
  };

  const onRegionSelect = (event, value, reason) => {
    if (reason === "selectOption") {
      setSelectedRegion(value);
      console.log("Option selected:", value);
      const selection = selectedCountry['label'] + "," + value['label'];
      fetch(`http://127.0.0.1:5000/all_region_cities/${selection}`)
        .then((res) => res.json())
        .then((result) => {
          setSelectedCity("");
          setCityList(result['cities']);
        });
    }
  };

  const onCitySelect = (event, value, reason) => {
    if (reason === "selectOption") {
      setSelectedCity(value);
      console.log("Option selected:", value);
    }
  };

  return (
    <Box>
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

      {(selectedRegion !== "" || ((selectedRegion === null) && (selectedCountry !== ""))) && (
        <Autocomplete
          disablePortal
          options={cityList}
          sx={{ width: 300, mt: 5 }}
          onChange={onCitySelect}
          value={selectedCity}
          renderInput={(params) => <TextField {...params} label="City" />}
        />
      )}
    </Box>
  );
};
