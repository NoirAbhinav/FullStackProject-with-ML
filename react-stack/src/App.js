import React from "react";
import "./App.css";
import ResponsiveSideBar from "./components/SideIcon/SideIcon";
import ResponsiveTopBar from "./components/TopBar/TopBar";
import FingerprintProvider from "./components/pipes/fingerContext";

function App() {
  return (
    <>
      <FingerprintProvider>
        <ResponsiveTopBar />
        <ResponsiveSideBar />
      </FingerprintProvider>
    </>
  );
}

export default App;
