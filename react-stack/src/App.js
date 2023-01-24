import React, { useState } from "react";
import "./App.css";

let socket = new WebSocket("wss://javascript.info/article/websocket/demo/hello");

socket.onopen = function(e) {
  alert("[open] Connection established");
  alert("Sending to server");
  socket.send("My name is John");
};

socket.onmessage = function(event) {
  alert(`[message] Data received from server: ${event.data}`);
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    alert('[close] Connection died');
  }
};

socket.onerror = function(error) {
  alert(`[error]`);
};

function App(){
  const [payload,setPayload] = useState([]);
  socket.onmessage = function(event) {
    setPayload(event.data)
  };
  return(
    <div>
      <img src={`data:image/png;base64,${payload}`}/>
    </div>
  )
}


export default App;