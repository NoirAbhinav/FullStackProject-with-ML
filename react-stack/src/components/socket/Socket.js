
import React from "react";
import "./Socket.css";
function Socket_send({ socket, children }) {
  const [image, setImage] = React.useState(null);
  socket.current.onmessage = (event) => {
    socket.current.send("Received");
    setImage(event.data);
  };
  return (
    <div className="socket">
      <img src={`data:image/png;base64,${image}`} />
      {children}
    </div>
  );
}

function Socket() {
  const socket = React.useRef(new WebSocket("ws://localhost:8000/ws"));
  React.useEffect(() => {
    socket.current.onopen = function (e) {
      console.log("[open] connection established");
    };
    return () => {
      console.log("Closing...");
      socket.current.send("closed");
      socket.current.close();
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
      <Socket_send socket={socket}>
      </Socket_send>
    </>
  );
}

export default Socket;
