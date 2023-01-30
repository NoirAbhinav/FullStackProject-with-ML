import React from "react";
import "./App.css";
import ResponsiveSideBar from "./components/SideIcon/SideIcon";
import ResponsiveTopBar from "./components/TopBar/TopBar";
function App() {
  return (
    <>
      <ResponsiveTopBar />
      <ResponsiveSideBar />
    </>
  );
}

export default App;
