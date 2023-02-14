import React from "react";
import { Button, Toolbar } from "@mui/material";
import "./Pipes.css";
import VideoTest from "./socket/vidstream";
function Pipes() {
  const [show, setShow] = React.useState({
    eda: false,
    modelInfo: false,
    socket: false,
  });

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
        {/* <Button variant="contained" onClick={() => handleClick("eda")}>
          EDA
        </Button>
        <Button variant="contained" onClick={() => handleClick("modelInfo")}>
          Model Info
        </Button> */}
        <Button variant="contained" onClick={() => handleClick("socket")}>
          Use
        </Button>
      </Toolbar>
      <div className="MLPipes">
        {show.socket && <VideoTest />}
        {/* {show.eda && <EDA_pipes />}
        {show.modelInfo && <Flow />} */}
      </div>
    </>
  );
}

export default Pipes;
