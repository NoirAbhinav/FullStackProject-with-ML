import { CircularProgress } from "@mui/material";
import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import "./vidStream.css";
function MyWebcam({ socket, intervalRef, children }) {
  const [image, setImage] = React.useState(null);
  const webcamRef = useRef(null);

  const startCapture = () => {
    intervalRef.current = setInterval(() => {
      if (webcamRef.current.getScreenshot()) {
        const imageSrc = webcamRef.current.getScreenshot();
        console.log(socket.current.readyState);
        socket.current.send(imageSrc);
        socket.current.onmessage = (event) => {
          setImage(event.data);
        };
      }
    }, 1000 / 10);
  };

  if (!intervalRef.current) {
    startCapture();
  }

  // if (intervalRef.current === null) {
  //   stopCapture();
  // }

  return (
    <>
      <Webcam
        className="webcamPrev"
        muted={false}
        audio={false}
        height={350}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={350}
      />
      {!image && (
        <CircularProgress color="secondary" sx={{ position: "unset" }} />
      )}
      {image && (
        <div className="socket">
          <img
            key="A"
            src={"data:image/jpeg;base64," + image}
            alt={`Screenshot ${1}`}
            style={{ marginRight: 10 }}
          />
        </div>
      )}
    </>
  );
}
function Socket() {
  const socket = React.useRef(new WebSocket("ws://localhost:8000/ws"));
  const intervalRef = useRef(null);
  const closeRef = useRef(false);
  const stopCapture = () => {
    clearInterval(intervalRef.current);
    intervalRef.current = null;
    closeRef.current = true;
  };

  React.useEffect(() => {
    socket.current.onopen = function (e) {
      console.log("[open] connection established");
    };
    return () => {
      console.log("Closing...");
      socket.current.send("closed");
      socket.current.close();
      stopCapture();
      socket.current.onclose = function (event) {
        if (event.wasClean) {
          console.log(
            `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
          );
        }
      };
    };
  }, []);
  return (
    <>
      <MyWebcam socket={socket} intervalRef={intervalRef}></MyWebcam>
    </>
  );
}
export default Socket;
