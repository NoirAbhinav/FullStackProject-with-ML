import React, { useContext } from "react";
import { Button, Toolbar, Typography } from "@mui/material";
import ApiOnClick from "../apiCalls";
import Pipes_handtrack from "../handTrack/Pipes";
import Pipes_emotion from "../EmotionPipelines/Pipes";
import FingerprintProvider, { FingerPrintContext } from "../fingerContext";
function Demo() {
  const fingerContext = useContext(FingerPrintContext);

  const fpPromise = import("https://openfpcdn.io/fingerprintjs/v3").then(
    (FingerprintJS) => FingerprintJS.load()
  );
  fpPromise
    .then((fp) => fp.get())
    .then((result) => {
      // This is the visitor identifier:
      const visitorId = result.visitorId;
      console.log(visitorId);
      fingerContext.setFingerprint(visitorId);
      console.log(window.screen.orientation.type);
      if (window.screen.orientation.type === "landscape-primary") {
        fingerContext.setDevicetype("PC");
      } else {
        fingerContext.setDevicetype("mobile");
      }
    });
  window.addEventListener("beforeunload", (ev) => {
    const rt = ApiOnClick("model/close", fingerContext.getFingerprint());
    return rt;
  });
  const [show, setShow] = React.useState({
    emotionPipes: false,
    handMotionDetect: false,
  });
  const [label, setLabel] = React.useState({
    emotionPipes: true,
    handMotionDetect: true,
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
  const handleLabel = (val) => {
    setLabel((prev) => {
      let x = { ...prev };
      if (new Set(Object.values(x)).size === 1) {
        Object.keys(x).forEach((n) => {
          x[n] = false;
        });
        x[val] = !x[val];
        return { ...x };
      }
      if (x[val] === true && new Set(Object.values(x)).size !== 1) {
        Object.keys(x).forEach((n) => {
          x[n] = true;
        });
        return { ...x };
      }
    });
  };

  return (
    <div className="contDemo showDataDemo">
      <Toolbar
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          top: "10px",
          gap: "5px",
        }}
      >
        {label.emotionPipes && (
          <Button
            variant="contained"
            onClick={() => {
              handleClick("emotionPipes");
              handleLabel("emotionPipes");
            }}
          >
            <Typography variant="button">
              Emotion Detection Project
              {new Set(Object.values(label)).size !== 1 && (
                <>
                  <br />
                  (Tap again to Return)
                </>
              )}
            </Typography>
          </Button>
        )}
        {label.handMotionDetect && (
          <Button
            variant="contained"
            onClick={() => {
              handleClick("handMotionDetect");
              handleLabel("handMotionDetect");
            }}
            sx={{ textAlign: "center" }}
          >
            <Typography variant="button">
              Hand Motion Detection
              {new Set(Object.values(label)).size !== 1 && (
                <>
                  <br />
                  (Tap again to Return)
                </>
              )}
            </Typography>
          </Button>
        )}
      </Toolbar>
      <div className="MLPipes">
        {show.emotionPipes && <Pipes_emotion />}
        {show.handMotionDetect && <Pipes_handtrack />}
      </div>
    </div>
  );
}

export default Demo;
