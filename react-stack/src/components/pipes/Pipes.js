import React from "react";
import { Button, Toolbar } from "@mui/material";
import axios from "axios";
import Socket from "../socket/Socket";
import "./Pipes.css";
function ApiOnClick({ data, setData, endpoint }) {
  React.useEffect(() => {
    axios
      .post("http://localhost:8000/" + endpoint, {
        ml_module: "emotions",
      })
      .then(function (response) {
        console.log(response.data[0]);
        setData(response.data[0]);
      });
  }, []);

  return (
    <div className="edaImg">
      <img width="100" src={`data:image/png;base64,${data}`} />
    </div>
  );
}
function Pipes() {
  const [show, setShow] = React.useState({
    eda: false,
    socket: false,
    getData: false,
    transformData: false,
    loadData: false,
    trainModel: false,
  });
  const [data, setData] = React.useState(null);

  const handleClick = (val) => {
    setShow((prev) => {
      let x = { ...prev };
      Object.keys(x).forEach((n) => {
        if (val !== n) x[n] = false;
      });
      x[val] = !x[val];
      return { ...x };
    });
  };

  return (
    <>
      <Toolbar
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          top: "10px",
          gap: "5px",
        }}
      >
        <Button variant="contained" onClick={() => handleClick("eda")}>
          EDA
        </Button>
        <Button variant="contained" onClick={() => handleClick("socket")}>
          Get Data
        </Button>
        <Button variant="contained" onClick={() => handleClick("socket")}>
          Transform Data
        </Button>
        <Button variant="contained" onClick={() => handleClick("socket")}>
          Load Data
        </Button>
        <Button variant="contained" onClick={() => handleClick("socket")}>
          Train Model
        </Button>
        <Button variant="contained" onClick={() => handleClick("socket")}>
          Use
        </Button>
      </Toolbar>
      <div className="MLPipes">
        {show.socket && <Socket />}
        {show.eda && (
          <ApiOnClick endpoint={"model/EDA"} data={data} setData={setData} />
        )}
      </div>
    </>
  );
}

export default Pipes;
